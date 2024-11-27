from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Notice
from .serializers import (
    NoticeSerializer, NoticeCompletionSerializer, NoticeContentSerializer, 
    NoticeTagSerializer, NoticeContentTagSerializer, NoticeRowSerializer
)

class NoticeView(APIView):
    serializer_class = NoticeSerializer

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
                description='Notice ID to retrieve',
                required=False,
            ),
            OpenApiParameter(
                name='sender_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Sender ID to retrieve',
                required=False,
            ),
            OpenApiParameter(
                name='notice_type',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Notice type to retrieve',
                required=False,
            ),
        ],
        responses={
            200: NoticeSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        notice_id = request.query_params.get('notice_id')
        sender_id = request.query_params.get('sender_id')
        notice_type = request.query_params.get('notice_type')

        filters = {}
        if notice_id:
            filters["id"] = notice_id
        if sender_id:
            filters["sender_id"] = sender_id
        if notice_type:
            filters["notice_type"] = notice_type

        notices = Notice.objects.filter(**filters)
        serializer = self.serializer_class(notices, many=True)
        return Response(serializer.data)

class NoticeCompletionView(APIView):
    serializer_class = NoticeCompletionSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice marked as completed successfully.",
                    "completion": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticeContentView(APIView):
    serializer_class = NoticeContentSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice content created successfully.",
                    "content": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticeTagView(APIView):
    serializer_class = NoticeTagSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice tag created successfully.",
                    "tag": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticeContentTagView(APIView):
    serializer_class = NoticeContentTagSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice content linked to tag successfully.",
                    "link": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticeRowView(APIView):
    serializer_class = NoticeRowSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Notice row added successfully.",
                    "row": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)