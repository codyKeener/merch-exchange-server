from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from merchexchangeapi.models import User, Listing, Artist, Category
# , WishlistLisitng

class ListingView(ViewSet):
  
  def retrieve(self, request, pk):
    
    try: 
      listing = Listing.objects.get(pk=pk)
      
      serializer = ListingSerializer(listing)
      return Response(serializer.data)
    
    except Listing.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    
    artist = request.query_params.get('artist', None)
    
    listings = Listing.objects.all()
    
    if artist is not None:
      listings = listings.filter(artist=artist)
    
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    
    artist = Artist.objects.get(pk=request.data["artist"])
    category = Category.objects.get(pk=request.data["category"])
    created_by = User.objects.get(uid=request.data["created_by"])
    
    listing = Listing.objects.create(
      title=request.data["title"],
      artist=artist,
      category=category,
      description=request.data["description"],
      price=request.data["price"],
      size=request.data["size"],
      condition=request.data["condition"],
      image=request.data["image"],
      created_by=created_by,
      ## created_at will automatically be set to current date and time
      published=request.data["published"]
      ## sold will be false by default when creating a new listing
    )
    
    serializer = ListingSerializer(listing)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    
    artist = Artist.objects.get(pk=request.data["artist"])
    category = Category.objects.get(pk=request.data["category"])
    created_by = User.objects.get(uid=request.data["created_by"])
    
    id = pk
    listing = Listing.objects.get(pk=pk)
    
    listing.title=request.data["title"]
    listing.artist=artist
    listing.category=category
    listing.description=request.data["description"]
    listing.price=request.data["price"]
    listing.size=request.data["size"]
    listing.condition=request.data["condition"]
    listing.image=request.data["image"]
    listing.created_by=created_by
    listing.published=request.data["published"]
    listing.sold=request.data["sold"]
    
    listing.save()
    
    serializer = ListingSerializer(listing)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    
    listing = Listing.objects.get(pk=pk)
    
    listing.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ListingSerializer(serializers.ModelSerializer):

  class Meta:
    model = Listing
    fields = ('id', 'title', 'artist', 'category', 'description', 'price', 'size', 'condition', 'image', 'created_by', 'created_at', 'published', 'sold')
    depth = 1
