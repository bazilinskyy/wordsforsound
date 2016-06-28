# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from datetime import datetime
from app import app, db, lm, oid
from .forms import DescriptionForm, NewAssetForm, AddTagForm, AddSoundForm, DeleteTagForm, DeleteSoundForm, VerificationForm, IterationForm, NewProjectForm, EditSoundForm
from .models import Description, Asset, Tag, Sound, AssetStatus, Iteration, Verification, Project, User
from .emails import follower_notification
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, ONGOING_PROJECTS_MENU, FINISHED_PROJECTS_MENU, ONGOING_ASSETS_MENU, FINISHED_ASSETS_MENU, SOUND_UPLOAD_FOLDER, ATACHMENT_UPLOAD_FOLDER, TAGS_FILE
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

# For horizontal menu
class HorizontalMenu():
    assets_ongoing = Asset.query.filter_by(finished=False).limit(ONGOING_ASSETS_MENU).all()
    assets_finished = Asset.query.filter_by(finished=True).limit(FINISHED_ASSETS_MENU).all()
    projects_ongoing = Project.query.filter_by(finished=False).limit(ONGOING_PROJECTS_MENU).all()
    projects_finished = Project.query.filter_by(finished=True).limit(FINISHED_PROJECTS_MENU).all()

    # THIS LISTS NEED TO BE USED WHENER MIGRATING DB
    # assets_ongoing = []
    # assets_finished = []
    # projects_ongoing = []
    # projects_finished = []

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
# @login_required
def index(page=1):
    # TODO Move to "in my hands" and "in other hands" with addition of accounts
    assets_description = Asset.query.filter_by(status=1).all() # TODO Add pagination
    assets_iteration = Asset.query.filter_by(status=2).all() # TODO Add pagination
    assets_verification = Asset.query.filter_by(status=3).all() # TODO Add pagination

    return render_template('index.html',
                           title='Home',
                           # assets_action=assets_action,
                           # assets_otherhands=assets_otherhands,
                           assets_description = assets_description,
                           assets_iteration = assets_iteration,
                           assets_verification = assets_verification,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

@app.route('/tags', methods=['GET', 'POST'])
def tags():
    tags = Tag.query.all()
    return render_template('tags.html',
                            tags=tags,
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)
@app.route('/tag')
@app.route('/tag/<int:tag_id>/')
def tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        flash(gettext('Tag not found.'))
        return redirect(url_for('index'))
    return render_template('tag.html',
                           tag=tag,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    form = AddTagForm()
    if form.validate_on_submit():
        # check if tag woth the same name exists
        tag = Tag.query.filter_by(name=form.name.data).first()
        if tag is not None:
            flash('This tag already exists.')
            return render_template('add_tag.html',
                            form=form,
                            title='Add tag',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)
        tag = Tag()
        tag.timestamp = datetime.now()
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()

        # for autofill for tags
        tags = Tag.query.all()
        tags_json = []
        if tags is not None:
	        for tag in tags:
		        tag_id = tag.id
		        tag_name = tag.name
		        tags_json.append({'value': tag_id, 'text' : tag_name})
	  	with open('app/' + TAGS_FILE, 'w') as outfile:
			json.dump(tags_json, outfile)  
        
        flash('New tag added.')
        return redirect(url_for('add_tag'))
    return render_template('add_tag.html',
                            form=form,
                            title='Add tag',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/delete_tag', methods=['GET', 'POST'])
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
                            title='Delete tag',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/sounds', methods=['GET', 'POST'])
def sounds():
    sounds = Sound.query.all()
    return render_template('sounds.html',
                            sounds=sounds,
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/sound', methods=['GET', 'POST'])
@app.route('/sound/<int:sound_id>/', methods=['GET', 'POST'])
def sound(sound_id):
    sound = Sound.query.filter_by(id=sound_id).first()
    if sound is None:
        flash(gettext('Sound not found.'))
        return redirect(url_for('index'))

    sound_location = SOUND_UPLOAD_FOLDER
    if sound.description == '':
    	sound.description = 'N/A'

    return render_template('sound.html',
                           sound=sound,
                           sound_location=sound_location,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

@app.route('/sound/edit', methods=['GET', 'POST'])
@app.route('/sound/<int:sound_id>/edit/', methods=['GET', 'POST'])
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
                           sound=sound,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

@app.route('/assets/<string:assets_type>', methods=['GET', 'POST'])
def assets(assets_type):
    if assets_type == 'ongoing':
        assets = Asset.query.filter_by(finished=False).all()
    elif assets_type == 'finished':
        assets = Asset.query.filter_by(finished=True).all()
    else:
        assets = Asset.query.all()
    return render_template('assets.html',
                            assets=assets,
                            assets_type=assets_type,
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)
@app.route('/asset')
@app.route('/asset/<int:asset_id>/')
def asset(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash('Asset not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('asset.html',
                           asset=asset,
                           attachment_location = attachment_location,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)


@app.route('/project/edit', methods=['GET', 'POST'])
@app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project is None:
        flash(gettext('Project not found.'))
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
def descriptions():
    descriptions = Description.query.all()
    return render_template('descriptions.html',
                            descriptions=descriptions,
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/description', methods=['GET', 'POST'])
@app.route('/description/<int:description_id>/', methods=['GET', 'POST'])
def description(description_id):
    description = Description.query.filter_by(id=description_id).first()
    if description is None:
        flash('Description not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('description.html',
                           description=description,
                           attachment_location=attachment_location,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

@app.route('/iterations', methods=['GET', 'POST'])
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
def iteration(iteration_id):
    iteration = Iteration.query.filter_by(id=iteration_id).first()
    if iteration is None:
        flash(gettext('Itteration not found.'))
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('iteration.html',
                           iteration=iteration,
                           attachment_location=attachment_location,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

@app.route('/verifications', methods=['GET', 'POST'])
def verifications():
    verifications = Verification.query.all()
    return render_template('verifications.html',
                            verifications=verifications,
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/verification', methods=['GET', 'POST'])
@app.route('/verification/<int:verification_id>/', methods=['GET', 'POST'])
def verification(verification_id):
    verification = Verification.query.filter_by(id=verification_id).first()
    if verification is None:
        flash('Verification not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('verification.html',
                           verification=verification,
                           attachment_location=attachment_location,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

@app.route('/add_sound', methods=['GET', 'POST'])
def add_sound():
    form = AddSoundForm()
    if form.validate_on_submit():
        # check if sound woth the same name exists
        sound = Sound.query.filter_by(name=form.name.data).first()
        if sound is not None:
            flash('Sound with the same name already exists.')
            return render_template('add_sound.html',
                            form=form,
                            title='Add sound',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)
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
                            filename=filename,
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/delete_sound', methods=['GET', 'POST'])
def delete_sound():
    form = DeleteSoundForm()
    if form.validate_on_submit():
        sound = Sound.query.filter_by(name=form.name.data).first()
        if sound == None:
            flash('Sound ' +  form.name.data + ' does not exist.')
            return redirect(url_for('delete_sound'))
    	  
        os.remove(os.path.join(SOUND_UPLOAD_FOLDER, sound.filename)) # delete uploaded file
        db.session.delete(sound)
        db.session.commit()  
        
        flash('Sound ' +  form.name.data + ' was deleted.')
        return redirect(url_for('delete_sound'))
    return render_template('delete_sound.html',
                            form=form,
                            title='Delete sound',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

# Create new asset with status = iteration. Creation process also includes the first description stage.
@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    form = NewAssetForm()
    if form.validate_on_submit():
        asset = Asset()
        asset.timestamp = datetime.now()
        asset.name = form.name.data
        asset.finished = False
        asset.status = AssetStatus.iteration.value
        asset.iteration_number = 0
        asset.description = form.description.data
        
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
                            title='Add asset',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/describe', methods=['GET', 'POST'])
@app.route('/describe/<int:asset_id>/', methods=['GET', 'POST'])
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
                            title='Describe asset',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/verify', methods=['GET', 'POST'])
@app.route('/verify/<int:asset_id>/', methods=['GET', 'POST'])
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
                            title='Verify asset',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/iterate', methods=['GET', 'POST'])
@app.route('/iterate/<int:asset_id>/', methods=['GET', 'POST'])
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
                            title='Iterate asset',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

# Create new project with status = iteration. Creation process also includes the first description stage.
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
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
                            title='Add project',
							              assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)

@app.route('/projects/<string:projects_type>', methods=['GET', 'POST'])
def projects(projects_type):
    if projects_type == 'ongoing':
        projects = Project.query.filter_by(finished=False).all()
    elif projects_type == 'finished':
        projects = Project.query.filter_by(finished=True).all()
    else:
        projects = Project.query.all()
    return render_template('projects.html',
                            projects=projects,
                            projects_type=projects_type,
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished,
                            projects_ongoing = HorizontalMenu.projects_ongoing,
                            projects_finished = HorizontalMenu.projects_finished)
@app.route('/project')
@app.route('/project/<int:project_id>/')
def project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project is None:
        flash('Project not found.')
        return redirect(url_for('index'))
    attachment_location = ATACHMENT_UPLOAD_FOLDER
    return render_template('project.html',
                           project=project,
                           attachment_location = attachment_location,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'],
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)

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
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        # make the user follow him/herself
        db.session.add(user.follow(user))
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


@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                           user=user,
                           posts=posts,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished,
                           projects_ongoing = HorizontalMenu.projects_ongoing,
                           projects_finished = HorizontalMenu.projects_finished)
