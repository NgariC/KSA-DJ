from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, GroupManager
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.loader import get_template
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserManager, EmailActivationManager
from apps.accounts.utils import unique_key_generator
from apps.registrations.models import ScoutLeader


class Groups(Group):
    description = models.TextField(_('description'), max_length=1000, null=True, blank=True)

    objects = GroupManager()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(_("Profile Picture"), upload_to='profile_image/%Y/%m/%d', null=True, blank=True)
    link_to_scout_leader = models.OneToOneField(ScoutLeader, on_delete=models.CASCADE, db_constraint=False, null=True,
                                                blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    email = models.EmailField(_('email address'))
    key = models.CharField(_('key'), max_length=120, blank=True, null=True)
    activated = models.BooleanField(_('activated'), default=False)
    forced_expired = models.BooleanField(_('forced_expired'), default=False)
    expires = models.IntegerField(_('expires'), default=7)  # 7 Days
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    update = models.DateTimeField(_('update'), auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        return bool(qs.exists())

    def activate(self):
        if self.can_activate():
            # pre activation user signal
            user = self.user
            user.is_active = True
            user.save()
            # post activation signal for user
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        return self.key is not None

    def send_activation(self):
        if self.activated or self.forced_expired or not self.key:
            return False
        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        key_path = reverse("email-activate", kwargs={'key': self.key})
        path = "{base}{path}".format(base=base_url, path=key_path)
        context = {'path': path, 'email': self.email}
        txt_ = get_template("registration/emails/verify.txt").render(context)
        html_ = get_template("registration/emails/verify.html").render(context)
        subject = '1-Click Email Verification'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        return send_mail(subject, txt_, from_email, recipient_list, html_message=html_, fail_silently=False)


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired and not instance.key:
        instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()


post_save.connect(post_save_user_create_reciever, sender=User)
