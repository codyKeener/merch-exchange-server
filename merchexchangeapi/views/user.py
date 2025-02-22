from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from merchexchangeapi.models import User

class UserView(ViewSet):
  
  def retrieve(self, request, pk):
    
      try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
      except User.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
      
      uid = request.query_params.get('uid', None)
          
      users = User.objects.all()
      
      ## FOR GETTING USER BY UID
      if uid is not None:
        users = users.filter(uid=uid)
        
      serializer = UserSerializer(users, many=True)
        
      return Response(serializer.data)
  
  def create(self, request):

      user = User.objects.create(
        username=request.data["username"],
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
        email=request.data["email"],
        bio=request.data["bio"],
        uid=request.data["uid"],
        is_admin=request.data["is_admin"],
        is_artist=request.data["is_artist"]
    )
      serializer = UserSerializer(user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):

      user = User.objects.get(pk=pk)
      user.username=request.data["username"]
      user.first_name=request.data["first_name"]
      user.last_name=request.data["last_name"]
      user.email=request.data["email"]
      user.bio=request.data["bio"]
      user.uid=request.data["uid"]
      user.is_admin=request.data["is_admin"]
      user.is_artist=request.data["is_artist"]
      user.save()
    
      serializer = UserSerializer(user)
      return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'email', 'bio', 'uid', 'is_admin', 'is_artist')
    depth = 1
