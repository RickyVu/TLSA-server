from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lab, ManageLab
from .serializers import LabSerializer, ManageLabSerializer, ManagerDetailSerializer, LabGetSerializer, LabPatchSerializer
from classes.models import ClassLocation, TeachClass
from courses.models import CourseClass, CourseEnrollment
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from tlsa_server.permissions import IsAuthenticated, IsStudent, IsTeacher, IsManager
from rest_framework_simplejwt.authentication import JWTAuthentication

class LabView(APIView):
    serializer_class = LabSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['POST', 'PATCH', 'DELETE']:
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
            OpenApiParameter(
                name='personal',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Get personal labs',
                required=False,
            ),
        ],
        responses={
            200: LabSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        serializer_class = LabGetSerializer
        lab_id = request.query_params.get('lab_id')
        lab_name = request.query_params.get('lab_name')
        personal = request.query_params.get('personal')
        user = request.user

        labs = Lab.objects.all()

        if lab_id:
            labs = labs.filter(id=lab_id)
        if lab_name:
            labs = labs.filter(name__icontains=lab_name)
        if personal and personal.lower() == "true":
            if user.role == "student":
                enrolled_courses = CourseEnrollment.objects.filter(student=user).values_list('course_id', flat=True)
                enrolled_classes = CourseClass.objects.filter(course_id__in=enrolled_courses).values_list('class_instance_id', flat=True)
                lab_locations = ClassLocation.objects.filter(class_id__in=enrolled_classes).values_list('lab_id', flat=True)

                labs = labs.filter(id__in=lab_locations)
            elif user.role == "teacher":
                taught_classes = TeachClass.objects.filter(teacher_id=user).values_list('class_id', flat=True)
                lab_locations = ClassLocation.objects.filter(class_id__in=taught_classes).values_list('lab_id', flat=True)

                labs = labs.filter(id__in=lab_locations)
                
            elif user.role == "manager":
                managed_labs = ManageLab.objects.filter(manager=user).values_list('lab_id', flat=True)
                labs = labs.filter(id__in=managed_labs)

        serializer = serializer_class(labs, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=LabPatchSerializer,
        responses={
            200: LabSerializer,
            404: OpenApiExample(
                name="Lab not found",
                value={"message": "Lab not found."},
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
        lab_id = request.data.get('id')
        try:
            lab = Lab.objects.get(id=lab_id)
        except Lab.DoesNotExist:
            return Response({"message": "Lab not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LabPatchSerializer(lab, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Lab updated successfully.",
                    "lab": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='lab_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Lab ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Lab deleted",
                value={"message": "Lab deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Lab not found",
                value={"message": "Lab not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        lab_id = request.query_params.get('lab_id')
        try:
            lab = Lab.objects.get(id=lab_id)
        except Lab.DoesNotExist:
            return Response({"message": "Lab not found."}, status=status.HTTP_404_NOT_FOUND)

        lab.delete()
        return Response({"message": "Lab deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class LabManagerView(APIView):
    serializer_class = ManageLabSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['POST', 'PATCH', 'DELETE']:
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
                        "manager_user_id": manage_lab.manager.user_id,
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
            filters["lab_id"] = lab_id
        if manager_name:
            filters["manager__username__icontains"] = manager_name

        managers = ManageLab.objects.filter(**filters)
        
        serializer = ManagerDetailSerializer(managers, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='lab_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Lab ID to delete the manager for',
                required=True,
            ),
            OpenApiParameter(
                name='manager_user_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Manager user_id to delete',
                required=True,
            ),
        ]
    )
    def delete(self, request, format=None):
        lab_id = request.query_params.get('lab_id')
        manager_user_id = request.query_params.get('manager_user_id')

        try:
            manage_lab = ManageLab.objects.get(lab_id=lab_id, manager__user_id=manager_user_id)
        except ManageLab.DoesNotExist:
            return Response({"message": "ManageLab record not found."}, status=status.HTTP_404_NOT_FOUND)

        manage_lab.delete()
        return Response({"message": "ManageLab record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)