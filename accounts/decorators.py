from functools import wraps
from django.shortcuts import redirect

# useful for redirections
ACCOUNT_URL = "accounts:index"


def anonymous_required(f):
    @wraps(f)
    def decorated(req, *args, **kwargs):
        if req.user.is_authenticated:
            return redirect(ACCOUNT_URL)
        return f(req, *args, **kwargs)
    return decorated


def user_status_required(*statuses):
    def decorator(f):
        @wraps(f)
        def decorated(req, *args, **kwargs):
            if req.user.profile.status not in statuses:
                return redirect("accounts:logout")
            return f(req, *args, **kwargs)

        return decorated

    return decorator
