from django.utils.timezone import now


def first_season():
    return 2012

def current_season():
    today = now().date()
    if today.month >= 9:
        return today.year + 1
    return today.year
