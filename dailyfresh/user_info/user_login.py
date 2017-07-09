from django.shortcuts import redirect


def login_au(fun):
    def func(request, *args, **kwargs):
        if request.session.has_key("uid"):
            return fun(request, *args, **kwargs)
        else:
            return redirect('/ttsx/login/')
    return func


