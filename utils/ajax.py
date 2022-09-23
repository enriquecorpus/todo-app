import functools
import django.core.exceptions


def ajax_required(func):
    @functools.wraps(func)
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax():
            return func(request, *args, **kwargs)
        return django.core.exceptions.PermissionDenied()

    return _wrapped_view
