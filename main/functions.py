


def msg_count(model, user):
    return model.objects.filter(users=user).count()

