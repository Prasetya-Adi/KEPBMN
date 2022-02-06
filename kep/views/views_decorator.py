from django.contrib.auth.models import Group


def checkPabean(user):
    test_group = Group.objects.get(name='Pabean')
    user_grop = user.groups.all()
    status = test_group in user_grop
    return status


def checkP2(user):
    test_group = Group.objects.get(name='P2')
    user_grop = user.groups.all()
    status = test_group in user_grop
    return status


def check_view(user):
    test_group = Group.objects.get(name='View')
    user_grop = user.groups.all()
    status = test_group in user_grop
    return status
