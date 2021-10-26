from rest_framework.response import Response
from .serializers import PointSerializer
from .models import Point
from rest_framework import generics, status
from users.models import User
from rest_framework.permissions import  IsAuthenticated


class PointView(generics.ListCreateAPIView):

    serializer_class = PointSerializer
    queryset = Point.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        if request.user.role == 'instructor' or request.user.role == 'ta':
            points = Point.objects.filter(owner__cohort=request.user.cohort)
        else:
            points = Point.objects.filter(owner=request.user)
              
        if len(points) == 0:
            return Response({'error':'you have no points'}, status=status.HTTP_204_NO_CONTENT)

        data = []
        for i in range(len(points)):
            data.append(self.serializer_class(points[i]).data)

        return Response(data, status=status.HTTP_200_OK) 
    
    def post(self, request):

        if request.user.role == 'ta':
            owner = User.objects.get(username=request.data['owner'])
            owner.total_points += 1
            owner.fulfilled_points += 1
            owner.save()
            return self.create(request)

        return Response({'error':'sorry dude .. you had no permission!'}, status=status.HTTP_403_FORBIDDEN)
    

class PointDetailsView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PointSerializer
    queryset = Point.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.role == 'instructor' or request.user.role == 'ta':
            return self.retrieve(request)
        return Response({'error':'no .. you cant get points from this route.. :/'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        # import pdb
        # pdb.set_trace()
        point = Point.objects.get(id=id)
        
        if request.user == point.owner:

            if request.data['is_approved'] and not point.is_confirmed:
                return Response({'error':'point should be confirmed first'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if point.is_approved:
                    return Response({'error':'point already approved, you cant donate it or edit it!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                if request.data['is_approved']:
                    point.is_approved = True
                    point.save()
                    request.user.fulfilled_points -= 1
                    request.user.save()
                    return Response({'success':'is approved successfuly..'}, status=status.HTTP_200_OK)

            if point.is_confirmed:
                return Response({'error':'point already confirmed, you cant donate it or edit it!'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            

            if request.data['is_donated']:
                if len(request.data['donated_to']) < 1:
                    return Response({'error':'make sure to fill donated_to field'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    new_user = User.objects.get(username=request.data['donated_to'])
                except:
                    return Response({'error':'user NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)

                if new_user.cohort != request.user.cohort:
                    return Response({'error':'this student are not in your class!!'}, status=status.HTTP_404_NOT_FOUND)
                
                if new_user.role == 'ta' or new_user.role == 'instructor':
                    return Response({'error':'thx, but Instructional team dosent use points! :)'}, status=status.HTTP_406_NOT_ACCEPTABLE)

                new_point = Point.objects.create(donated_from=request.user.username, owner=new_user, notes=request.data['notes'])
                new_user.fulfilled_points += 1
                new_user.save()
                request.user.fulfilled_points -= 1
                request.user.save()
                self.destroy(request)
                new_point.save()
                return Response({'success':'point transferd successfuly..'}, status=status.HTTP_200_OK)
        
            if request.data['is_confirmed']:
                return Response({'error':'only instructional team can confirm your point!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if request.data['owner'] != point.owner.username:
                return Response({'error':'you can dontae this point but not change the owner directly!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            return self.update(request)
        return Response({'error':'ONLY point owner can edit it'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, *args, **kwargs):
        if request.user.role == 'ta':
            self.destroy(request, *args, **kwargs)
        return Response({'error':'only TA can delete point!'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def patch(self, request, id):
        if request.user.role == 'ta':
            point = Point.objects.get(id=id)
            if not point.is_confirmed:
                point.is_confirmed = True
                point.save()
                return Response({'success':'point confirmed..'}, status=status.HTTP_200_OK)
            return Response({'error':'point is already confirmed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'you can only confirm points by this method'}, status=status.HTTP_403_FORBIDDEN)
    