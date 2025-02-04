from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.group import Group
from models import db
from forms import AddGroupForm
from . import dashboard_bp
from utils.decorators import roles_required





@dashboard_bp.route('/admin-dashboard', methods=['GET', 'POST'])
@roles_required('Admin')

def admin_dashboard():
    form = AddGroupForm()
    groups = Group.query.all()
    if form.validate_on_submit():
        new_group = Group(group_name=form.group_name.data, group_link=form.group_link.data)
        db.session.add(new_group)
        db.session.commit()
        flash('New group added successfully!', 'success')
        return redirect(url_for('dashboard_bp.admin_dashboard'))
    return render_template('dashboard/admin-dashboard.html', form=form, groups=groups)
