from ast import Return
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import InformationForm, RegistrationForm, LoginForm, EmailForm, PasswordForm, Search
from pymysql.cursors import DictCursor

import pymysql.cursors

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = pymysql.connect(host='localhost', user='root', password='', database='customer', cursorclass=DictCursor)
cursor = db.cursor()

#variables and dictionaries
loginstate = False
adminstate = False
infoid = 0
searchkey = ''
adminbox = 'n'
session = {
            'ID':'',
            'name':'',
            'email':'',
            'password':''}
result = {
            'AID':'',
            'UID':'',
            'name':'',
            'email':'',
            'password':''}
#index and default page
@app.route("/")
@app.route("/index")
def index():
    global loginstate
    global session
    udisplay = ''
    #get username from dictionary
    if loginstate == True:
        udisplay = session['name']
    return render_template('index.html',loginstate=loginstate, userdisplay=udisplay)
    

#about page
@app.route("/about")
def about():
    global loginstate
    return render_template('about.html', title='About',loginstate=loginstate)

#infolist page
@app.route("/infolist",methods=["GET","POST"])
def infolist():
    global loginstate
    global session
    global cursor
    global infoid
    sql = "SELECT * FROM information"
    cursor.execute(sql)
    infolist=cursor.fetchall()
    if request.method == 'POST':
        infoid = request.form.get("button")
        return redirect(url_for('infodisplay'))
    else:
        pass
        
    return render_template('infolist.html', title='infolist list', infolist=infolist)

#infosearch page
@app.route("/infosearch",methods=["GET","POST"])
def infosearch():
    global searchkey
    global cursor
    form = Search()
    if request.method == 'POST'and form.validate_on_submit():
        searchkey = request.form.get("Keyword")
        return redirect(url_for('infosearchr',form=form))
    return render_template('infosearch.html',title='infosearch',form=form)

#info search result
@app.route("/infosearchr")
def infosearchr():
    global searchkey
    global cursor
    global infoid
    sql = "SELECT * FROM information WHERE skills LIKE %s"
    cursor.execute(sql,('%'+searchkey+'%'))
    infolist = cursor.fetchall()
    if request.method == 'POST':
        infoid = request.form.get("button")
        return redirect(url_for('infodisplay.html'))
    else:
        pass

    return render_template('infosearchr.html', title='info result',infolist=infolist)
#info display
@app.route("/infodisplay/<UID>",methods=["GET","POST"])
def infodisplay(UID):
    global infoid
    global cursor
    sql = "SELECT * FROM information WHERE UID =(%s)"


    # var = infoid
    form = EmailForm()
    cursor.execute(sql,UID)
    infolist=cursor.fetchone()
    if request.method == 'POST'and form.validate_on_submit():
        email = request.form.get("email")
        name = request.form.get("name")
        sql = "INSERT INTO VEMail (name, email, UID) VALUE (%s,%s,%s)"
        cursor.execute(sql,(email,name,infoid))
        db.commit()
        flash(f'email{form.email.data} will be sent to freelancer!,Talent may contact you soon!', 'success')
        return render_template('infolist.html', title='infolist list', infolist=infolist)
    else:
            pass
    return render_template('infodisplay.html',title='info_detials', infolist=infolist, form=form)

#account registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    global cursor
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql,(username, email, password))
        db.commit()

        flash(f'Account created for {form.username.data}!,Please go to account to update information', 'success')
        return redirect(url_for('index'))
    return render_template('register.html/', title='Register',form=form ,loginstate=loginstate)

@app.route("/infosubmission.html", methods=['GET', 'POST'])
def infosubmission():
    global session
    global cursor
    global loginstate
    form = InformationForm()
    if request.method == "POST"and form.validate_on_submit():
            #this section is for first timers inserting information
        try:
            name = request.form["Fullname"]
            location = request.form["location"]
            skills = request.form["skills"]
            website = request.form["website"]
            email = request.form["email"]
            phone = request.form["phone"]
            experience = request.form["experience"]
            selfintro = request.form["selfintro"]
            UID = session["ID"]
            sql = "INSERT INTO information(UID,name,location,skills,website,email,phone,experience,selfintro) VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)"
            cursor.execute(sql,(UID,name,location,skills,website,email,phone,experience,selfintro))
            db.commit()
            #this section is for updating personal information
        except:
            name = request.form["Fullname"]
            location = request.form["location"]
            skills = request.form["skills"]
            website = request.form["website"]
            email = request.form["email"]
            phone = request.form["phone"]
            experience = request.form["experience"]
            selfintro = request.form["selfintro"]
            UID = session["ID"]
            sql = "UPDATE information SET name =%s , location=%s , skills=%s , website=%s , email=%s ,phone=%s ,experience=%s ,selfintro=%s WHERE UID = %s"
            val = name,location,skills,website,email,phone,experience,selfintro,UID
            cursor.execute(sql,val)
            db.commit()

        flash(f'Account information updated !', 'success')
        return redirect(url_for('account')) 
    return render_template('infosubmission.html',title='submission',form=form,session=session)


@app.route("/login", methods=['GET', 'POST'])
def login():
    global session
    global loginstate
    global adminstate
    global result
    form = LoginForm()
    if form.validate_on_submit():
        #clearing previous users's detials
        session = {
            'ID':'',
            'name':'',
            'email':'',
            'password':''}
        #resetting checkbox initial state
        adminbox = 'n'

        email = request.form["email"]
        password = request.form["password"]
        #admin checkbox check
        try:
            adminbox = request.form["admin"]
        #non admin login
        except:
            adminbox = 'n'
        if adminbox == 'y':
            sql = "SELECT * FROM admin WHERE email=(%s)"
            cursor.execute(sql,(email))
            result = cursor.fetchone()

            try:
                session['ID'] = result['AID']
                session['name'] = result['username']
                session['email'] = result['email']
                session['password'] = result['password']
            except :
                adminbox = 'n'
            #successful admin login
            if password == session['password']:
                loginstate = True
                adminstate = True
                flash('You have been logged in as administrator!', 'success')
                return redirect(url_for('admin',session=session))
            #failed admin login
            else:
                session.pop('ID',None)
                session.pop('name',None)
                session.pop('email',None)
                session.pop('password',None)
                loginstate = False
                flash('Failed to log in as administrator!', 'danger')
                return redirect(url_for('login'))
        if adminbox == 'n':        
            sql = "SELECT * FROM users WHERE email=(%s)"
            cursor.execute(sql,(email))
            result = cursor.fetchone()
            
            try:
                session['ID'] = result['UID']
                session['name'] = result['username']
                session['email'] = result['email']
                session['password'] = result['password']
            except:
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return render_template('login.html', title='Login',form=form ,loginstate=loginstate)
            try:
                if password == session['password']:
                    loginstate = True
                    flash('You have been logged in!', 'success')
                    print(loginstate)
                    return redirect(url_for('index',loginstate=loginstate))
                else:
                    session.pop('ID',None)
                    session.pop('name',None)
                    session.pop('email',None)
                    session.pop('password',None)
                    loginstate = False
                    flash('Login Unsuccessful. Please check username and password', 'danger')
                    return render_template('login.html', title='Login',form=form,loginstate=loginstate)
            except:
                flash('Login Unsuccessful. Please check username and password', 'danger')            
    return render_template('login.html', title='Login',form=form,loginstate=loginstate)

@app.route("/logout", )
def logout():
    global session
    global loginstate
    global adminstate
    if loginstate == True:
        session.pop('ID',None)
        session.pop('name',None)
        session.pop('email',None)
        session.pop('password',None)
        loginstate = False
        adminstate = False
        flash('Logout successful.', 'success')
    else:
        flash('You are currently not logged in.', 'danger')
    return render_template('index.html',loginstate=loginstate)

@app.route("/account", methods=["GET", "POST"])
def account():
    global session
    global loginstate
    global adminstate
    global cursor
    if adminstate == True:
        flash('Please use admin for all details.', 'danger')
        return redirect(url_for('admin',loginstate=loginstate))
    #Determine if user is logged in
    if loginstate == True:
        login = "true"
        UID= session['ID']
        sql = "SELECT UID, username, email FROM users WHERE UID=(%s)"
        cursor.execute(sql,(UID))
        account=cursor.fetchone()
        sql = "SELECT * FROM information WHERE UID=(%s)"
        cursor.execute(sql,(UID))
        infolist=cursor.fetchone()
        sql = " SELECT * FROM vemail WHERE UID=(%s)"
        cursor.execute(sql,(UID))
        vlist=cursor.fetchall()

        if request.method == "POST":
            VEID = request.form.get("VEID")
            sql = "DELETE FROM vemail WHERE VEID=(%s)"
            cursor.execute(sql,(VEID))
            db.commit()
            flash('Visitor detail removed.','success')
            return render_template('account.html',infolist=infolist, account=account, vlist=vlist, loginstate=loginstate, login=login)
        else:
            pass
        
    #If user is not logged in
    else:
        login = "false"
        flash('You are currently not logged in, please login to access personal detials', 'danger')
        return redirect(url_for('index'))
    return render_template('account.html',infolist=infolist, account=account, vlist=vlist, loginstate=loginstate, login=login)

#Change user password
@app.route("/passwordchange", methods=['GET', 'POST'])
def passwordchange():
    global session
    global cursor
    form = PasswordForm()
    if request.method == "POST" and form.validate_on_submit():
        UID = session['ID']
        sql = "SELECT * FROM users WHERE UID=(%s)"
        cursor.execute(sql,(UID))
        result = cursor.fetchone()
        oldpassword = request.form["oldpassword"]
        if oldpassword == result['password']:
            password = request.form["password"]
            sql = "UPDATE users SET password=%s WHERE UID = %s"
            cursor.execute(sql,(password, UID))
            db.commit()
            flash(f'User password updated!','success')
            return redirect(url_for('account'))
        
        else:
            flash(f'An error occured please re-enter password', 'danger')
            return redirect(url_for('passwordchange'))
    return render_template('passwordchange.html/', title='Passwordchange',form=form ,loginstate=loginstate)

@app.route("/admin",)
def admin():
    global session
    global loginstate
    global adminstate
    if loginstate == True and adminstate == True:
        return render_template('admin.html',loginstate=loginstate)
    else:
        flash('Please login as admin before proceding', 'danger')
    return render_template('index.html',loginstate=loginstate)

@app.route("/adminview",methods=["GET","POST"])
def adminview():
    global cursor
    global loginstate
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    userlist=cursor.fetchall()
    if request.method == "POST":
        id = request.form.get("id")
        confirm = request.form.get("confirm")
        if confirm == "Confirm":
            try:
                sql = "DELETE FROM users WHERE UID=(%s)"
                cursor.execute(sql,(id))
                db.commit()
                flash('User removed successfully', 'success')
                return render_template('adminview.html',userlist=userlist,loginstate=loginstate)
            except:
                flash('Please re-enter id to be removed', 'danger')
                return render_template('adminview.html',userlist=userlist,loginstate=loginstate)
        else:
            flash('Please re-confirm', 'danger')
            return render_template('adminview.html',userlist=userlist,loginstate=loginstate)
    return render_template('adminview.html',userlist=userlist,loginstate=loginstate)

@app.route("/infoview")
def bookingview():
    global loginstate

    sql = "SELECT * FROM information"
    cursor.execute(sql)
    infolist=cursor.fetchall()
    return render_template('infoview.html',infolist=infolist,loginstate=loginstate)


@app.route("/home")
def home():
    global adminstate
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, )

