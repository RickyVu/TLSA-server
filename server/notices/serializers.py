from rest_framework import serializers
from .models import Notice, NoticeCompletion, NoticeContent, NoticeTag, NoticeContentTag, NoticeRow

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

class NoticeCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeCompletion
        fields = '__all__'

class NoticeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeContent
        fields = '__all__'

class NoticeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeTag
        fields = '__all__'

class NoticeContentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeContentTag
        fields = '__all__'

class NoticeRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeRow
        fields = '__all__'