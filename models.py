from peewee import *

DATABASE = SqliteDatabase('learning_journal.db')


class Entry(Model):
    """ Peewee model of entries """
    title = CharField()
    date = CharField()
    duration = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)


def initialize():
    """ Create Entry table in database if it does not already exist """
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
