#-*- coding:utf-8 -*-
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from dataton_anticorrupcion.blueprints.contrataciones_abiertas.models import ContratacionesAbiertas

contrataciones_abiertas = Blueprint('contrataciones_abiertas',
                                     __name__,
                                     template_folder='templates')


@contrataciones_abiertas.before_request
@login_required
def before_request():
    pass


@contrataciones_abiertas.route('/contrataciones_abiertas')
def list_active():
    contrataciones_abiertas = ContratacionesAbiertas.query.all()
    return render_template('contrataciones_abiertas/list.html',
                           contrataciones_abiertas=contrataciones_abiertas,
                           actions=None)
