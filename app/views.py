from django.shortcuts import redirect


def home(req):
    return redirect('/admin/')
