from flask import Flask,session,g
from flask_migrate import Migrate
from ext import db
from blueprints import user_bp,qa_bp
from ext import mail
from models import UserModel

import constants

app = Flask(__name__)
app.config.from_object(constants)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app,db)
app.register_blueprint(user_bp)
app.register_blueprint(qa_bp)



# 请求来了 -> before_request -> 视图函数 -> 视图函数返回模板 -> context_processor
@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定user
            # setattr(g,'user',user)
            g.user = user
        except:
            g.user = None

@app.context_processor
def context_processor():
    if hasattr(g,'user'):
        return {"user": g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
