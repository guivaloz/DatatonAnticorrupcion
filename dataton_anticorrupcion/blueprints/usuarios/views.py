#-*- coding:utf-8 -*-
from flask import Blueprint, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from lib.safe_next_url import safe_next_url

from dataton_anticorrupcion.blueprints.usuarios.decorators import anonymous_required, role_required
from dataton_anticorrupcion.blueprints.usuarios.forms import LoginForm, UsuariosForm
from dataton_anticorrupcion.blueprints.usuarios.models import Usuarios


usuarios = Blueprint('usuarios', __name__, template_folder='templates')


@usuarios.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))
    if form.validate_on_submit():
        u = Usuarios.find_by_identity(request.form.get('identidad'))
        if u and u.authenticated(password=request.form.get('contrasena')):
            if login_user(u, remember=True) and u.is_active():
                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))
                return redirect(url_for('sistemas.inicio'))
            else:
                flash(u'Esta cuenta está inactiva', 'error')
        else:
            flash(u'Usuario o contraseña incorrectos.', 'error')
    return render_template('usuarios/login.html', form=form)


@usuarios.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'Ha salido de este sistema.', 'success')
    return redirect(url_for('usuarios.login'))


@usuarios.route('/usuarios')
@login_required
@role_required('admin')
def list_active():
    estatus = 'A'
    usuarios = Usuarios.query. \
        filter(Usuarios.estatus == estatus). \
        order_by(Usuarios.nombre).all()
    actions = { 'status': estatus, 'new': True }
    return render_template('usuarios/list.html', usuarios=usuarios, actions=actions)


@usuarios.route('/usuarios/deleted')
@login_required
@role_required('admin')
def list_deleted():
    estatus = 'B'
    usuarios = Usuarios.query. \
        filter(Usuarios.estatus == estatus). \
        order_by(Usuarios.nombre).all()
    actions = { 'status': estatus }
    return render_template('usuarios/list.html', usuarios=usuarios, actions=actions)


@usuarios.route('/usuarios/detail/<int:id>')
@login_required
@role_required('admin')
def detail(id):
    usuario = Usuarios.query.get(id)
    actions = { 'status': usuario.estatus, 'edit': True }
    return render_template('usuarios/detail.html', usuario=usuario, actions=actions)


@usuarios.route('/usuarios/new', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def new():
    form = UsuariosForm()
    if form.validate_on_submit():
        usuario = Usuarios()
        form.populate_obj(usuario)
        usuario.save()
        flash(u'Usuario {0} recibido.'.format(usuario.nombre), 'success')
        return redirect(url_for('usuarios.detail', id=usuario.id))
    return render_template('usuarios/new.html', form=form)


@usuarios.route('/usuarios/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    usuario = Usuarios.query.get(id)
    form = UsuariosForm()
    if form.validate_on_submit():
        form.populate_obj(usuario)
        usuario.save()
        flash(u'Usuario {0} modificado.'.format(usuario.nombre), 'success')
        return redirect(url_for('usuarios.detail', id=id))
    form.process(obj=usuario)
    return render_template('usuarios/edit.html', form=form, usuario=usuario)


@usuarios.route('/usuarios/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete(id):
    usuario = Usuarios.query.get(id)
    if usuario.estatus == 'A':
        usuario.delete()
        flash(u'Usuario {0} eliminado.'.format(usuario.nombre), 'success')
    return redirect(url_for('usuarios.detail', id=id))


@usuarios.route('/usuarios/recover/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def recover(id):
    usuario = Usuarios.query.get(id)
    if usuario.estatus == 'B':
        usuario.recover()
        flash(u'Usuario {0} recuperado.'.format(usuario.nombre), 'success')
    return redirect(url_for('usuarios.detail', id=id))
