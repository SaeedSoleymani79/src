from django.contrib.auth.decorators import user_passes_test

def anonymous_required(function=None, redirect_url=None):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the specified page if necessary.
    """
    if not redirect_url:
        redirect_url = '/'

    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
