#-*- coding:utf-8 -*-
from functools import wraps
from flask import flash, redirect
from flask_login import current_user


def anonymous_required(url='/'):
    """
    Redirect a user to a specified location if they are already signed in
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url)
            return f(*args, **kwargs)
        return decorated_function

    return decorator


def role_required(*roles):
    """
    Does a user have permission to view this page?
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.rol not in roles:
                flash(u'No tiene permiso para usar este módulo.', 'error')
                return redirect('/')
            return f(*args, **kwargs)
        return decorated_function

    return decorator
