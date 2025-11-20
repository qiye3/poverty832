from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

def data_entry_required(view_func):
    return user_passes_test(lambda u: u.groups.filter(name="data_entry").exists())(view_func)

def analyst_required(view_func):
    return user_passes_test(lambda u: u.groups.filter(name="analyst").exists())(view_func)
