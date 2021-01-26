from rest_framework import serializers
from djongo import models

class news_serializer(serializers.ModelSerializer):

    class Meta:
        model = "news"
        fields = '__all__'
