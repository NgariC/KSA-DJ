import random
import string

from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.debug import sensitive_post_parameters


class DisAllowLoggedInUser:
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    slug = new_slug if new_slug is not None else slugify(instance.title)
    Klass = instance.__class__
    if qs_exists := Klass.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_key_generator(instance):
    size = random.randint(30, 45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    if qs_exists := Klass.objects.filter(key=key).exists():
        return unique_slug_generator(instance)
    return key
