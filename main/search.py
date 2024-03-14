
def search_brief_title(model, param: str):
    return model.objects.filter(title__icontains=param)


def search_brief_category(model, param: str):
    return model.objects.filter(categories__title__icontains=param)

