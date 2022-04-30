from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

"""如果想让视图函数只对具有特定权限的用户开放，可以使用自定义的装饰器。下面实
现了两个装饰器，一个用于检查常规权限，另一个专门检查管理员权限。"""

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
