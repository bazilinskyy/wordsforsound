# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from datetime import datetime
from app import app, db, lm, oid
from .forms import DescriptionForm, NewAssetForm, AddTagForm, AddSoundForm, DeleteTagForm, DeleteSoundForm
from .models import Description, Asset, Tag, Sound
from .emails import follower_notification
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, ONGOING_PROJECTS_MENU, FINISHED_PROJECTS_MENU

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
    assets_ongoing = Asset.query.filter_by(finished=False).limit(ONGOING_PROJECTS_MENU).all()
    assets_finished = Asset.query.filter_by(finished=True).limit(FINISHED_PROJECTS_MENU).all()

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
    assets_action = [  # fake array of assets
        { 
            'name': "Asset 1",
            'avatar': "http://gravatar.com/avatar/b50f24a5349355a5ce3845f2d1e1cf7e?s=60&d=identicon",
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et',
            'active': 1,
            'iteration': 500
        },
        { 
            'name': "Asset 2",
            'avatar': "http://gravatar.com/avatar/443f3a0d245fa5200c43182325937f2c?s=60&d=identicon",
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et',
            'active': 2,
            'iteration': 2
        },
        { 
            'name': "Asset 4",
            'avatar': "http://gravatar.com/avatar/b50f24a5349355a5ce3845f2d1e1cf7e?s=60&d=identicon",
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et',
            'active': 1,
            'iteration': 7
        },
    ]
    assets_otherhands = [  # fake array of assets
        { 
            'name': "Asset 5",
            'avatar': "http://gravatar.com/avatar/b50f24a5349355a5ce3845f2d1e1cf7e?s=60&d=identicon",
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et',
            'active': 0,
            'iteration': 5
        },
        { 
            'name': "Asset 3",
            'avatar': "http://gravatar.com/avatar/443f3a0d245fa5200c43182325937f2c?s=60&d=identicon",
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et',
            'active': 0,
            'iteration': 2
        },
        { 
            'name': "Asset 6",
            'avatar': "http://gravatar.com/avatar/443f3a0d245fa5200c43182325937f2c?s=60&d=identicon",
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et',
            'active': 0,
            'iteration': 21
        },
        { 
            'name': "Asset 7",
            'avatar': "http://gravatar.com/avatar/b50f24a5349355a5ce3845f2d1e1cf7e?s=60&d=identicon",
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et',
            'active': 0,
            'iteration': 7
        },
    ]

    assets_action = Asset.query.all()

    return render_template('index.html',
                           title='Home',
                           assets_action=assets_action,
                           assets_otherhands=assets_otherhands,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished)

@app.route('/tags', methods=['GET', 'POST'])
def tags():
    tags = Tag.query.all()
    return render_template('tags.html',
                            tags=tags,
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)
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
                           assets_finished = HorizontalMenu.assets_finished)

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    form = AddTagForm()
    if form.validate_on_submit():
        tag = Tag()
        tag.timestamp = datetime.now()
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()    
        
        flash('New tag added.')
        return redirect(url_for('add_tag'))
    return render_template('add_tag.html',
                            form=form,
                            title='Add tag',
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)

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
                            assets_finished = HorizontalMenu.assets_finished)

@app.route('/sounds', methods=['GET', 'POST'])
def sounds():
    sounds = Sound.query.all()
    return render_template('sounds.html',
                            sounds=sounds,
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)
@app.route('/sound')
@app.route('/sound/<int:sound_id>/')
def sound(sound_id):
    sound = Sound.query.filter_by(id=sound_id).first()
    if sound is None:
        flash(gettext('Sound not found.'))
        return redirect(url_for('index'))
    return render_template('sound.html',
                           sound=sound,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished)

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
                            assets_finished = HorizontalMenu.assets_finished)
@app.route('/asset')
@app.route('/asset/<int:asset_id>/')
def asset(asset_id):
    asset = Asset.query.filter_by(id=asset_id).first()
    if asset is None:
        flash(gettext('Asset not found.'))
        return redirect(url_for('index'))
    return render_template('asset.html',
                           asset=asset,
                           type=type,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished)

@app.route('/descriptions', methods=['GET', 'POST'])
def descriptions():
    descriptions = Asset.query.all()
    return render_template('descriptions.html',
                            descriptions=descriptions,
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)

@app.route('/description')
@app.route('/description/<int:asset_id>/')
def description(description_id):
    description = Description.query.filter_by(id=description_id).first()
    if description is None:
        flash(gettext('description not found.'))
        return redirect(url_for('index'))
    return render_template('description.html',
                           description=description,
                           assets_ongoing = HorizontalMenu.assets_ongoing,
                           assets_finished = HorizontalMenu.assets_finished)

@app.route('/add_sound', methods=['GET', 'POST'])
def add_sound():
    form = AddSoundForm()
    if form.validate_on_submit():
        sound = Sound()
        sound.timestamp = datetime.now()
        sound.name = form.name.data
        sound.description = form.description.data
        sound.sound_type = form.sound_type.data
        sound.sound_family = form.sound_family.data
        db.session.add(sound)
        db.session.commit()    
        
        flash('New sound added.')
        return redirect(url_for('add_sound'))
    return render_template('add_sound.html',
                            form=form,
                            title='Add sound',
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)

@app.route('/delete_sound', methods=['GET', 'POST'])
def delete_sound():
    form = DeleteSoundForm()
    if form.validate_on_submit():
        sound = Sound.query.filter_by(name=form.name.data).first()
        if sound == None:
            flash('Sound ' +  form.name.data + ' does not exist.')
            return redirect(url_for('delete_sound'))
        db.session.delete(sound)
        db.session.commit()  
        
        flash('Sound ' +  form.name.data + ' was deleted.')
        return redirect(url_for('delete_sound'))
    return render_template('delete_sound.html',
                            form=form,
                            title='Delete sound',
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)

@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    form = NewAssetForm()
    if form.validate_on_submit():
        asset = Asset()
        asset.timestamp = datetime.now()
        asset.name = form.name.data
        asset.finished = False
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
        db.session.add(description)
        db.session.commit()
        
        flash('New asset description created.')
        return redirect(url_for('index'))
    return render_template('add_asset.html',
                            form=form,
                            title='Describe asset',
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)

# @app.route('/description/edit', methods=['GET', 'POST'])
# @app.route('/description/edit/<int:description_id>', methods=['GET', 'POST'])
@app.route('/describe', methods=['GET', 'POST'])
def describe():
    asset_id = request.args.get('asset_id')
    if asset_id is None:
        flash('Asset not specified.')
        return redirect(url_for('index'))
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

        db.session.add(description)
        db.session.commit()
        
        flash('Description created.')
        return redirect(url_for('index'))
    # elif request.method != "POST":
    #     if description is not None:
    #         form.name.data = description.name
    #         form.duration.data = description.duration
    #         form.pitch.data = description.pitch
    #         form.sound_type = description.sound_type
    #         form.sound_family = description.sound_family
    return render_template('describe.html',
                            form=form,
                            asset=asset,
                            title='Describe asset',
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return render_template('verify.html',
                            title='Verify iteration',
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)

@app.route('/iteratation', methods=['GET', 'POST'])
def iteratation():
    return render_template('iterate.html',
                            title='Iterate asset',
                            assets_ongoing = HorizontalMenu.assets_ongoing,
                            assets_finished = HorizontalMenu.assets_finished)

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
                           assets_finished = HorizontalMenu.assets_finished)


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
                           assets_finished = HorizontalMenu.assets_finished)
