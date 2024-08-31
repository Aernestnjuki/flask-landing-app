from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from .forms import AddProjectForm, BlogForm
from .models import LoadProject, CreateBlog, CustomerInformation, Register
from . import db
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required


admin = Blueprint('admin', __name__)


@admin.route('/load-projects', methods=['GET', 'POST'])
@login_required
def load_projects():
    if current_user.id == 1:
        form = AddProjectForm()
        if form.validate_on_submit():
            title = form.title.data
            location = form.location.data
            price = form.price.data
            about = form.about_project.data
            display_project = form.display_project.data

            file = form.project_image.data
            file_name = secure_filename(file.filename)

            file_path = f'./media/{file_name}'

            file.save(file_path)

            #### project video #####
            video = form.project_video.data
            video_name = secure_filename(video.filename)
            video_path = f'./media/{video_name}'
            video.save(video_path)

            new_project = LoadProject()

            new_project.title = title
            new_project.location = location
            new_project.price = price
            new_project.about_project = about
            new_project.display_project = display_project
            new_project.project_image = file_path
            new_project.project_video = video_path

            try:
                db.session.add(new_project)
                db.session.commit()
                print('New project added successfully')
                flash('New project added successfully', category='success')
            except Exception as e:
                print(e)
                flash('Project had not been added', category='danger')

            form.title.data = ''
            form.location.data = ''
            form.price.data = ''
            form.about_project.data = ''

        return render_template('load_projects.html', form=form)
    return render_template('index.html')


@admin.route('/view-projects', methods=['GET', 'POST'])
@login_required
def view_project():
    if current_user.id == 1:
        projects = LoadProject.query.order_by(LoadProject.date_added).all()
        return render_template('view_projects.html', projects=projects)
    return redirect(url_for('index'))


@admin.route('/update-project/<int:id>', methods=['GET', 'POST'])
@login_required
def update_project(id):
    if current_user.id == 1:
        form = AddProjectForm()

        project_to_update = LoadProject.query.get(id)

        form.title.render_kw = {'placeholder': project_to_update.title}
        form.location.render_kw = {'placeholder': project_to_update.location}
        form.price.render_kw = {'placeholder': project_to_update.price}
        form.display_project.render_kw = {'placeholder': project_to_update.display_project}

        if form.validate_on_submit():
            title = form.title.data
            location = form.location.data
            price = form.price.data
            about_project = form.about_project
            display_project = form.display_project.data

            file = form.project_image.data
            file_name = secure_filename(file.filename)
            file_path = f"./media/{file_name}"
            file.save(file_path)

            #### project video #####
            video = form.project_video.data
            video_name = secure_filename(video.filename)
            video_path = f'./media/{video_name}'
            video.save(video_path)

            try:
                LoadProject.query.filter_by(id=id).update(title=title,
                                                          location=location,
                                                          price=price,
                                                          display_project=display_project,
                                                          about_project=about_project,
                                                          project_image=file_path,
                                                          project_video=video_path)
                db.session.commit()
                flash('Project successfully updated', category='success')
                return redirect(url_for('view_project'))
            except Exception as e:
                print(e)
                flash('Project has not been updates', category='danger')
        return render_template('update_project.html', form=form)
    return redirect(url_for('index'))

@admin.route('/delete-project/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    if current_user.id == 1:
        try:
            project_to_delete = LoadProject.query.get(id)
            db.session.delete(project_to_delete)
            db.session.commit()
            flash('Project successfully deleted', category='success')
            return redirect(url_for('admin.view_project'))
        except Exception as e:
            print(e)
            flash('An error occurred! Please try again!!!!', category='danger')
    return redirect(url_for('admin.view_project'))


@admin.route('/admins-panel')
@login_required
def admins_panel():
    return render_template('admin.html')


@admin.route('/view-blog', methods=['GET', 'POST'])
@login_required
def view_blog():
    if current_user.id == 1:
        blogs = CreateBlog.query.all()
        return render_template('view_blog.html', blogs=blogs)
    return redirect(url_for('index'))


@admin.route('/add-blog', methods=['GET', 'POST'])
@login_required
def add_blog():
    if current_user.id == 1:
        form = BlogForm()

        if form.validate_on_submit():
            blog_title = form.blog_title.data
            blog_content = form.blog_content.data
            display_blog = form.display_blog.data
            file = form.blog_image.data
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_blog = CreateBlog()

            new_blog.blog_title = blog_title
            new_blog.blog_content = blog_content
            new_blog.display_blog = display_blog
            new_blog.blog_image = file_path

            try:
                db.session.add(new_blog)
                db.session.commit()
                flash('Blog successfully added', category='success')
                return redirect(url_for('admin.view_blog'))
            except Exception as e:
                print(e)
                flash('There was an error adding the blog. Try again', category='danger')

            form.blog_title.data = ""
            form.blog_content.data = ""
            form.display_blog.data = ""

        return render_template('add_blog.html', form=form)
    return render_template('index.html')


@admin.route('/update-blog/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    if current_user.id == 1:
        form = BlogForm()

        blog_to_update = CreateBlog.query.get(blog_id)

        form.blog_title.render_kw = {'placeholder': blog_to_update.blog_title}
        form.blog_content.render_kw = {'placeholder': blog_to_update.blog_content}
        form.display_blog.render_kw = {'placeholder': blog_to_update.display_blog}

        if form.validate_on_submit():
            blog_title = form.blog_title.data
            blog_content = form.blog_content.data
            display_blog = form.display_blog.data

            file = form.blog_image.data
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)

            try:
                CreateBlog.query.filter_by(id=blog_id).update(blog_title=blog_title,
                                                              blog_content=blog_content,
                                                              blog_image=file_path,
                                                              display_blog=display_blog)

                db.session.commit()
                flash('Blog has been successfully updated', category='success')
                return redirect(url_for('view_blog'))
            except Exception as e:
                print(e)
                flash('Blog has not been updated!', category='danger')

        return render_template('update_blog.html', form=form)
    return render_template('index.html')


@admin.route('/delete-blog/<int:id>')
@login_required
def delete_blog(id):
    if current_user.id == 1:
        try:
            blog_to_delete = CreateBlog.query.get(id)
            db.session.delete(blog_to_delete)
            db.session.commit()
            flash("Blog successfully deleted!", category='success')
            return redirect(url_for('admin.view_blog'))
        except Exception as e:
            print(e)
            flash('An error occurred! Please try again!!', category='danger')

    return redirect(url_for('admin.view_blog'))


@admin.route('/client-info')
@login_required
def client_info():
    if current_user.id == 1:
        clients = CustomerInformation.query.all()
        return render_template('client_info.html', clients=clients)
    return redirect(url_for('admin_panel'))


@admin.route('/registered-clients')
@login_required
def registered_clients():
    if current_user.id == 1:
        clients = Register.query.all()
        return render_template('registered_clients.html', clients=clients)
    return redirect(url_for('admin.registered_clients'))