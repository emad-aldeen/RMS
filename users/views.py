from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UsersSerializer, LoginSerializer
from .models import User, RandomUser
import random
from datetime import datetime

class UsersAPIView(generics.ListCreateAPIView):
    serializer_class = UsersSerializer
    queryset = User.objects.all()


    def post(self, request, *args, **kwargs):
        return Response({'error':'ERORR'}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request):
        if request.user.role == 'student':
            mates = User.objects.filter(cohort=request.user.cohort, is_superuser=False, role='student')
            data = {'Students': []}
        elif request.user.role == 'ta' or request.user.role == 'instructor':
            mates = User.objects.filter(cohort=request.user.cohort)
            data = {'Instructor': [], 'TAs': [], 'Students': []}

        
        for i in range(len(mates)):
            if mates[i].role == 'instructor':
                data['Instructor'].append({'username':mates[i].username})
            elif mates[i].role == 'ta':
                data['TAs'].append({'username':mates[i].username})
            else:
                data['Students'].append({'username':mates[i].username})

        return Response(data, status=status.HTTP_200_OK) 


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 

       
class RandomizerListAPIView(generics.ListAPIView):
        serializer_class = UsersSerializer
        queryset = User.objects.all()
        
        
        def get(self, request):
            today = datetime.today()
            invoice_for_today = RandomUser.objects.filter(created_at__year=today.year, created_at__month=today.month, created_at__day=today.day)

            if len(invoice_for_today) < 1:
                RandomUser.objects.all().delete()
            
            filtred_students = User.objects.filter(role='student', cohort=request.user.cohort)
            student = random.choice(filtred_students)

            old_students = RandomUser.objects.all()            
            if len(old_students) != len(filtred_students):
                old_stu_arr = []
                for i in range(len(old_students)):
                    old_stu_arr.append(old_students[i].username)

                while student.username in old_stu_arr:
                    student = random.choice(filtred_students)
                new_user = RandomUser.objects.create(username=student.username)
                new_user.save()
                return Response(new_user.username, status=status.HTTP_200_OK) 
            return Response({'congrats':'ALL students are voluntered today :)'}, status=status.HTTP_400_BAD_REQUEST)
