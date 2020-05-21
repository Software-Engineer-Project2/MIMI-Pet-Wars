from flask import Flask
from hospitalapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads,UploadSet,IMAGES
from flask_migrate import Migrate
from sqlalchemy import MetaData

app = Flask(__name__)
app.config.from_object(Config)

photos = UploadSet('products', IMAGES)
configure_uploads(app, photos)
###初始化插件
#定义命名惯例，不需要改
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
#初始化db,将命名惯例naming_convention传给SQL_Alchemy,解决“ValueError: Constraint must have a name"的问题
db = SQLAlchemy(app=app,metadata=MetaData(naming_convention=naming_convention))
#使用batch操作替换普通操作，因为普通操作不支持表名，列名的改变！
migrate = Migrate(app,db,render_as_batch=True)
#db = SQLAlchemy(app)
#migrate = Migrate(app,db) #migrate databaseCMD
#migrate = Migrate(app,db, render_as_batch=True)
from hospitalapp import routes, models



