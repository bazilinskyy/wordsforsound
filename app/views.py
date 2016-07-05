# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from __future__ import division
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.mail import Message
from datetime import datetime
from app import app, db, lm, oid, mail
from .forms import DescriptionForm, NewAssetForm, AddTagForm, AddSoundForm, DeleteTagForm, DeleteSoundForm, \
    VerificationForm, IterationForm, NewProjectForm, EditSoundForm, LoginForm, PasswordForm, EmailForm, \
    RegisterForm, SearchForm, EditForm
from .models import Description, Asset, Tag, Sound, AssetStatus, Iteration, Verification, Project, User, \
    SupplierUser, ClientUser
from .emails import follower_notification
from .util import ts
from config import SOUNDS_PER_PAGE, MAX_SEARCH_RESULTS, ONGOING_PROJECTS_MENU, FINISHED_PROJECTS_MENU, \
    ONGOING_ASSETS_MENU, FINISHED_ASSETS_MENU, SOUND_UPLOAD_FOLDER, ATACHMENT_UPLOAD_FOLDER, TAGS_FILE, \
    TAGS_PER_PAGE, ASSETS_PER_PAGE, DATABASE_QUERY_TIMEOUT
from werkzeug import secure_filename
from flask_wtf.file import FileField
import os
import time
import json

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
        g.assets_ongoing = Asset.query.filter_by(finished=False).limit(ONGOING_ASSETS_MENU).all()
        g.assets_finished = Asset.query.filter_by(finished=True).limit(FINISHED_ASSETS_MENU).all()
        g.projects_ongoing = Project.query.filter_by(finished=False).limit(ONGOING_PROJECTS_MENU).all()
        g.projects_finished = Project.query.filter_by(finished=True).limit(FINISHED_PROJECTS_MENU).all()

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning(
                "SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                (query.statement, query.parameters, query.duration,
                 query.context))
    return response

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    error = None
    form = LoginForm()
    if request.method == 'POST':
      if form.validate_on_submit():
          user = User.query.filter_by(nickname=form.username.data).first()
          if user is not None and user.password == form.password.data:
              login_user(user)
              session['remember_me'] = form.remember_me.data
              return redirect(url_for('index', just_logged_in = 'Yes'))
          else:
              error = 'Invalid username or password.'
    return render_template('login.html', 
                            form=form, 
                            error=error,
                            title='Sign In',
                            )

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.user_type.data == '1':
            user = ClientUser(
                nickname=form.nickname.data,
                email=form.email.data,
                password=form.password.data
            )
        else:
            user = SupplierUser(
                nickname=form.nickname.data,
                email=form.email.data,
                password=form.password.data
            )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        # make the user follow him/herself
        # db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Email not found.')
        else:
            token = ts.dumps(user.email, salt='recover-key')

            recover_url = url_for(
                'reset_with_token',
                token=token,
                _external=True)

            msg = Message(subject="Password reset requested",
                      sender="wordsforsound@gmail.com",
                      recipients=user.email,
                      html = "Please click on {{ recover_url }} to recover your password. Thank you!")

            # msg.html = render_template(
            #     'email/recover.html',
            #     recover_url=recover_url)

            # Send email with recovery link
            #TODO does not send email
            mail.send(msg)

            return redirect(url_for('index'))
    return render_template('reset.html', form=form)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('reset_with_token.html', form=form, token=token)

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    user_assets = Asset.query.filter_by(in_hands_id = user.id).paginate(page, ASSETS_PER_PAGE, False)
    print "Assets " + str(user_assets.items)
    return render_template('user.html',
                           page=page,
                           user=user,
                           user_assets=user_assets)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    elif request.method != "POST":
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.route('/follow/<nickname>', methods=['GET', 'POST'])
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname)
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>', methods=['GET', 'POST'])
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page_description>/<int:page_iteration>/<int:page_verification>/<int:page_otherhands>', methods=['GET', 'POST'])
@login_required
def index(page_description=1, page_iteration=1, page_verification=1, page_otherhands=1):
    assets_description = Asset.query.filter_by(status = 1).join((ClientUser, Asset.clients)).filter_by(id = g.user.id).paginate(page_description, ASSETS_PER_PAGE, False)
    assets_iteration = Asset.query.filter_by(status = 2).join((SupplierUser, Asset.suppliers)).filter_by(id = g.user.id).paginate(page_iteration, ASSETS_PER_PAGE, False)
    assets_verification = Asset.query.filter_by(status = 3).join((ClientUser, Asset.clients)).filter_by(id = g.user.id).paginate(page_verification, ASSETS_PER_PAGE, False)
    assets_otherhands = Asset.query.filter(Asset.in_hands_id != g.user.id).paginate(page_otherhands, ASSETS_PER_PAGE, False)

    return render_template('index.html',
                           title='Home',
                           assets_otherhands=assets_otherhands,
                           assets_description = assets_description,
                           assets_iteration = assets_iteration,
                           assets_verification = assets_verification,
                           page_description=page_description,
                           page_iteration=page_iteration,
                           page_verification=page_verification,
                           page_otherhands=page_otherhands)

@app.route('/tags', methods=['GET', 'POST'])
@app.route('/tags/<int:page>', methods=['GET', 'POST'])
@login_required
def tags(page=1):
    tags = Tag.query.paginate(page, TAGS_PER_PAGE, False)
    return render_template('tags.html',
                            title='Tags',
                            tags=tags)
@app.route('/tag')
@app.route('/tag/<int:tag_id>/')
@login_required
def tag(tag_id, page=1):
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        flash('Tag not found.')
        return redirect(url_for('index'))
    sounds = tag.sounds.paginate(page, SOUNDS_PER_PAGE, False)
    return render_template('tag.html',
                           title='Tag',
                           tag=tag,
                           page=page,
                           sounds=sounds)

@app.route('/add_tag', methods=['GET', 'POST'])
@login_required
def add_tag():
    form = AddTagForm()
    if form.validate_on_submit():
        # check if tag woth the same name exists
        tag = Tag.query.filter_by(name=form.name.data).first()
        if tag is not None:
            flash('This tag already exists.')
            return render_template('add_tag.html',
                            form=form,
                            title='Add tag')
        tag = Tag()
        tag.timestamp = datetime.now()
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()

        # for autofill for tags and tag cloud
        tags = Tag.query.all()
        tags_json = []
        if tags is not None:
            # Determine highest number of sounds linked to a tag for giving max weight of 1.0
            # max_number_of_sounds = 0
            # for tag in tags:
            #     if tag.sounds.count() > max_number_of_sounds:
            #         max_number_of_sounds = tag.sounds.count()
            # print max_number_of_sounds
            for tag in tags:
                tag_id = tag.id
                tag_name = tag.name
                # tag_weight = tag.sounds.count() / max_number_of_sounds # weight for jQuery
                tag_weight = tag.sounds.count()
                tag_link = "tag/" + str(tag.id)
                tags_json.append({'value': tag_id, 'text' : tag_name, 'weight' : tag_weight, 'link' : tag_link})
                with open('app/' + TAGS_FILE, 'w') as outfile:
                    json.dump(tags_json, outfile)
        
        flash('New tag added.')
        return redirect(url_for('add_tag'))
    return render_template('add_tag.html',
                            form=form,
                            title='Add tag')

@app.route('/delete_tag', methods=['GET', 'POST'])
@login_required
def delete_tag():
    form = DeleteSoundForm()
    if form.validate_on_submit():
        tag = Tag.query.filter_by(name=form.name.data).first()
        if tag == None:
            flash('Tag ' +  form.name.data + ' does not exist.')
            return redirect(url_for('delete_tag'))
        db.session.delete(tag)
        db.session.commit()  
        
        flash('Tag ' +  form.name.data + ' was deleted.')
        return redirect(url_for('delete_tag'))
    return render_template('delete_tag.html',
                            form=form,
                            title='Delete tag')

@app.route('/sounds', methods=['GET', 'POST'])
@app.route('/sounds/<int:page>', methods=['GET', 'POST'])
@login_required
def sounds(page=1):
    sound_location = SOUND_UPLOAD_FOLDER
    sounds = Sound.query.paginate(page, SOUNDS_PER_PAGE, False)
    return render_template('sounds.html',
                            sounds=sounds,
                            sound_location=sound_location)

@app.route('/sound', methods=['GET', 'POST'])
@app.route('/sound/<int:sound_id>/', methods=['GET', 'POST'])
@login_required
def sound(sound_id):
    sound = Sound.query.filter_by(id=sound_id).first()
    if sound is None:
        flash('Sound not found.')
        return redirect(url_for('index'))

    sound_location = SOUND_UPLOAD_FOLDER
    if sound.description == '':
    	sound.description = 'N/A'

    return render_template('sound.html',
                           sound=sound,
                           sound_location=sound_location)

@app.route('/sound/edit', methods=['GET', 'POST'])
@app.route('/sound/<int:sound_id>/edit/', methods=['GET', 'POST'])
@login_required
def sound_edit(sound_id):
    sound = Sound.query.filter_by(id=sound_id).first()
    form = EditSoundForm()

    if form.validate_on_submit():
        # check if sound woth the same name exists
        sound = Sound.query.filter_by(id=sound_id).first()
        sound.timestamp = datetime.now()
        sound.name = form.name.data
        sound.description = form.description.data
        sound.sound_type = form.sound_type.data
        sound.sound_family = form.sound_family.data
        sound.rights = form.rights.data

        # add tags
        sound.ags = []
        for tag in form.tags.data:
            if tag != ',':
                sound.tags.append(Tag.query.filter_by(id=int(tag)).first())

        # Upload file
        filename = secure_filename(form.upload_file.data.filename)
        if os.path.isfile('app/' + SOUND_UPLOAD_FOLDER + filename):
            current_milli_time = lambda: int(round(time.time() * 1000))
            filename = str(current_milli_time()) + filename
        form.upload_file.data.save('app/' + SOUND_UPLOAD_FOLDER + filename)
        sound.filename = filename

        db.session.commit()
        
        flash('Sound was edited.')
        return redirect(url_for('index'))

    elif request.method != "POST":
        if sound is not None:
            form.name.data = sound.name
            form.description.data = sound.description
            form.sound_type.data = sound.sound_type
            form.sound_family.data = sound.sound_family
            form.rights.data = sound.rights

    return render_template('edit_sound.html',
                           form=form,
                           sound=sound)

@app.route('/assets/<string:assets_type>', methods=['GET', 'POST'])
@login_required
def assets(assets_type):
    if assets_type == 'ongoing':
        assets = Asset.query.filter_by(finished=False).all()
    elif assets_type == 'finished':
        assets = Asset.query.filter_by(finished=True).all()
    else:
        assets = Asset.query.all()
    return render_template('assets.html',
                            assets=assets,
                            assets_type=assets_type)
@app.route('/asset')
@app.route('/asset/<int:asset_id>/')
@login_required
def asset(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('asset.html',
                           asset=asset,
                           attachment_location = attachment_location)


@app.route('/project/edit', methods=['GET', 'POST'])
@app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project is None:
        flash('Project not found.')
        return redirect(url_for('index'))
    form = NewProjectForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            if request.form['submit'] == 'edit':
              project.timestamp = datetime.now()
              project.name = form.name.data
              project.description = form.description.data
              
              # Upload file
              if form.upload_file.data.filename:
                filename = secure_filename(form.upload_file.data.filename)
                if os.path.isfile('app/' + ATACHMENT_UPLOAD_FOLDER + filename):
                    current_milli_time = lambda: int(round(time.time() * 1000))
                    filename = str(current_milli_time()) + filename
                form.upload_file.data.save('app/' + ATACHMENT_UPLOAD_FOLDER + filename)
                project.filename = filename

              flash('Project was edited successfully.')

            elif request.form['submit'] == 'finalise':
              project.finished = True
              flash('Project was marked as finished.')

            else:
              flash('Unknown status.')
              pass # unknown

        db.session.add(project)
        db.session.commit()    
        
        return redirect(url_for('project', project_id=project_id))

    elif request.method != "POST":
        if project is not None:
          form.name.data = project.name
          form.description.data = project.description

    return render_template('edit_project.html',
                            form=form,
                            title='Edit project',
                            project=project,
                            assets_ongoing = HorizontalMenu.projects_ongoing,
                            assets_finished = HorizontalMenu.projects_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/descriptions', methods=['GET', 'POST'])
@login_required
def descriptions():
    descriptions = Description.query.all()
    return render_template('descriptions.html',
                            descriptions=descriptions)

@app.route('/description', methods=['GET', 'POST'])
@app.route('/description/<int:description_id>/', methods=['GET', 'POST'])
@login_required
def description(description_id):
    description = Description.query.filter_by(id=description_id).first()
    if description is None:
        flash('Description not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('description.html',
                           description=description,
                           attachment_location=attachment_location)

@app.route('/iterations', methods=['GET', 'POST'])
@login_required
def iterations():
    iterations = Iteration.query.all()
    return render_template('iterations.html',
                            iterations=iterations,
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished,)

@app.route('/iteration', methods=['GET', 'POST'])
@app.route('/iteration/<int:iteration_id>/', methods=['GET', 'POST'])
@login_required
def iteration(iteration_id):
    iteration = Iteration.query.filter_by(id=iteration_id).first()
    if iteration is None:
        flash('Itteration not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('iteration.html',
                           iteration=iteration,
                           attachment_location=attachment_location)

@app.route('/verifications', methods=['GET', 'POST'])
@login_required
def verifications():
    verifications = Verification.query.all()
    return render_template('verifications.html',
                            verifications=verifications)

@app.route('/verification', methods=['GET', 'POST'])
@app.route('/verification/<int:verification_id>/', methods=['GET', 'POST'])
@login_required
def verification(verification_id):
    verification = Verification.query.filter_by(id=verification_id).first()
    if verification is None:
        flash('Verification not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('verification.html',
                           verification=verification,
                           attachment_location=attachment_location)

@app.route('/add_sound', methods=['GET', 'POST'])
@login_required
def add_sound():
    form = AddSoundForm()
    if form.validate_on_submit():
        # check if sound woth the same name exists
        sound = Sound.query.filter_by(name=form.name.data).first()
        if sound is not None:
            flash('Sound with the same name already exists.')
            return render_template('add_sound.html',
                            form=form,
                            title='Add sound')
        sound = Sound()
        sound.timestamp = datetime.now()
        sound.name = form.name.data
        sound.description = form.description.data
        sound.sound_type = form.sound_type.data
        sound.sound_family = form.sound_family.data
        sound.rights = form.rights.data

        # add tags
        for tag in form.tags.data:
            if tag != ',':
                sound.tags.append(Tag.query.filter_by(id=int(tag)).first())

        # Upload file
        filename = secure_filename(form.upload_file.data.filename)
        if os.path.isfile('app/' + SOUND_UPLOAD_FOLDER + filename):
            current_milli_time = lambda: int(round(time.time() * 1000))
            filename = str(current_milli_time()) + filename
        form.upload_file.data.save('app/' + SOUND_UPLOAD_FOLDER + filename)
        sound.filename = filename

        db.session.add(sound)
        db.session.commit()
        
        flash('New sound added.')
        return redirect(url_for('add_sound'))
    filename = None
    return render_template('add_sound.html',
                            form=form,
                            title='Add sound',
                            filename=filename)

@app.route('/delete_sound', methods=['GET', 'POST'])
@login_required
def delete_sound():
    form = DeleteSoundForm()
    if form.validate_on_submit():
        sound = Sound.query.filter_by(name=form.name.data).first()
        if sound == None:
            flash('Sound ' +  form.name.data + ' does not exist.')
            return redirect(url_for('delete_sound'))
        try:
            os.remove(os.path.join(SOUND_UPLOAD_FOLDER, sound.filename)) # delete uploaded file
        except OSError:
            pass
        db.session.delete(sound)
        db.session.commit()  
        
        flash('Sound ' +  form.name.data + ' was deleted.')
        return redirect(url_for('delete_sound'))
    return render_template('delete_sound.html',
                            form=form,
                            title='Delete sound')

# Create new asset with status = iteration. Creation process also includes the first description stage.
@app.route('/add_asset', methods=['GET', 'POST'])
@login_required
def add_asset():
    if g.user.type == "supplier_user":
        flash('You do not have permissions to request new assets.')
        return redirect(url_for('index'))

    form = NewAssetForm()

    # List of projects for selection during new asset creation
    projects = Project.query.all()
    project_choices = []
    for project in projects:
        project_choices.append((str(project.id), project.name))
    form.project.choices = project_choices
    # List of users as clients for new assets
    clients = ClientUser.query.all()
    clients_choices = []
    for client in clients:
        clients_choices.append((str(client.id), client.nickname + ' : ' + client.full_name))
    form.clients.choices =clients_choices
    # List of users as suppliers for new assets
    suppliers = SupplierUser.query.all()
    suppliers_choices = []
    for supplier in suppliers:
        suppliers_choices.append((str(supplier.id), supplier.nickname + ' : ' + supplier.full_name))
    form.suppliers.choices = suppliers_choices

    if form.validate_on_submit():
        asset = Asset()
        asset.timestamp = datetime.now()
        asset.name = form.name.data
        asset.finished = False
        asset.status = AssetStatus.iteration.value
        asset.iteration_number = 0
        asset.description = form.description.data
        asset.project_id = form.project.data
        for client in form.clients.data:
            asset.client_add(ClientUser.query.filter_by(id=int(client)).first())
        for supplier in form.suppliers.data:
            asset.supplier_add(SupplierUser.query.filter_by(id=int(supplier)).first())
        asset.in_hands_id = asset.suppliers[0].id  # After creating the request for the asset the \
                                                   # first user to work on it is the first supplier        
        # Upload file
        if form.upload_file.data.filename:
	        filename = secure_filename(form.upload_file.data.filename)
	        if os.path.isfile('app/' + ATACHMENT_UPLOAD_FOLDER + filename):
	            current_milli_time = lambda: int(round(time.time() * 1000))
	            filename = str(current_milli_time()) + filename
	        form.upload_file.data.save('app/' + ATACHMENT_UPLOAD_FOLDER + filename)
	        asset.filename = filename

        db.session.add(asset)
        db.session.commit()    
        
        description = Description()
        description.description = form.description.data
        description.duration = form.duration.data
        description.pitch = form.pitch.data
        description.sound_type = form.sound_type.data
        description.sound_family = form.sound_family.data
        description.timestamp = datetime.now()
        description.asset_id = asset.id

        # Add tags
        for tag in form.tags.data:
            if tag != ',':
                description.tags.append(Tag.query.filter_by(id=int(tag)).first())

        db.session.add(description)
        db.session.commit()
        
        flash('New asset description created.')
        return redirect(url_for('index'))
    return render_template('add_asset.html',
                            form=form,
                            title='Add asset')

@app.route('/describe', methods=['GET', 'POST'])
@app.route('/describe/<int:asset_id>/', methods=['GET', 'POST'])
@login_required
def describe(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    # if g.user not in project.owners:
    #     flash('You do not have permissions to create milestones for this project.')
    #     return redirect(url_for('index'))
    # description = None
    # if description_id:
    #     description = Description.query.filter_by(id=description_id).first()

    form = DescriptionForm()
    if form.validate_on_submit():
        # get asset similar to project_id 
        description = Description()
        description.description = form.description.data
        description.duration = form.duration.data
        description.pitch = form.pitch.data
        description.sound_type = form.sound_type.data
        description.sound_family = form.sound_family.data
        description.timestamp = datetime.now()
        description.asset_id = asset.id

        asset.description = form.description.data

        # Found who needs to work on the asset next
        current_user_found  = False
        in_hands_found = False
        if len(asset.clients.all()) != 1:
            if len(asset.clients.all()) < 1:
                flash('No clients for the asset.')
                return redirect(url_for('index'))  
            for client in asset.clients:
                if client.id == g.user.id:
                    current_user_found = True
                elif current_user_found == True:
                    asset.in_hands_id = client.id
                    in_hands_found = True
                    break

        if not in_hands_found:
            if len(asset.suppliers.all()) < 1:
                flash('No suppliers for the asset.')
                return redirect(url_for('index'))    
            asset.in_hands_id = asset.suppliers[0].id
            asset.status = AssetStatus.iteration.value


        # Upload file
        if form.upload_file.data:
	        filename = secure_filename(form.upload_file.data.filename)
	        if os.path.isfile('app/' + ATACHMENT_UPLOAD_FOLDER + filename):
	            current_milli_time = lambda: int(round(time.time() * 1000))
	            filename = str(current_milli_time()) + filename
	        form.upload_file.data.save('app/' + ATACHMENT_UPLOAD_FOLDER + filename)
	        description.filename = filename

        db.session.add(description)
        db.session.commit()
        
        flash('Description created.')
        return redirect(url_for('index'))
    elif request.method != "POST":
        if asset.descriptions.count() > 0 is not None:
            description = asset.descriptions.first()
            form.description.data = description.description
            form.duration.data = description.duration
            form.pitch.data = description.pitch
            form.sound_type.data = description.sound_type
            form.sound_family.data = description.sound_family
    return render_template('describe.html',
                            form=form,
                            asset=asset,
                            title='Describe asset')

@app.route('/verify', methods=['GET', 'POST'])
@app.route('/verify/<int:asset_id>/', methods=['GET', 'POST'])
@login_required
def verify(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    # if g.user not in project.owners:
    #     flash('You do not have permissions to create milestones for this project.')
    #     return redirect(url_for('index'))
    # description = None
    # if description_id:
    #     description = Description.query.filter_by(id=description_id).first()

    form = VerificationForm()
    if form.validate_on_submit():
        # get asset similar to project_id 
        verification = Verification()
        verification.description = form.description.data
        verification.timestamp = datetime.now()
        verification.asset_id = asset.id

        # Upload file
        if form.upload_file.data:
	        filename = secure_filename(form.upload_file.data.filename)
	        if os.path.isfile('app/' + ATACHMENT_UPLOAD_FOLDER + filename):
	            current_milli_time = lambda: int(round(time.time() * 1000))
	            filename = str(current_milli_time()) + filename
	        form.upload_file.data.save('app/' + ATACHMENT_UPLOAD_FOLDER + filename)
	        verification.filename = filename

        asset.description = form.description.data
        if request.method == 'POST':
            if request.form['submit'] == 'iterate':
                # Found who needs to work on the asset next
                current_user_found  = False
                in_hands_found = False
                if len(asset.clients.all()) != 1:
                    if len(asset.clients.all()) < 1:
                        flash('No clients for the asset.')
                        return redirect(url_for('index'))  
                    for client in asset.clients:
                        if client.id == g.user.id:
                            current_user_found = True
                        elif current_user_found == True:
                            asset.in_hands_id = client.id
                            in_hands_found = True
                            break

                if not in_hands_found:
                    if len(asset.suppliers.all()) < 1:
                        flash('No suppliers for the asset.')
                        return redirect(url_for('index'))    
                    asset.in_hands_id = asset.suppliers[0].id
                    asset.status = AssetStatus.description.value

	            flash('Verification created.')
	        elif request.form['submit'] == 'finalise':
	            asset.status = AssetStatus.finished.value
	            asset.finished = True
	            flash('Asset was marked as finalised.')
	        else:
	            pass # unknown

        db.session.add(verification)
        db.session.commit()
       
        return redirect(url_for('index'))
    # elif request.method != "POST":
    #     if verification is not None:
    #         form.name.data = verification.name
    #         form.duration.data = verification.duration
    #         form.pitch.data = verification.pitch
    #         form.sound_type = verification.sound_type
    #         form.sound_family = verification.sound_family
    return render_template('verify.html',
                            form=form,
                            asset=asset,
                            title='Verify asset')

@app.route('/iterate', methods=['GET', 'POST'])
@app.route('/iterate/<int:asset_id>/', methods=['GET', 'POST'])
@login_required
def iterate(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    # if g.user not in project.owners:
    #     flash('You do not have permissions to create milestones for this project.')
    #     return redirect(url_for('index'))
    # description = None
    # if description_id:
    #     description = Description.query.filter_by(id=description_id).first()

    form = IterationForm()
    if form.validate_on_submit():
        iteration = Iteration()
        iteration.description = form.description.data
        iteration.timestamp = datetime.now()
        iteration.asset_id = asset.id

        # Upload file
        if form.upload_file.data:
	        filename = secure_filename(form.upload_file.data.filename)
	        if os.path.isfile('app/' + ATACHMENT_UPLOAD_FOLDER + filename):
	            current_milli_time = lambda: int(round(time.time() * 1000))
	            filename = str(current_milli_time()) + filename
	        form.upload_file.data.save('app/' + ATACHMENT_UPLOAD_FOLDER + filename)
	        iteration.filename = filename

        asset.iteration_number = asset.iteration_number+1
        asset.description = form.description.data

        # Found who needs to work on the asset next
        current_user_found  = False
        in_hands_found = False
        if len(asset.suppliers.all()) != 1:
            if len(asset.suppliers.all()) < 1:
                flash('No suppliers for the asset.')
                return redirect(url_for('index'))  
            for supplier in asset.suppliers:
                if supplier.id == g.user.id:
                    current_user_found = True
                elif current_user_found == True:
                    asset.in_hands_id = supplier.id
                    in_hands_found = True
                    break

        if not in_hands_found:
            if len(asset.clients.all()) < 1:
                flash('No clients for the asset.')
                return redirect(url_for('index'))    
            asset.in_hands_id = asset.clients[0].id
            asset.status = AssetStatus.verification.value

        db.session.add(iteration)
        db.session.commit()
        
        flash('Iteration created.')
        return redirect(url_for('index'))
    # elif request.method != "POST":
    #     if description is not None:
    #         form.name.data = description.name
    #         form.duration.data = description.duration
    #         form.pitch.data = description.pitch
    #         form.sound_type = description.sound_type
    #         form.sound_family = description.sound_family
    return render_template('iterate.html',
                            form=form,
                            asset=asset,
                            title='Iterate asset')

# Create new project with status = iteration. Creation process also includes the first description stage.
@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if g.user.type == "supplier_user":
        flash('You do not have permissions to create new projects.')
        return redirect(url_for('index'))

    form = NewProjectForm()
    if form.validate_on_submit():
        project = Project()
        project.timestamp = datetime.now()
        project.name = form.name.data
        project.description = form.description.data
        project.finished = False
        
        # Upload file
        if form.upload_file.data.filename:
            filename = secure_filename(form.upload_file.data.filename)
            if os.path.isfile('app/' + ATACHMENT_UPLOAD_FOLDER + filename):
                current_milli_time = lambda: int(round(time.time() * 1000))
                filename = str(current_milli_time()) + filename
            form.upload_file.data.save('app/' + ATACHMENT_UPLOAD_FOLDER + filename)
            project.filename = filename

        db.session.add(project)
        db.session.commit()    
        
        flash('New project created.')
        return redirect(url_for('index'))
    return render_template('add_project.html',
                            form=form,
                            title='Add project')

@app.route('/projects/<string:projects_type>', methods=['GET', 'POST'])
@login_required
def projects(projects_type):
    if projects_type == 'ongoing':
        projects = Project.query.filter_by(finished=False).all()
    elif projects_type == 'finished':
        projects = Project.query.filter_by(finished=True).all()
    else:
        projects = Project.query.all()
    return render_template('projects.html',
                            projects=projects,
                            projects_type=projects_type)
@app.route('/project')
@app.route('/project/<int:project_id>/')
@login_required
def project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project is None:
        flash('Project not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('project.html',
                           project=project,
                           attachment_location=attachment_location)

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    tags_results = Tag.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    sounds_results = Sound.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    # users_results = User.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    users_results = []
    projects_results = Project.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    assets_results = Asset.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    
    print "query: " + query
    print "tags: " + str(tags_results)
    print "sounds: " + str(sounds_results)
    # print "users: " + str(users_results)
    print "projects: " + str(projects_results)
    print "assets: " + str(assets_results)

    return render_template('search_results.html',
                           query=query,
                           tags_results=tags_results,
                           sounds_results=sounds_results,
                           users_results=users_results,
                           projects_results=projects_results,
                           assets_results=assets_results)