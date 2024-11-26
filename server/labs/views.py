from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lab, ManageLab
from .serializers import LabSerializer, ManageLabSerializer, ManagerDetailSerializer
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
                description='Query by lab_name',
                required=False,
            ),
        ],
        responses={
            200: LabSerializer(many=True),
            400: {'error': 'Either lab_id or lab_name parameter is required'},
            404: {'error': 'Lab not found'},
        },
    )
    def get(self, request, format=None):
        lab_id = request.query_params.get('lab_id')
        lab_name = request.query_params.get('lab_name')

        lab_id = request.query_params.get('lab_id')
        lab_name = request.query_params.get('lab_name')

        if not lab_id and not lab_name:
            return Response({"error": "Either lab_id or lab_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        if lab_id:
            try:
                labs = Lab.objects.filter(id=lab_id)
            except Lab.DoesNotExist:
                return Response({"error": "Lab not found"}, status=status.HTTP_404_NOT_FOUND)
        elif lab_name:
            labs = Lab.objects.filter(name__icontains=lab_name)

        serializer = self.serializer_class(labs, many=True)
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
                required=True,
            ),
        ],
        responses={
            200: ManageLabSerializer(many=True),
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

        managers = ManageLab.objects.filter(lab=lab)
        #serializer = self.serializer_class(managers, many=True)
        serializer = ManagerDetailSerializer(managers, many=True)
        return Response(serializer.data)