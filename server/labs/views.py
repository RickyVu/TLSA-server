from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lab, ManageLab
from .serializers import LabSerializer, ManageLabSerializer, ManagerDetailSerializer, LabOutputSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from tlsa_server.permissions import IsAuthenticated, IsStudent, IsTeacher, IsManager

class LabView(APIView):
    serializer_class = LabSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
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
                description='Query by lab_id',
                required=False,
            ),
            OpenApiParameter(
                name='lab_name',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Query by lab_name (similarity)',
                required=False,
            ),
        ],
        responses={
            200: LabSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        serializer_class = LabOutputSerializer
        lab_id = request.query_params.get('lab_id')
        lab_name = request.query_params.get('lab_name')

        filters = {}
        if lab_id:
            filters["id"] = lab_id
        if lab_name:
            filters["name__icontains"] = lab_name

        labs = Lab.objects.filter(**filters)

        serializer = serializer_class(labs, many=True)
        return Response(serializer.data)
    
class LabManagerView(APIView):
    serializer_class = ManageLabSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsManager()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            manage_lab = serializer.save()
            return Response(
                {
                    "message": "Manager added to lab successfully.",
                    "manager": {
                        "manager_id": manage_lab.manager.id,
                        "lab_id": manage_lab.lab.id
                    }
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
                description='Lab ID to retrieve managers for',
                required=False,
            ),
            OpenApiParameter(
                name='manager_name',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Manager name to retrieve (simularity)',
                required=False,
            ),
        ],
        responses={
            200: ManagerDetailSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        lab_id = request.query_params.get('lab_id')
        manager_name = request.query_params.get('manager_name')

        filters = {}
        if lab_id:
            filters["id"] = lab_id
        if manager_name:
            filters["manager__username__icontains"] = manager_name

        managers = ManageLab.objects.filter(**filters)
        
        serializer = ManagerDetailSerializer(managers, many=True)
        return Response(serializer.data)