from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return "<p> Login </p>"

       # user = User.query.filter_by(email=email).first()
        #if user:
         #   if check_password_hash(user.password, password):
          #      flash('Logged in successfully!', category='success')
           #     login_user(user, remember=True)
            #    return redirect(url_for('views.home'))
            #else:
             #   flash('Incorrect password, try again.', category='error')
        #else:
     #       flash('Email does not exist.', category='error') """
    return render_template("login.html")



@auth.route('/logout')
def logout():
    return "<p> Logout </p>"


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return "<p> Sign Up </p>"


