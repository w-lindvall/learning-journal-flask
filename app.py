from flask import Flask, g, render_template, flash, redirect, url_for

import forms
import models


DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

app = Flask(__name__)
app.secret_key = 'woopwoop'


@app.before_request
def before_request():
    """ Opens database (as 'g.db') before each request """
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """ Closes database (as 'g.db') before each request and returns response """
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
def index():
    """ List view of existing entries """
    entries = models.Entry.select().order_by(models.Entry.id.desc())
    return render_template('index.html', entries=entries)


@app.route('/entries/<postid>')
def detail(postid=None):
    """ Displays details of individual entry """
    entry = models.Entry.get(models.Entry.id == postid)
    return render_template('detail.html', entry=entry)


@app.route('/entries/edit/<postid>', methods=['GET', 'POST'])
def edit(postid=None):
    """ Allows user to edit information in individual entry """
    entry = models.Entry.get(models.Entry.id == postid)
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.update(
            title=form.title.data.strip(),
            date=form.date.data,
            duration=form.duration.data,
            learned=form.learned.data.strip(),
            resources=form.resources.data.strip(),
            ).where(models.Entry.id == postid).execute()
        flash("Entry saved!", 'success')
        return redirect(url_for('index'))
    form.title.data = entry.title
    form.date.data = entry.date
    form.duration.data = entry.duration
    form.learned.data = entry.learned
    form.resources.data = entry.resources
    return render_template('edit.html', form=form)


@app.route('/entries/delete/<postid>')
def delete(postid=None):
    """ Deletes individual entry and returns to list view of entries """
    models.Entry.get(models.Entry.id == postid).delete_instance()
    flash("Deleted!", 'success')
    return redirect(url_for('index'))


@app.route('/entry', methods=('GET', 'POST'))
def new_entry():
    """ Allows user to add an entry """
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(title=form.title.data.strip(),
                            date=form.date.data,
                            duration=form.duration.data,
                            learned=form.learned.data.strip(),
                            resources=form.resources.data.strip())
        flash('Entry added!', 'success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)

