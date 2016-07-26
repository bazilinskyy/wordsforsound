# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from __future__ import division
from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.paginate import Pagination
from flask.ext.mail import Message
from datetime import datetime
from app import app, db, lm, mail
from .forms import DescriptionForm, NewAssetForm, AddTagForm, AddSoundForm, DeleteTagForm, DeleteSoundForm, \
    VerificationForm, IterationForm, NewProjectForm, EditSoundForm, LoginForm, PasswordForm, EmailForm, \
    RegisterForm, SearchForm, EditUserForm, EditAssetForm, EditTagForm
from .models import Description, Asset, Tag, Sound, AssetStatus, Iteration, Verification, Project, User, \
    SupplierUser, ClientUser
from .emails import description_notification, iteration_notification, verification_notification
from .util import ts
from config import SOUNDS_PER_PAGE, MAX_SEARCH_RESULTS, ONGOING_PROJECTS_MENU, FINISHED_PROJECTS_MENU, \
    ONGOING_ASSETS_MENU, FINISHED_ASSETS_MENU, SOUND_UPLOAD_FOLDER, ATTACHMENT_UPLOAD_FOLDER, TAGS_FILE, \
    TAGS_PER_PAGE, ASSETS_PER_PAGE, DATABASE_QUERY_TIMEOUT, PROJECTS_PER_PAGE, SOUNDS_FILE, AVATAR_UPLOAD_FOLDER
from werkzeug import secure_filename
from flask_wtf.file import FileField
import os
import time
import json
import boto3
import markdown

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
    g.user = current_user
    if not app.debug and g.user.is_authenticated and "/static/" not in str(request.url):
        app.logger.info("USER %s visited URL %s" % (str(g.user.nickname), str(request.url)))
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
def login():
    session.pop('_flashes', None)
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
      if form.validate_on_submit():
          user = User.query.filter_by(nickname=form.username.data).first()
          if user is not None and user.password == form.password.data:
              login_user(user)
              session['remember_me'] = form.remember_me.data
              return redirect(url_for('index'))
          else:
              flash('Invalid username or password.')
    return render_template('login.html', form=form, title='Login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user.is_authenticated:
        flash('Please logout first.')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if provided email is not used by another
        user_email = User.query.filter_by(email=form.email.data).first()
        user_nickname = User.query.filter_by(nickname=form.nickname.data).first()
        if user_email is not None or user_nickname is not None:
            # flash('Email ' + form.email.data + ' is used in another account. Please use another one.')
            pass
        else:
            if form.user_type.data == '1':
                user = ClientUser(
                    nickname=form.nickname.data,
                    email=form.email.data,
                    password=form.password.data,
                    receive_emails=True
                )
            else:
                user = SupplierUser(
                    nickname=form.nickname.data,
                    email=form.email.data,
                    password=form.password.data,
                    receive_emails=True
                )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Register')

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

            subject="Password reset requested"
            sender="wordsforsound@gmail.com"
            recipients=user.email
            txt = "Please click on {{ recover_url }} to recover your password. Thank you!"
            html = "Please click on {{ recover_url }} to recover your password. Thank you!"

            send_email(subject, sender, recipients, txt, html)

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
    return render_template('user.html',
                           page=page,
                           user=user,
                           user_assets=user_assets)


@app.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        g.user.first_name = form.first_name.data
        g.user.last_name = form.last_name.data
        g.user.receive_emails = form.receive_emails.data
        g.user.email = form.email.data

        if not os.environ.get('HEROKU'):
          if form.upload_file.data.filename:
            filename = secure_filename(form.upload_file.data.filename)
            if os.path.isfile('app/' + AVATAR_UPLOAD_FOLDER + filename):
                current_milli_time = lambda: int(round(time.time() * 1000))
                filename = str(current_milli_time()) + filename
            form.upload_file.data.save('app/' + AVATAR_UPLOAD_FOLDER + filename)
            g.user.avatar_filename = filename
        else:
          g.user.avatar_filename = form.upload_file.data.filename

        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_user'))
    elif request.method != "POST":
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        form.first_name.data = g.user.first_name 
        form.last_name.data = g.user.last_name
        form.receive_emails.data = g.user.receive_emails
        form.upload_file.data = g.user.avatar_filename
        form.email.data = g.user.email
    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    return render_template('edit_user.html',
        form=form,
        heroku_state=heroku_state)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page_description>/<int:page_iteration>/<int:page_verification>/<int:page_otherhands>', methods=['GET', 'POST'])
@login_required
def index(page_description=1, page_iteration=1, page_verification=1, page_otherhands=1):
    assets_description = Asset.query.join(User).filter(Asset.in_hands_id == g.user.id).filter(Asset.status == 1).paginate(page_verification, ASSETS_PER_PAGE, False)
    assets_iteration = Asset.query.join(User).filter(Asset.in_hands_id == g.user.id).filter(Asset.status == 2).paginate(page_verification, ASSETS_PER_PAGE, False)
    assets_verification = Asset.query.join(User).filter(Asset.in_hands_id == g.user.id).filter(Asset.status == 3).paginate(page_verification, ASSETS_PER_PAGE, False)
    if g.user.type == "client_user":
        assets_otherhands = Asset.query.filter(Asset.in_hands_id != g.user.id).filter(Asset.finished != True).filter(Asset.clients.contains(g.user)).filter(Asset.clients.contains(g.user)).paginate(page_otherhands, ASSETS_PER_PAGE, False)
    else:
        assets_otherhands = Asset.query.filter(Asset.in_hands_id != g.user.id).filter(Asset.finished != True).filter(Asset.clients.contains(g.user)).filter(Asset.suppliers.contains(g.user)).paginate(page_otherhands, ASSETS_PER_PAGE, False)

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

@app.route('/tags', methods=['GET', 'OPST'])
@app.route('/tags/<int:page>', methods=['GET', 'POST'])
@login_required
def tags(page=1):
    tags = Tag.query.order_by(Tag.name.asc()).all()
    return render_template('tags.html',
                            title='Tags',
                            tags=tags)
@app.route('/tag')
@app.route('/tag/<int:tag_id>/')
@login_required
def tag(tag_id=0, page=1):
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        flash('Tag not found.')
        return redirect(url_for('index'))
    sounds = tag.sounds.paginate(page, SOUNDS_PER_PAGE, False)
    return render_template('tag.html',
                           title='Tag',
                           tag=tag,
                           page=page,
                           sounds=sounds,
                           sound_location=SOUND_UPLOAD_FOLDER)

@app.route('/add_tag', methods=['GET', 'POST'])
@login_required
def add_tag():
    form = AddTagForm()
    if form.validate_on_submit():
        # check if tag woth the same name exists
        tag = Tag.query.filter_by(name=form.name.data).first()
        if tag is not None:
            flash('Tag with the same name already exists.')
            return render_template('add_tag.html',
                            form=form,
                            title='Add tag')
        tag = Tag()
        tag.timestamp = datetime.now()
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()
        update_tags_json() # For autofill for tags and tag cloud
        
        flash('New tag added.')
        return redirect(url_for('add_tag'))
    return render_template('add_tag.html',
                            form=form,
                            title='Add tag')

@app.route('/tag/edit', methods=['GET', 'POST'])
@app.route('/tag/<int:tag_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    form = EditTagForm()
    if form.validate_on_submit():
        # check if tag woth the same name exists
        tag = Tag.query.filter_by(name=form.name.data).first()
        if tag is not None:
            flash('Tag with the same name already exists.')
            return render_template('edit_tag.html',
                            form=form,
                            title='Edit tag')
        tag = Tag()
        tag.name = form.name.data
        tag.timestamp = datetime.now()
        db.session.add(tag)
        db.session.commit()
        update_tags_json() # For autofill for tags and tag cloud
        
        flash('Tag was edited successfully.')
        return redirect(url_for('tag', tag_id=tag_id))
    elif request.method != "POST":
        if tag is not None:
            form.name.data = tag.name
    return render_template('edit_tag.html',
                            form=form,
                            tag=tag,
                            title='Edit tag')

@app.route('/delete_tag', methods=['GET', 'POST'])
@app.route('/tag/<int:tag_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_tag(tag_id=0):
    form = DeleteSoundForm()
    if form.validate_on_submit() or tag_id > 0:
        if form.validate_on_submit():
            tag = Tag.query.filter_by(name=form.name.data).first()
        else:
            tag = Tag.query.filter_by(id=tag_id).first()
        
        if tag == None:
            if form.validate_on_submit():
                flash('Tag ' +  form.name.data + ' does not exist.')
            else:
                flash('Tag with ID ' +  str(tag_id) + ' does not exist.')
            return redirect(url_for('delete_tag'))
        
        db.session.delete(tag)
        db.session.commit()

        update_tags_json()  # for autofill for tags
        
        flash('Tag ' +  tag.name + ' was deleted.')
        return redirect(url_for('tags'))
    return render_template('delete_tag.html',
                            form=form,
                            title='Delete tag')

@app.route('/assets', methods=['GET', 'POST'])
@app.route('/assets/<string:assets_type>', methods=['GET', 'POST'])
@app.route('/assets/<string:assets_type>/<int:page>', methods=['GET', 'POST'])
@login_required
def assets(assets_type="all", page=1):
    search = False
    q = request.args.get('q')
    if q:
        search = True

    if assets_type == 'ongoing':
        assets = Asset.query.filter_by(finished=False).paginate(page, ASSETS_PER_PAGE, False)
        total_count = len(Asset.query.filter_by(finished=False).all())
    elif assets_type == 'finished':
        assets = Asset.query.filter_by(finished=True).paginate(page, ASSETS_PER_PAGE, False)
        total_count = len(Asset.query.filter_by(finished=True).all())
    else:
        assets = Asset.query.paginate(page, ASSETS_PER_PAGE, False)
        total_count = len(Asset.query.all())
    pagination = Pagination(page=page,
                            per_page=ASSETS_PER_PAGE,
                            total=total_count,
                            search=search,
                            record_name='assets',
                            css_framework='foundation')
    return render_template('assets.html',
                            assets=assets,
                            assets_type=assets_type,
                            pagination=pagination)

@app.route('/asset')
@app.route('/asset/<int:asset_id>/')
@login_required
def asset(asset_id=0):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    attachment_location = ATTACHMENT_UPLOAD_FOLDER
    sound_location = SOUND_UPLOAD_FOLDER
    return render_template('asset.html',
                           asset=asset,
                           attachment_location = attachment_location,
                           sound_location=sound_location)


@app.route('/project/edit', methods=['GET', 'POST'])
@app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    if g.user.type == "supplier_user":
        flash('You do not have permissions to edit projects.')
        return redirect(url_for('index'))

    project = Project.query.filter_by(id=project_id).first()
    if project is None:
        flash('Project not found.')
        return redirect(url_for('index'))
    if project.finished is True:
        flash('Finished project cannot be edited.')
        return redirect(url_for('index'))
    form = NewProjectForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            if request.form['submit'] == 'edit':
                # check if tag woth the same name exists
                project = Project.query.filter_by(name=form.name.data).first()
                if project is not None:
                    flash('Project with the same name already exists.')
                    return render_template('edit_project.html',
                                    form=form,
                                    project=project,
                                    title='Edit project')
                project.timestamp = datetime.now()
                project.name = form.name.data
                project.description = form.description.data

                # Upload file
                if not os.environ.get('HEROKU'):
                  if form.upload_file.data.filename:
                    filename = secure_filename(form.upload_file.data.filename)
                    if os.path.isfile('app/' + ATTACHMENT_UPLOAD_FOLDER + filename):
                        current_milli_time = lambda: int(round(time.time() * 1000))
                        filename = str(current_milli_time()) + filename
                    form.upload_file.data.save('app/' + ATTACHMENT_UPLOAD_FOLDER + filename)
                    project.filename = filename
                else:
                  project.filename = form.upload_file.data.filename

                flash('Project was edited successfully.')

            elif request.form['submit'] == 'finalise':
              project.finished = True
              for asset in project.assets:
                asset.finished = True
              flash('Project and assets in project were marked as finished.')

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
    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    return render_template('edit_project.html',
                            form=form,
                            title='Edit project',
                            project=project,
                            heroku_state=heroku_state)

@app.route('/descriptions', methods=['GET', 'POST'])
@login_required
def descriptions():
    descriptions = Description.query.all()
    return render_template('descriptions.html',
                            descriptions=descriptions)

@app.route('/description', methods=['GET', 'POST'])
@app.route('/description/<int:description_id>/', methods=['GET', 'POST'])
@login_required
def description(description_id=0):
    description = Description.query.filter_by(id=description_id).first()
    if description is None:
        flash('Description not found.')
        return redirect(url_for('index'))
    attachment_location = ATTACHMENT_UPLOAD_FOLDER
    sound_location = SOUND_UPLOAD_FOLDER

    # Check if attachment is a videofile
    attachment_is_video = False
    if description.filename is not None:
        attachment_is_video = check_if_video(description.filename)

    return render_template('description.html',
                           description=description,
                           attachment_location=attachment_location,
                           sound_location=sound_location,
                           attachment_is_video=attachment_is_video)

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
def iteration(iteration_id=0):
    iteration = Iteration.query.filter_by(id=iteration_id).first()
    if iteration is None:
        flash('Itteration not found.')
        return redirect(url_for('index'))
    sound_location = SOUND_UPLOAD_FOLDER
    return render_template('iteration.html',
                           iteration=iteration,
                           sound_location=sound_location)

@app.route('/verifications', methods=['GET', 'POST'])
@login_required
def verifications():
    verifications = Verification.query.all()
    return render_template('verifications.html',
                            verifications=verifications)

@app.route('/verification', methods=['GET', 'POST'])
@app.route('/verification/<int:verification_id>/', methods=['GET', 'POST'])
@login_required
def verification(verification_id=0):
    verification = Verification.query.filter_by(id=verification_id).first()
    if verification is None:
        flash('Verification not found.')
        return redirect(url_for('index'))
    attachment_location = ATTACHMENT_UPLOAD_FOLDER
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

        update_sounds_json()  # for autofill for sounds
        update_tags_json()  # for autofill for sounds

        # Upload file
        if not os.environ.get('HEROKU'):
            filename = secure_filename(form.upload_file.data.filename)
            if os.path.isfile('app/' + SOUND_UPLOAD_FOLDER + filename):
                current_milli_time = lambda: int(round(time.time() * 1000))
                filename = str(current_milli_time()) + filename
            form.upload_file.data.save('app/' + SOUND_UPLOAD_FOLDER + filename)
            sound.filename = filename
        else:
            sound.filename = form.upload_file.data.filename

        db.session.add(sound)
        db.session.commit()

        # Upate json files for autofill
        update_sounds_json()
        update_tags_json()
        
        flash('New sound added.')
        return redirect(url_for('add_sound'))
    filename = None
    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    return render_template('add_sound.html',
                            form=form,
                            title='Add sound',
                            filename=filename,
                            heroku_state=heroku_state)

@app.route('/delete_sound', methods=['GET', 'POST'])
@app.route('/sound/<int:sound_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_sound(sound_id=0):
    form = DeleteSoundForm()
    if form.validate_on_submit() or sound_id > 0:
        if form.validate_on_submit():
            sound = Sound.query.filter_by(name=form.name.data).first()
        else:
            sound = Sound.query.filter_by(id=sound_id).first()

        if sound == None:
            if form.validate_on_submit():
                flash('Sound ' +  form.name.data + ' does not exist.')
            else:
                flash('Sound with ID ' +  str(sound_id) + ' does not exist.')
            return redirect(url_for('delete_sound'))
        if not os.environ.get('HEROKU'):
            try:
                # Removed file stored locally
                os.remove(os.path.join(SOUND_UPLOAD_FOLDER, sound.filename)) # delete uploaded file
            except OSError:
                app.logger.error("Could not delete file %s." % str(sound.filename))
        else:
            # Remove file stored in Heroku
            try:
                s3 = boto3.resource('s3')
                s3.Object(os.environ.get('S3_BUCKET_SOUNDS'), sound.filename).delete()
            except:
                app.logger.error("Could not delete file %s from Heroku." % str(sound.filename))

        db.session.delete(sound)
        db.session.commit()  

        update_sounds_json()  # for autofill for sounds
        update_tags_json()  # for autofill for sounds

        flash('Sound ' +  sound.name + ' was deleted.')
        return redirect(url_for('sounds'))
    return render_template('delete_sound.html',
                            form=form,
                            title='Delete sound')

@app.route('/sounds', methods=['GET', 'POST'])
@app.route('/sounds/<int:page>', methods=['GET', 'POST'])
@login_required
def sounds(page=1):
    search = False
    q = request.args.get('q')
    if q:
        search = True

    sounds = Sound.query.order_by(Sound.timestamp.desc()).paginate(page, SOUNDS_PER_PAGE, False)
    total_count = len(Sound.query.all())
    pagination = Pagination(page=page,
                            per_page=5,
                            total=len(sounds.items),
                            search=search,
                            css_framework='foundation')
    return render_template('sounds.html',
                            sounds=sounds,
                            pagination=pagination,
                            sound_location=SOUND_UPLOAD_FOLDER)

@app.route('/sound', methods=['GET', 'POST'])
@app.route('/sound/<int:sound_id>/', methods=['GET', 'POST'])
@login_required
def sound(sound_id=0):
    print sound_id
    sound = Sound.query.filter_by(id=sound_id).first()
    if sound is None:
        flash('Sound not found.')
        return redirect(url_for('index'))

    if sound.description == '':
        sound.description = 'N/A'

    return render_template('sound.html',
                           sound=sound,
                           sound_location=SOUND_UPLOAD_FOLDER)

@app.route('/sound/edit', methods=['GET', 'POST'])
@app.route('/sound/<int:sound_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_sound(sound_id):
    sound = Sound.query.filter_by(id=sound_id).first()
    form = EditSoundForm()
    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0

    if form.validate_on_submit():
        # check if sound woth the same name exists
        sound = Sound.query.filter_by(name=form.name.data).first()
        if sound is not None:
            flash('Sound with the same name already exists.')
            return render_template('edit_sound.html',
                            form=form,
                            sound=sound,
                            title='Edit sound',
                            heroku_state=heroku_state)
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
        if not os.environ.get('HEROKU'):
            filename = secure_filename(form.upload_file.data.filename)
            if os.path.isfile('app/' + SOUND_UPLOAD_FOLDER + filename):
                current_milli_time = lambda: int(round(time.time() * 1000))
                filename = str(current_milli_time()) + filename
            form.upload_file.data.save('app/' + SOUND_UPLOAD_FOLDER + filename)
            sound.filename = filename
        else:
            sound.filename = form.upload_file.data.filename

        db.session.commit()
        
        flash('Sound was edited successfully.')
        return redirect(url_for('sound', sound_id=sound_id))

    elif request.method != "POST":
        if sound is not None:
            form.name.data = sound.name
            form.description.data = sound.description
            form.sound_type.data = sound.sound_type
            form.sound_family.data = sound.sound_family
            form.rights.data = sound.rights
            form.upload_file.data = sound.filename
    return render_template('edit_sound.html',
                           form=form,
                           title='Edit sound',
                           sound=sound,
                           heroku_state=heroku_state)

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
    if len(projects) == 0:
        flash('You need to create at least one project before adding assets.')
        return redirect(url_for('index'))
    project_choices = []
    for project in projects:
        project_choices.append((str(project.id), project.name))
    form.project.choices = project_choices
    # List of users as clients for new assets
    clients = ClientUser.query.all()
    if len(clients) == 0:
        flash('You need have at least one client user before adding assets.')
        return redirect(url_for('index'))
    clients_choices = []
    for client in clients:
        clients_choices.append((str(client.id), client.nickname + ' : ' + client.full_name))
    form.clients.choices =clients_choices
    # List of users as suppliers for new assets
    suppliers = SupplierUser.query.all()
    if len(suppliers) == 0:
        flash('You need have at least one supplier user before adding assets.')
        return redirect(url_for('index'))
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
        asset.notify_by_email = form.notify_by_email.data
        asset.project_id = form.project.data
        asset.user_id = g.user.id
        for client in form.clients.data:
            asset.client_add(ClientUser.query.filter_by(id=int(client)).first())
        for supplier in form.suppliers.data:
            asset.supplier_add(SupplierUser.query.filter_by(id=int(supplier)).first())
        asset.init_in_hands()

        db.session.add(asset)

        description = Description()
        description.description = form.description.data
        description.duration = form.duration.data
        description.pitch = form.pitch.data
        description.sound_type = form.sound_type.data
        description.sound_family = form.sound_family.data
        description.timestamp = datetime.now()
        description.asset_id = asset.id
        description.user_id = g.user.id

        # Upload file
        if not os.environ.get('HEROKU'):
            if form.upload_file.data.filename:
                filename = secure_filename(form.upload_file.data.filename)
                if os.path.isfile('app/' + ATTACHMENT_UPLOAD_FOLDER + filename):
                    current_milli_time = lambda: int(round(time.time() * 1000))
                    filename = str(current_milli_time()) + filename
                form.upload_file.data.save('app/' + ATTACHMENT_UPLOAD_FOLDER + filename)
                asset.filename = filename
                description.filename = filename
        else:
            asset.filename = form.upload_file.data.filename
            description.filename = form.upload_file.data.filename

        # Change tags
        for tag in form.tags.data:
            if tag != ',':
                description.tags.append(Tag.query.filter_by(id=int(tag)).first())

        # Change sounds
        for sound in form.sounds.data:
            if sound != ',':
                description.sounds.append(Sound.query.filter_by(id=int(sound)).first())

        db.session.add(description)
        db.session.commit()
        
        description_notification(asset.user_in_hands, asset)
        flash('New asset description created.')
        return redirect(url_for('index'))
    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    return render_template('add_asset.html',
                            form=form,
                            title='Add asset',
                            heroku_state=heroku_state)

@app.route('/asset/edit', methods=['GET', 'POST'])
@app.route('/asset/<int:asset_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_asset(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    if asset.finished is True:
        flash('Finished asset cannot be edited.')
        return redirect(url_for('index'))
    form = EditAssetForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            if request.form['submit'] == 'edit':
              asset.timestamp = datetime.now()
              asset.name = form.name.data
              asset.description = form.description.data
              
              # Upload file
              if not os.environ.get('HEROKU'):
                  if form.upload_file.data.filename:
                    filename = secure_filename(form.upload_file.data.filename)
                    if os.path.isfile('app/' + ATTACHMENT_UPLOAD_FOLDER + filename):
                        current_milli_time = lambda: int(round(time.time() * 1000))
                        filename = str(current_milli_time()) + filename
                    form.upload_file.data.save('app/' + ATTACHMENT_UPLOAD_FOLDER + filename)
                    asset.filename = filename
              else:
                  asset.filename = form.upload_file.data.filename

              flash('Asset was edited successfully.')

            elif request.form['submit'] == 'finalise':
              asset.finished = True
              flash('Asset was marked as finished.')

            else:
              flash('Unknown status.')
              pass # unknown

        update_tags_json()

        db.session.add(asset)
        db.session.commit()    
        
        return redirect(url_for('asset', asset_id=asset_id))

    elif request.method != "POST":
        if asset is not None:
          form.name.data = asset.name
          form.description.data = asset.description

    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    return render_template('edit_asset.html',
                            form=form,
                            title='Edit asset',
                            asset=asset,
                            heroku_state=heroku_state)

@app.route('/describe', methods=['GET', 'POST'])
@app.route('/describe/<int:asset_id>/', methods=['GET', 'POST'])
@login_required
def describe(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    if asset.user_in_hands.id != g.user.id:
        flash('You do not have permissions to work on this asset at this moment.')
        return redirect(url_for('index'))

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
        description.user_id = g.user.id

        # Find who needs to work on the asset next
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
        if not os.environ.get('HEROKU'):
            if form.upload_file.data:
    	        filename = secure_filename(form.upload_file.data.filename)
    	        if os.path.isfile('app/' + ATTACHMENT_UPLOAD_FOLDER + filename):
    	            current_milli_time = lambda: int(round(time.time() * 1000))
    	            filename = str(current_milli_time()) + filename
    	        form.upload_file.data.save('app/' + ATTACHMENT_UPLOAD_FOLDER + filename)
    	        description.filename = filename
        else:
            description.filename = form.upload_file.data.filename

        # Add tags
        description.tags = []
        for tag in form.tags.data:
            if tag != ',':
                description.tags.append(Tag.query.filter_by(id=int(tag)).first())

        # Add sounds
        description.sounds = []
        for sound in form.sounds.data:
            if sound != ',':
                description.sounds.append(Sound.query.filter_by(id=int(sound)).first())

        db.session.add(description)
        db.session.commit()
        
        description_notification(asset.user_in_hands, asset)
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

    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    return render_template('describe.html',
                            form=form,
                            asset=asset,
                            verification=asset.get_last_verification(),
                            title='Describe asset',
                            heroku_state=heroku_state)

@app.route('/verify', methods=['GET', 'POST'])
@app.route('/verify/<int:asset_id>/', methods=['GET', 'POST'])
@login_required
def verify(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    if asset.user_in_hands.id != g.user.id:
        flash('You do not have permissions to work on this asset at this moment.')
        return redirect(url_for('index'))

    form = VerificationForm()
    if form.validate_on_submit():
        # get asset similar to project_id 
        verification = Verification()
        verification.description = form.description.data
        verification.timestamp = datetime.now()
        verification.asset_id = asset.id
        verification.user_id = g.user.id

        # Upload file
        if not os.environ.get('HEROKU'):
            if form.upload_file.data:
    	        filename = secure_filename(form.upload_file.data.filename)
    	        if os.path.isfile('app/' + ATTACHMENT_UPLOAD_FOLDER + filename):
    	            current_milli_time = lambda: int(round(time.time() * 1000))
    	            filename = str(current_milli_time()) + filename
    	        form.upload_file.data.save('app/' + ATTACHMENT_UPLOAD_FOLDER + filename)
    	        verification.filename = filename
        else:
            verification.filename = form.upload_file.data.filename

        if request.method == 'POST':
            if request.form['submit'] == 'iterate':
                # Find who needs to work on the asset next
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
                    asset.status = AssetStatus.description.value

                    verification_notification(asset.user_in_hands, asset)
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
    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    return render_template('verify.html',
                            form=form,
                            asset=asset,
                            iteration=asset.get_last_iteration(),
                            attachment_location=SOUND_UPLOAD_FOLDER,
                            title='Verify asset',
                            heroku_state=heroku_state)

@app.route('/iterate', methods=['GET', 'POST'])
@app.route('/iterate/<int:asset_id>/', methods=['GET', 'POST'])
@login_required
def iterate(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    if asset.user_in_hands.id != g.user.id:
        flash('You do not have permissions to work on this asset at this moment.')
        return redirect(url_for('index'))

    form = IterationForm()
    if form.validate_on_submit():
        iteration = Iteration()
        iteration.description = form.description.data
        iteration.timestamp = datetime.now()
        iteration.asset_id = asset.id
        iteration.user_id = g.user.id
        asset.iteration_number = asset.iteration_number+1
        
        # Upload file
        sound = Sound()
        sound.timestamp = datetime.now()
        sound.name = "Asset-" + str(asset.id) + "_ver-" + str(asset.iteration_number)
        sound.description = "Iteration for asset " + str(asset.id) + " ver. " \
            + str(asset.iteration_number) + "."
        if not os.environ.get('HEROKU'):
            if form.upload_file.data:
    	        filename = secure_filename(form.upload_file.data.filename)
    	        if os.path.isfile('app/' + SOUND_UPLOAD_FOLDER + filename):
    	            current_milli_time = lambda: int(round(time.time() * 1000))
    	            filename = str(current_milli_time()) + filename
    	        form.upload_file.data.save('app/' + SOUND_UPLOAD_FOLDER + filename)
    	        iteration.filename = filename
                sound.filename = filename
        else:
            iteration.filename = form.upload_file.data.filename
            sound.filename = form.upload_file.data.filename
        db.session.add(sound)

        # Find who needs to work on the asset next
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
        
        iteration_notification(asset.user_in_hands, asset)
        flash('Iteration created.')
        return redirect(url_for('index'))
    description = asset.get_last_description()
    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    return render_template('iterate.html',
                            form=form,
                            asset=asset,
                            description=description,
                            title='Iterate asset',
                            heroku_state=heroku_state)

# Create new project with status = iteration. Creation process also includes the first description stage.
@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if g.user.type == "supplier_user":
        flash('You do not have permissions to create new projects.')
        return redirect(url_for('index'))
    if os.environ.get('HEROKU'):
        heroku_state = 1
    else:
        heroku_state = 0
    form = NewProjectForm()
    if form.validate_on_submit():
        # check if tag woth the same name exists
        project = Project.query.filter_by(name=form.name.data).first()
        if project is not None:
            flash('Project with such name already exists.')
            return render_template('add_project.html',
                            form=form,
                            title='Add project',
                            heroku_state=heroku_state)
        project = Project()
        project.timestamp = datetime.now()
        project.name = form.name.data
        project.description = form.description.data
        project.finished = False
        
        # Upload file
        if not os.environ.get('HEROKU'):
            if form.upload_file.data.filename:
                filename = secure_filename(form.upload_file.data.filename)
                if os.path.isfile('app/' + ATTACHMENT_UPLOAD_FOLDER + filename):
                    current_milli_time = lambda: int(round(time.time() * 1000))
                    filename = str(current_milli_time()) + filename
                form.upload_file.data.save('app/' + ATTACHMENT_UPLOAD_FOLDER + filename)
                project.filename = filename
        else:
            project.filename = form.upload_file.data.filename

        db.session.add(project)
        db.session.commit()    
        
        flash('New project created.')
        return redirect(url_for('index'))
    return render_template('add_project.html',
                            form=form,
                            title='Add project',
                            heroku_state=heroku_state)

@app.route('/projects/<string:projects_type>', methods=['GET', 'POST'])
@app.route('/projects/<string:projects_type>/<int:page>', methods=['GET', 'POST'])
@login_required
def projects(projects_type, page=1):
    if projects_type == 'ongoing':
        projects = Project.query.filter_by(finished=False).paginate(page, PROJECTS_PER_PAGE, False)
    elif projects_type == 'finished':
        projects = Project.query.filter_by(finished=True).paginate(page, PROJECTS_PER_PAGE, False)
    else:
        projects = Project.query.paginate(page, PROJECTS_PER_PAGE, False)
    return render_template('projects.html',
                            projects=projects,
                            projects_type=projects_type,
                            page=page)
@app.route('/project')
@app.route('/project/<int:project_id>/')
@login_required
def project(project_id=0):
    project = Project.query.filter_by(id=project_id).first()
    if project is None:
        flash('Project not found.')
        return redirect(url_for('index'))
    attachment_location = ATTACHMENT_UPLOAD_FOLDER
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

    return render_template('search_results.html',
                           query=query,
                           tags_results=tags_results,
                           sounds_results=sounds_results,
                           users_results=users_results,
                           projects_results=projects_results,
                           assets_results=assets_results,
                           sound_location=SOUND_UPLOAD_FOLDER)

@app.route('/readme', methods=["GET", "POST"])
def readme():
    with open('README.md', 'r') as myfile:
        readme_content=myfile.read()
    readme_content = Markup(markdown.markdown(readme_content))
    return render_template('readme.html',
        readme_content=readme_content)

# For autofill for tags and tag cloud
def update_tags_json():
    tags = Tag.query.all()
    tags_json = []
    if tags is not None:
        for tag in tags:
            tag_id = tag.id
            tag_name = tag.name
            # tag_weight = tag.sounds.count() / max_number_of_sounds # weight for jQuery
            tag_weight = tag.sounds.count()
            tag_link = "tag/" + str(tag.id)
            tags_json.append({'value': tag_id, 'text' : tag_name, 'weight' : tag_weight, 'link' : tag_link})
            with open('app/' + TAGS_FILE, 'w') as outfile:
                json.dump(tags_json, outfile)

# For autofill for sounds
def update_sounds_json():
    sounds = Sound.query.all()
    sounds_json = []
    if sounds is not None:
        for sound in sounds:
            sound_id = sound.id
            sound_name = sound.name
            sound_link = "sound/" + str(sound.id)
            sounds_json.append({'value': sound_id, 'text' : sound_name, 'link' : sound_link})
            with open('app/' + SOUNDS_FILE, 'w') as outfile:
                json.dump(sounds_json, outfile)

# Listen for GET requests for S3
@app.route('/sign-s3/<type>')
def sign_s3(type):
    # Load necessary information into the application
    if type == "sound":
        S3_BUCKET = os.environ.get('S3_BUCKET_SOUNDS')
    elif type == "attachment":
        S3_BUCKET = os.environ.get('S3_BUCKET_ATTACHMENTS')
    elif type == "image":
        S3_BUCKET = os.environ.get('S3_BUCKET_IMAGES')
    else:
        S3_BUCKET = "N/A"   

    # Load required data from the request
    file_name = request.args.get('file-name')
    file_type = request.args.get('file-type')

    # Initialise the S3 client
    s3 = boto3.client('s3')

    # Generate and return the presigned URL
    presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
    )

    # Return the data to the client
    return json.dumps({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })

def check_if_video(filename):
    if filename.lower().endswith(('.avi', '.mpeg', '.mp4')):
        return True
    return False