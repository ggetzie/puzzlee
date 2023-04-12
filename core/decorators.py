from functools import wraps
from django.http import JsonResponse


def user_is_staff_api(view_func):
    """
    Check that user is staff for api requests
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({"error": "This feature is for staff only"})
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view
