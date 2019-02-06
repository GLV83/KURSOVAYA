from werkzeug.security import generate_password_hash, check_password_hash
from peewee import *
from constants import *
import datetime

handle = SqliteDatabase('finance.db')


class BaseModel(Model):
    id = PrimaryKeyField(null=False)
    created = DateTimeField(default=datetime.datetime.now())
    updated = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = handle


class User(BaseModel):
    login = CharField(unique=True)
    passwordHash = CharField()
    role = CharField()

    class Meta:
        db_table = 't_user'

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)


class Record(BaseModel):
    start_week = DateField()
    sum_revenue = FloatField(null=True)
    sum_deb_receivables = FloatField(null=True)
    sum_cred_receivables = FloatField(null=True)
    sum_arrived = FloatField(null=True)
    sum_pre_calc = FloatField(null=True)
    sum_surcharges = FloatField(null=True)
    sum_prepay = FloatField(null=True)

    class Meta:
        db_table = 't_record'


entities = [User, Record]

handle.connect()
handle.drop_tables(entities, safe=True)
handle.create_tables(entities, safe=True)

User.create(login='User1', role=USER_ROLES[0], passwordHash=generate_password_hash('test'))
User.create(login='User2', role=USER_ROLES[1], passwordHash=generate_password_hash('test'))
User.create(login='User3', role=USER_ROLES[2], passwordHash=generate_password_hash('test'))
