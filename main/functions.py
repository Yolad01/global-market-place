


def msg_count(model, user):
    return model.objects.filter(users=user).count()


def orders_count(model, user):
    return model.objects.filter(skilla=user).count() or model.objects.filter(client=user).count

