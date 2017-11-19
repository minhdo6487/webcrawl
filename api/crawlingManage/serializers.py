from rest_framework_mongoengine import serializers
from core.crawling.models import test_model

class TestModelSerializer(serializers.DocumentSerializer):
    class Meta:
        model = test_model
        fields = ('email', 'first_name', 'last_name')