from rest_framework import serializers
from .models import Notice, NoticeCompletion, NoticeContent, NoticeTag, NoticeContentTag, NoticeRow
from tlsa_server.models import TLSA_User

class NoticeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeContent
        fields = '__all__'

class NoticeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeTag
        fields = '__all__'

class NoticeContentTagSerializer(serializers.ModelSerializer):
    notice_content_id = serializers.PrimaryKeyRelatedField(queryset=NoticeContent.objects.all())
    notice_tag_id = serializers.PrimaryKeyRelatedField(queryset=NoticeTag.objects.all())

    class Meta:
        model = NoticeContentTag
        fields = '__all__'

class NoticeRowSerializer(serializers.ModelSerializer):
    notice_id = serializers.PrimaryKeyRelatedField(queryset=Notice.objects.all())
    notice_content_id = serializers.PrimaryKeyRelatedField(queryset=NoticeContent.objects.all())

    class Meta:
        model = NoticeRow
        fields = '__all__'

class NoticeRowGetSerializer(serializers.ModelSerializer):
    notice_content = NoticeContentSerializer(read_only=True, source='notice_content_id')
    order_num = serializers.IntegerField()

    class Meta:
        model = NoticeRow
        fields = ['id', 'notice_content', 'order_num']

class NoticeCompletionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=TLSA_User.objects.all())
    notice = serializers.PrimaryKeyRelatedField(queryset=Notice.objects.all())

    class Meta:
        model = NoticeCompletion
        fields = '__all__'

class NoticeSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=TLSA_User.objects.all())
    completions = NoticeCompletionSerializer(many=True, read_only=True)
    rows = NoticeRowSerializer(many=True, read_only=True)

    class Meta:
        model = Notice
        fields = '__all__'

class NoticeGetSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=TLSA_User.objects.all())
    completions = NoticeCompletionSerializer(many=True, read_only=True)
    rows = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = '__all__'

    def get_rows(self, obj):
        rows = obj.rows.all().order_by('order_num')
        return NoticeRowGetSerializer(rows, many=True).data

class NoticePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'class_or_lab_id', 'sender', 'notice_type', 'post_time', 'end_time']

class NoticePageSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(allow_null=True)
    course_id = serializers.IntegerField()

    class Meta:
        model = Notice
        fields = ['id', 'class_or_lab_id', 'sender', 'notice_type', 'post_time', 'end_time', 'class_id', 'course_id']