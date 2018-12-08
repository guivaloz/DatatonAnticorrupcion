#-*- coding:utf-8 -*-
from flask import Blueprint, redirect, render_template
from flask_login import current_user

sistemas = Blueprint('sistemas', __name__, template_folder='templates')


@sistemas.route('/')
def inicio():
    if current_user.is_authenticated:
        return render_template('sistemas/inicio.html',
                               title='Inicio',
                               description=u'Página inicial',
                               message='Bienvenido al sistema Central.')
    else:
        return redirect('/login')
