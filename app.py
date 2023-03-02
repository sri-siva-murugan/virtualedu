from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo, MongoClient
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb+srv://sri-siva-murugan-v:worldhello123@cluster0.9bjtndz.mongodb.net/test'

mongo = PyMongo(app)

# client = pymongo.MongoClient("mongodb+srv://sri-siva-murugan-v:<password>@cluster0.9bjtndz.mongodb.net/?retryWrites=true&w=majority")
# db = client.test


db = mongo.db.test

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'email' in session:
        return redirect(url_for('teacher_dashboard'))
    # return render_template('landingpage.html')


# @app.route('/enteras', methods=['GET', 'POST'])
# def role():
    if request.method == 'POST':
        if request.form.get('TEACHER') == 'TEACHER':
            return render_template('index.html')
#         elif  request.form.get('STUDENT') == 'STUDENT':
#             return "this is student entry"
#     elif request.method == 'GET':
#         return render_template("landingpage.html")
    
    return render_template("landingpage.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'email' in session: 
        return redirect(url_for('teacher_dashboard'))


    teachers = mongo.db.teachers
    login_teacher = teachers.find_one({'email' : request.form['email']})

    if login_teacher:
        print(request.form['password'].encode('utf-8')) #b'password'
        print(login_teacher['password'])  #b'$2b$12$hUQ.mlQ4oryRY7yl1C37rueGkA/eEZPn4BkS2zkz4XvRETRZu/Nb.'
        print(bcrypt.hashpw(request.form['password'].encode('utf-8'), login_teacher['password']))  #b'$2b$12$hUQ.mlQ4oryRY7yl1C37rueGkA/eEZPn4BkS2zkz4XvRETRZu/Nb.'
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_teacher['password']) == login_teacher['password']:
        # # if bcrypt.hashpw(request.form['password'], login_teacher['password']) == login_teacher['password']:
            session['email'] = request.form['email']
            return redirect(url_for('index'))

    return 'Invalid email/password combination'


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email',None)
    return redirect(url_for("index"))

@app.route('/register', methods=['POST', 'GET'])
def register():
    print(mongo)
    print("--")
    print(db)
    print("--")
    print(mongo.db.test)
    if request.method == 'POST':
        teachers = mongo.db.teachers
        existing_teacher = teachers.find_one({'email' : request.form['email']})

        if existing_teacher is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            teachers.insert_one({'email': request.form['email'], 'username' : request.form['username'], 'password' : hashpass})
            session['email'] = request.form['email']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/teacher_dashboard', methods=['GET', 'POST', 'DELETE'])
def teacher_dashboard():
    
    if 'email' not in session:
    # if 'email' in session:
        return redirect(url_for('index'))
    elif request.method == 'GET' and 'email'  in session:
        return render_template("teacher_dashboard.html")
    else:
        if request.form.get('CREATE LESSON') == 'CREATE LESSON':
            return redirect(url_for('create_lesson'))
    #     elif request.form.get('DELETE LESSON') == 'DELETE LESSON':
    #         return "del les page"
    #     elif request.form.get('ADD PAGE') == 'ADD PAGE':
    #         return 'add page page'
    #     elif request.form.get('DELETE PAGE') == 'DELETE PAGE':
    #         return 'delete page page'
    #     elif request.form.get('VIEW EXERCISES') == 'VIEW EXERCISES':
    #         return 'view exercises page'

@app.route('/create_lesson', methods=['GET', 'POST'])
def create_lesson():
    if "email" not in session:
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('create_lesson.html')
    else:
        back = request.referrer
        lesson_name = request.form.get('lessonname')
        teacher_email= session['email']
        lessons = mongo.db.lessons
        existing_lesson = lessons.find_one({'teacher_email' : teacher_email, 'lesson_name': lesson_name})
        
        if existing_lesson is None:

            lessons.insert_one({'teacher_email': teacher_email, 'lesson_name': lesson_name})
            print('lesson created successfully')
            flash('lesson created successfully')
            return redirect(url_for('teacher_dashboard'))
        
        flash('lesson name already exists')
        return render_template('create_lesson.html')
        # teacher_doc = teachers.find_one({'email' : teacher_email})
        # print(teacher_doc['email'])
        # print(teacher_doc['_id'])
        

    
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)