from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from .forms import ClientInfo, EmailForm
from .models import LoadProject, CreateBlog, CustomerInformation
from . import db, MAIL
from flask_mail import Message

views = Blueprint('views', __name__)


@views.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@views.route('/', methods=['GET', 'POST'])
def index():
    form = ClientInfo()
    email_form = EmailForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            client_name = form.client_name.data
            phone_number = form.phone_number.data
            land_location = form.land_location.data
            budget = form.budget.data

            new_client = CustomerInformation()

            new_client.client_name = client_name
            new_client.phone_number = phone_number
            new_client.land_location = land_location
            new_client.budget = budget

            if len(str(phone_number)) != 12 and str(phone_number)[0] != 2 and str(phone_number)[1] != 5 and str(phone_number)[2] != 4:
                flash('Your phone number should start with +254, try again!!!', category='danger')
                return redirect(url_for('views.index'))


            try:
                db.session.add(new_client)
                db.session.commit()
                flash('Successfully submitted', category='success')
                return redirect(url_for('index'))
            except Exception as e:
                print(e)
                # flash("An error occurred! Please try again!!", category='danger')

            form.client_name.data = ""
            form.phone_number.data = ""
            form.land_location.data = ""
            form.budget.data = ""

        if email_form.validate_on_submit():
            username = email_form.username.data
            email = email_form.email.data
            subject = email_form.subject.data
            message = email_form.message.data
            msg = Message(subject=subject, sender=email, recipients=['aernestnjuki@gmail.com'])
            msg.body = message
            MAIL.send(message=msg)
            flash("Email Successfully send!", category='success')

            email_form.username.data = ""
            email_form.email.data = ""
            email_form.subject.data = ""
            email_form.message.data = ""

    projects = LoadProject.query.filter_by(display_project=True)
    blogs = CreateBlog.query.filter_by(display_blog=True)

    return render_template('index.html', projects=projects, blogs=blogs, form=form, email_form=email_form)


@views.route('/about-project/<int:id>')
def about_project(id):
    project = LoadProject.query.get(id)

    from markupsafe import Markup
    description = Markup(project.about_project)
    project.about_project = description

    return render_template('about_project.html', project=project)


@views.route('/blog_contents/<int:blog_id>', methods=['GET', 'POST'])
def blog_contents(blog_id):
    blog = CreateBlog.query.get(blog_id)
    blogs = CreateBlog.query.all()

    from markupsafe import Markup
    content = Markup(blog.blog_content)
    blog.blog_content = content

    return render_template('blog_content.html', blog=blog, blogs=blogs)


@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        project = LoadProject.query.filter(LoadProject.location.ilike(f'%{search_query}%')).all()
        return render_template('search.html', project=project)
    return render_template('search.html')