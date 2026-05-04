from flask import Blueprint, render_template, request, session
from app.models.project import Project

projects = Blueprint('projects', __name__, url_prefix='/projects')


@projects.route('/')
def projects_page():
    projects = Project.query.order_by(Project.order.asc(), Project.created_at.desc()).all()
    return render_template('projects.html', projects=projects)


@projects.route('/filter')
def projects_by_tech():
    tech = request.args.get('tech', '').strip()
    if not tech:
        return render_template('projects_filtered.html', projects=[], tech=tech)

    projects = Project.query.filter(
        Project.tech_stack.ilike(f'%{tech}%')
    ).order_by(Project.created_at.desc()).all()

    return render_template('projects_filtered.html', projects=projects, tech=tech)


@projects.route('/sort', methods=['POST'])
def sort_projects():
    sort = request.form.get('sort', 'newest')
    session['project_sort'] = sort
    return ('', 204)


@projects.route('/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)