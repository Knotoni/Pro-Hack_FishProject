from flask_wtf import FlaskForm
from wtforms import *

class TableFor(FlaskForm):

    id_ves = IntegerField("ID корабля: ")

    id_own = IntegerField("ID собственника: ")

    id_part = IntegerField("ID юридич. лица: ")

    date = StringField("Дата: ")

    region = StringField("Регион: ")


class TableForm(FlaskForm):

    Name_Plat = IntegerField()

    Anomaly_Count = IntegerField()