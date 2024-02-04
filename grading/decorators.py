from django.contrib.auth.decorators import user_passes_test


def student_required(function=None, login_url=None):
    actual_decorator = user_passes_test(lambda u: u.is_student, login_url=login_url)
    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, login_url=None):
    actual_decorator = user_passes_test(lambda u: u.is_teacher, login_url=login_url)
    if function:
        return actual_decorator(function)
    return actual_decorator
