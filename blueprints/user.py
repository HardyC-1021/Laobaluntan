from flask import (Blueprint,render_template,
                   request,session,url_for,flash,redirect,jsonify,g)
from flask_mail import Message
from ext import mail,db
from models import EmailCaptchaModel,UserModel
import string
import random
from datetime import datetime
import os
from blueprints.forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
bp = Blueprint('user',__name__,url_prefix='/user')

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password,password):
                session['user_id'] = user.id
                return redirect('/')
            else:
                flash('邮箱和密码不匹配')
                return redirect(url_for('user.login'))

        else:
            flash('邮箱或密码格式错误')
            return redirect(url_for('user.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))


@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))


@bp.route("/captcha",methods=['POST'])
def get_captcha():
    # get方法用request.args.get获取
    # email = request.args.get('email')
    # post方法用request.form.get获取
    email = request.form.get('email')
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters,4))
    if email:
        message = Message(
            subject='一封神秘的电子邮件',
            recipients=[email],
            body=f'【老八论坛】\n您的验证是 {captcha} ! ',
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email,captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
            #"code":200} 表示正常
        return jsonify({"code":200})
    else:
        return jsonify({"code":200,"message":'请先传递邮箱 '})

@bp.route('/userhome')
def userhome():
    return render_template("userhome.html")

@bp.route('/upload', methods=["GET","POST"])
def upload():
    f = request.files['file']
    name = str(g.user.id) + ".jpg"
    path = os.path.join('./static/images', name)
    f.save(path)
    return redirect(url_for('user.userhome'))

@bp.route('/rename', methods=["GET","POST"])
def rename():
    newname = request.form.get('newname')
    user = UserModel.query.filter_by(id=g.user.id).first()
    if user:
        user.username = newname
        db.session.add(user)
        db.session.commit()
    else:
        print("failed")
    return redirect(url_for('user.userhome'))