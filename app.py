from flask import Flask, render_template, request, session, redirect, g, url_for, flash
from generate_options import generate_meanings
from db_code import Database
from email_validation import ExtraFunc
import re

app = Flask(__name__, template_folder='templates')
app.secret_key = 'gfyeg72t4972@6828'
app.config['SESSION_TYPE'] = 'filesystem'

correct_option = None
all_options = None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)
        user_email = request.form['user_email']
        password = request.form['password']
        if user_email != "" or password != "":
            db = Database()
            get_info = db.check_user(user_email, password)
            db.close()
            if get_info:
                session['user'] = user_email
                session['user_id'] = get_info
                return redirect(url_for('home_page'))
            else:
                flash('Incorrect Username/Password !!', category='error')
                return render_template('index.html')
    else:
        if g.user:
            return render_template('home.html')
        else:
            return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_name = request.form['user_email']
        pass_word = request.form['password']
        conf_password = request.form['conf_password']
        if all(len(var) >= 4 for var in [user_name, pass_word, conf_password] if var):
            if pass_word == conf_password:
                db = Database()
                check_status = db.exist_user(user_name)
                if check_status is False:
                    db.close()
                    flash('Email is already exist !!', category='error')
                    return render_template('sign_up.html')
                else:
                    check_email = ExtraFunc(user_name)
                    result = check_email.is_valid_email()
                    if type(result) is bool:
                        if result:
                            db.insert_user(user_name, pass_word)
                            db.close()
                            flash('Account created successfully !!', category='success')
                            return render_template('index.html')
                        else:
                            db.close()
                            flash('Email id is not valid!!', category='error')
                            return render_template('sign_up.html')
                    else:
                        db.close()
                        print(user_name, check_email.is_valid_email())
                        flash('Please try next month Thanks for showing interested!!', category='error')
                        return render_template('sign_up.html')
            else:
                flash('Password did not match!!', category='error')
                return render_template('sign_up.html')
        else:
            flash('Please use minimum 4 digit in each field', category='error')
            return render_template('sign_up.html')
    else:
        if g.user:
            return render_template('home.html')
        else:
            return render_template('sign_up.html')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/home', methods=['GET', 'POST'])
def home_page():
    if g.user:
        return render_template('home.html')
    else:
        return redirect(url_for('index'))


@app.route('/quiz', methods=['GET', 'POST'])
def question():
    global correct_option, all_options
    if g.user:
        db = Database()
        last_val = db.get_ques_num(session['user_id'])
        try:
            if request.method == 'POST':
                option = request.form['answer']
                user_id = session.get('user_id')
                if option == correct_option:
                    in_ques = db.insert_question(session['user'], user_id, last_val, True, correct_option)
                    db.close()
                    if in_ques:
                        flash('Correct', category='success')
                    else:
                        db.close()
                        flash('Something went wrong', category='error')
                        return redirect(url_for('logout_session'))
                else:
                    in_ques = db.insert_question(session['user'], user_id, last_val, False, correct_option)
                    db.close()
                    if in_ques:
                        flash('Incorrect', category='error')
                    else:
                        flash('Something went wrong', category='error')
                        return redirect(url_for('logout_session'))
                last_val = last_val + 1
            choices = generate_meanings()
            correct_option = choices[0][0]
            all_options = choices[1]
            return render_template('question.html', options=all_options, val=last_val)
        except Exception as e:
            print(e)
            db.close()
            flash('There was an error submitting the quiz. Please try again.', category='error')
            return redirect(url_for('quiz'))
    else:
        return redirect(url_for('logout_session'))


@app.route('/score', methods=['GET'])
def score_card():
    if g.user:
        db = Database()
        result = db.get_score(session['user_id'])
        db.close()
        return render_template('score_card.html', result=result)
    else:
        flash('Something went wrong', category='error')
        return redirect(url_for('logout_session'))

@app.route('/contact', methods=['POST'])
def submit_contact():
    if g.user:
        if request.method == 'POST':
            name = request.form['cont_name']
            email = request.form['contact_email']
            comp_name = request.form['comp_name']
            msz = request.form['message']
            if all(len(var) >= 3 for var in [name, email, comp_name, msz] if var):
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(pattern, email):
                    flash('Please use valid email', category='error')
                    return render_template('home.html')
                else:
                    db = Database()
                    db.insert_contact(name, email, comp_name, msz)
                    db.close()
                    flash('Successfully submitted!!', category='success')
                    return render_template('home.html')
            else:
                flash('Please use minimum 3 digit in each field', category='error')
                return render_template('home.html')
    else:
        flash('Something went wrong', category='error')
        return redirect(url_for('logout_session'))

@app.route('/logout')
def logout_session():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
