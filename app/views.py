# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from datetime import datetime
from app import app, db, lm, oid
from .forms import LoginForm, SearchForm, DescribeForm
from .models import User, Sound, Tag
from .emails import follower_notification
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS

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

    return render_template('index.html',
                           title='Home',
                           assets_action=assets_action,
                           assets_otherhands=assets_otherhands)

@app.route('/tags', methods=['GET', 'POST'])
def tags():
    return render_template('tags.html')

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    return render_template('add_tag.html',
                            title='Add tag',)

@app.route('/delete_tag', methods=['GET', 'POST'])
def delete_tag():
    return render_template('delete_tag.html',
                            title='Delete tag',)

@app.route('/sounds', methods=['GET', 'POST'])
def sounds():
    return render_template('sounds.html',
                            title='Sounds',)

@app.route('/add_sound', methods=['GET', 'POST'])
def add_sound():
    return render_template('add_sound.html',
                            title='Add sound',)

@app.route('/delete_sound', methods=['GET', 'POST'])
def delete_sound():
    return render_template('delete_sound.html',
                            title='Delete sound',)

@app.route('/describe', methods=['GET', 'POST'])
def describe():
    return render_template('describe.html',
                            title='Describe asset',)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return render_template('verify.html',
                            title='Verify iteration',)

@app.route('/iterate', methods=['GET', 'POST'])
def iterate():
    return render_template('iterate.html',
                            title='Iterate asset',)

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
                           providers=app.config['OPENID_PROVIDERS'])


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
                           posts=posts)

