from .views import views_decorator


def user_group(request):
    pabean = views_decorator.checkPabean(request.user)
    p2 = views_decorator.checkP2(request.user)
    view = views_decorator.check_view(request.user)

    return {'pabean': pabean,
            'p2': p2,
            'view': view}
