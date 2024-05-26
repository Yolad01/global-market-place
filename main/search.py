from django.db.models.query import QuerySet

def search_brief_title(model, param) -> QuerySet:
    return model.objects.filter(title__icontains=param)


def search_brief_category(model, param) -> QuerySet:
    return model.objects.filter(categories__title__icontains=param)

def search_skill_category(model, param) -> QuerySet:
    return model.objects.filter(category__title__icontains=param)


def search_skilla(model, param) -> QuerySet:
    return model.objects.filter(username__icontains=param)

def skill_search(model, param) -> QuerySet:
    return model.objects.filter(title__icontains=param)

