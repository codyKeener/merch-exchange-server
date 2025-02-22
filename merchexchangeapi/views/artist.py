
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from merchexchangeapi.models import Artist

class ArtistView(ViewSet):

    def retrieve(self, request, pk):

        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):

        categories = Artist.objects.all()
        serializer = ArtistSerializer(categories, many=True)
        return Response(serializer.data)
    
    def create(self, request):

        artist = Artist.objects.create(
          name=request.data["name"],
          genre=request.data["genre"]
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.genre = request.data["genre"]
        artist.save()

        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ArtistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Artist
        fields = ('id', 'name', 'genre')
