from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Lab
from .serializers import LabSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from tlsa_server.permissions import IsManager, IsStudent

class LabView(APIView):
    serializer_class = LabSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsStudent()]
        elif self.request.method == 'POST':
            return [IsManager()]
        return []
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Lab created successfully.",
                    "lab": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='lab_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Lab ID to retrieve',
                required=True,
            ),
        ],
        responses={
            200: LabSerializer,
            400: {'error': 'lab_id parameter is required'},
            404: {'error': 'Lab not found'},
        },
    )
    def get(self, request, format=None):
        lab_id = request.query_params.get('lab_id')
        if not lab_id:
            return Response({"error": "lab_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lab = Lab.objects.get(id=lab_id)
        except Lab.DoesNotExist:
            return Response({"error": "Lab not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(lab)
        return Response(serializer.data)