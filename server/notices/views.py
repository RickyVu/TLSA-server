from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notice, NoticeCompletion, NoticeContent, NoticeTag, NoticeContentTag, NoticeRow
from .serializers import NoticeSerializer, NoticeCompletionSerializer, NoticeContentSerializer, NoticeTagSerializer, NoticeContentTagSerializer, NoticeRowSerializer, NoticeGetSerializer, NoticePatchSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import permission_classes
from tlsa_server.permissions import IsAuthenticated, IsStudent, IsTeacher, IsManager, IsTeachingAffairs


class NoticeView(APIView):
    serializer_class = NoticeSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsTeacher() or IsManager()]
        elif self.request.method == 'PATCH':
            return [IsTeacher() or IsManager()]
        elif self.request.method == 'DELETE':
            return [IsTeacher() or IsManager()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice created successfully.",
                    "notice": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='notice_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Query by notice_id',
                required=False,
            ),
            OpenApiParameter(
                name='notice_type',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Query by notice_type',
                required=False,
            ),
            OpenApiParameter(
                name='class_or_lab_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Filter by class_or_lab_id',
                required=False,
            ),
        ],
        responses={
            200: NoticeGetSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        serializer_class = NoticeGetSerializer
        notice_id = request.query_params.get('notice_id')
        notice_type = request.query_params.get('notice_type')
        class_or_lab_id = request.query_params.get('class_or_lab_id')

        filters = {}
        if notice_id:
            filters["id"] = notice_id
        if notice_type:
            filters["notice_type"] = notice_type
        if class_or_lab_id:
            filters["class_or_lab_id"] = class_or_lab_id

        notices = Notice.objects.filter(**filters)

        serializer = serializer_class(notices, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=NoticePatchSerializer,
        responses={
            200: NoticeSerializer,
            404: OpenApiExample(
                name="Notice not found",
                value={"message": "Notice not found."},
                response_only=True,
            ),
            400: OpenApiExample(
                name="Invalid data",
                value={"message": "Invalid data provided."},
                response_only=True,
            ),
        },
    )
    def patch(self, request, format=None):
        notice_id = request.data.get('id')
        try:
            notice = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            return Response({"message": "Notice not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoticePatchSerializer(notice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice updated successfully.",
                    "notice": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='notice_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Notice ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Notice deleted",
                value={"message": "Notice deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Notice not found",
                value={"message": "Notice not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        notice_id = request.query_params.get('notice_id')
        try:
            notice = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            return Response({"message": "Notice not found."}, status=status.HTTP_404_NOT_FOUND)

        notice.delete()
        return Response({"message": "Notice deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class NoticeCompletionView(APIView):
    serializer_class = NoticeCompletionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsTeacher() or IsManager()]
        elif self.request.method == 'PATCH':
            return [IsTeacher() or IsManager()]
        elif self.request.method == 'DELETE':
            return [IsTeacher() or IsManager()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice completion created successfully.",
                    "notice_completion": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='completion_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Query by completion_id',
                required=False,
            ),
        ],
        responses={
            200: NoticeCompletionSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        completion_id = request.query_params.get('completion_id')

        filters = {}
        if completion_id:
            filters["id"] = completion_id

        completions = NoticeCompletion.objects.filter(**filters)

        serializer = self.serializer_class(completions, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='completion_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Completion ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Notice completion deleted",
                value={"message": "Notice completion deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Notice completion not found",
                value={"message": "Notice completion not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        completion_id = request.query_params.get('completion_id')
        try:
            completion = NoticeCompletion.objects.get(id=completion_id)
        except NoticeCompletion.DoesNotExist:
            return Response({"message": "Notice completion not found."}, status=status.HTTP_404_NOT_FOUND)

        completion.delete()
        return Response({"message": "Notice completion deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class NoticeContentView(APIView):
    serializer_class = NoticeContentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsTeacher() or IsManager()]
        elif self.request.method == 'PATCH':
            return [IsTeacher() or IsManager()]
        elif self.request.method == 'DELETE':
            return [IsTeacher() or IsManager()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice content created successfully.",
                    "notice_content": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='content_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Query by content_id',
                required=False,
            ),
            OpenApiParameter(
                name='tag_name',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter by tag name',
                required=False,
            ),
            OpenApiParameter(
                name='text_content',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter by text content (similarity)',
                required=False,
            ),
        ],
        responses={
            200: NoticeContentSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        content_id = request.query_params.get('content_id')
        tag_name = request.query_params.get('tag_name')
        text_content = request.query_params.get('text_content')

        filters = {}
        if content_id:
            filters["id"] = content_id
        if text_content:
            filters["text_content__icontains"] = text_content

        contents = NoticeContent.objects.filter(**filters)

        if tag_name:
            contents = contents.filter(noticecontenttag__notice_tag_id__tag_name=tag_name)

        serializer = self.serializer_class(contents, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=NoticeContentSerializer,
        responses={
            200: NoticeContentSerializer,
            404: OpenApiExample(
                name="Notice content not found",
                value={"message": "Notice content not found."},
                response_only=True,
            ),
            400: OpenApiExample(
                name="Invalid data",
                value={"message": "Invalid data provided."},
                response_only=True,
            ),
        },
    )
    def patch(self, request, format=None):
        content_id = request.data.get('id')
        try:
            content = NoticeContent.objects.get(id=content_id)
        except NoticeContent.DoesNotExist:
            return Response({"message": "Notice content not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice content updated successfully.",
                    "notice_content": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='content_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Content ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Notice content deleted",
                value={"message": "Notice content deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Notice content not found",
                value={"message": "Notice content not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        content_id = request.query_params.get('content_id')
        try:
            content = NoticeContent.objects.get(id=content_id)
        except NoticeContent.DoesNotExist:
            return Response({"message": "Notice content not found."}, status=status.HTTP_404_NOT_FOUND)

        content.delete()
        return Response({"message": "Notice content deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class NoticeTagView(APIView):
    serializer_class = NoticeTagSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsTeacher() or IsManager() or IsTeachingAffairs()]
        elif self.request.method == 'DELETE':
            return [IsTeacher() or IsManager() or IsTeachingAffairs()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice tag created successfully.",
                    "notice_tag": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='tag_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Query by tag_id',
                required=False,
            ),
        ],
        responses={
            200: NoticeTagSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        tag_id = request.query_params.get('tag_id')

        filters = {}
        if tag_id:
            filters["id"] = tag_id

        tags = NoticeTag.objects.filter(**filters)

        serializer = self.serializer_class(tags, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='tag_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Tag ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Notice tag deleted",
                value={"message": "Notice tag deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Notice tag not found",
                value={"message": "Notice tag not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        tag_id = request.query_params.get('tag_id')
        try:
            tag = NoticeTag.objects.get(id=tag_id)
        except NoticeTag.DoesNotExist:
            return Response({"message": "Notice tag not found."}, status=status.HTTP_404_NOT_FOUND)

        tag.delete()
        return Response({"message": "Notice tag deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class NoticeContentTagView(APIView):
    serializer_class = NoticeContentTagSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsTeacher() or IsManager() or IsTeachingAffairs]
        elif self.request.method == 'DELETE':
            return [IsTeacher() or IsManager() or IsTeachingAffairs]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice content tag created successfully.",
                    "notice_content_tag": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='content_tag_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Query by content_tag_id',
                required=False,
            ),
        ],
        responses={
            200: NoticeContentTagSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        content_tag_id = request.query_params.get('content_tag_id')

        filters = {}
        if content_tag_id:
            filters["id"] = content_tag_id

        content_tags = NoticeContentTag.objects.filter(**filters)

        serializer = self.serializer_class(content_tags, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='content_tag_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Content tag ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Notice content tag deleted",
                value={"message": "Notice content tag deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Notice content tag not found",
                value={"message": "Notice content tag not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        content_tag_id = request.query_params.get('content_tag_id')
        try:
            content_tag = NoticeContentTag.objects.get(id=content_tag_id)
        except NoticeContentTag.DoesNotExist:
            return Response({"message": "Notice content tag not found."}, status=status.HTTP_404_NOT_FOUND)

        content_tag.delete()
        return Response({"message": "Notice content tag deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class NoticeRowView(APIView):
    serializer_class = NoticeRowSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsTeacher() or IsManager()]
        elif self.request.method == 'DELETE':
            return [IsTeacher() or IsManager()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice row created successfully.",
                    "notice_row": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='row_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Query by row_id',
                required=False,
            ),
        ],
        responses={
            200: NoticeRowSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        row_id = request.query_params.get('row_id')

        filters = {}
        if row_id:
            filters["id"] = row_id

        rows = NoticeRow.objects.filter(**filters)

        serializer = self.serializer_class(rows, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='row_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Row ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Notice row deleted",
                value={"message": "Notice row deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Notice row not found",
                value={"message": "Notice row not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        row_id = request.query_params.get('row_id')
        try:
            row = NoticeRow.objects.get(id=row_id)
        except NoticeRow.DoesNotExist:
            return Response({"message": "Notice row not found."}, status=status.HTTP_404_NOT_FOUND)

        row.delete()
        return Response({"message": "Notice row deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
