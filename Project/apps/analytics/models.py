from django.conf import settings
from django.contrib.contenttypes import fields
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


def views_limit():
    return Q(model='unit')


class ObjectViewed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, limit_choices_to=views_limit, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return f"{self.content_object} viewed: {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'


class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Client(models.Model):
    city = models.CharField(max_length=16)

    # These aren't required, but they'll allow you do cool stuff
    # like "person.sent_messages.all()" to get all messages sent
    # by that person, and "person.received_messages.all()" to
    # get all messages sent to that person.
    # Well...sort of, since "received_messages.all()" will return
    # a queryset of "MessageRecipient" instances.
    sent_messages = fields.GenericRelation('Message',
                                           content_type_field='sender_content_type',
                                           object_id_field='sender_id'
                                           )
    received_messages = fields.GenericRelation('MessageRecipient',
                                               content_type_field='recipient_content_type',
                                               object_id_field='recipient_id'
                                               )

    class Meta:
        abstract = True


class PersonClient(Client):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    gender = models.CharField(max_length=1)

    def __unicode__(self):
        return f'{self.last_name} {self.first_name}'


class CompanyClient(Client):
    name = models.CharField(max_length=32)
    tax_no = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class Message(models.Model):
    sender_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    sender_id = models.PositiveIntegerField()
    sender = fields.GenericForeignKey('sender_content_type', 'sender_id')
    msg_body = models.CharField(max_length=1024)

    def __unicode__(self):
        return f'{self.msg_body[:25]}...'


class MessageRecipient(models.Model):
    message = models.ForeignKey(Message, on_delete=models.PROTECT)
    recipient_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    recipient_id = models.PositiveIntegerField()
    recipient = fields.GenericForeignKey('recipient_content_type', 'recipient_id')

    def __unicode__(self):
        return f'{self.message} sent to {self.recipient}'
