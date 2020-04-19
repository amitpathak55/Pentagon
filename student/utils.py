from django.utils.text import slugify


def generate_unique_slug(instance, field_name):
    field = getattr(instance, field_name)
    slug = slugify(field)
    index = 1
    while instance._meta.model.objects.filter(slug=slug).count() > 0:
        slug = slug+'-'+str(index)
        index += 1
    return slug
    
