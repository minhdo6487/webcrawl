from __future__ import unicode_literals

from django.db import models
from mongoengine import Document, EmbeddedDocument, fields

# Create your models here.

class test_model(Document):
    email = fields.StringField(required=True)
    first_name = fields.StringField(max_length=50)
    last_name = fields.StringField(max_length=50)

    meta = {'ordering': ['-email']}