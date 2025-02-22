from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from merchexchangeapi.models import WishlistListing, User, Listing


class WishListListingView(ViewSet):

    def retrieve(self, request, pk):
        
        try:
          wishlist_listing = WishlistListing.objects.get(pk=pk)
          
          serializer = WishlistListingSerializer(wishlist_listing)
          return Response(serializer.data)
        except WishlistListing.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        
        wishlist_listings = WishlistListing.objects.all()
        
        serializer = WishlistListingSerializer(wishlist_listings, many=True)
        return Response(serializer.data)

    def create(self, request):
        
        user = User.objects.get(pk=request.data["user"])
        listing = Listing.objects.get(pk=request.data["listing"])

        wishlist_listing = WishlistListing.objects.create(
            user=user,
            listing=listing
        )

        serializer = WishlistListingSerializer(wishlist_listing)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        
        wishlist_listing = WishlistListing.objects.get(pk=pk)

        user = User.objects.get(pk=request.data["user"])
        listing = Listing.objects.get(pk=request.data["listing"])

        wishlist_listing.user = user
        wishlist_listing.listing = listing
        
        wishlist_listing.save()
        
        serializer = WishlistListingSerializer(wishlist_listing)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        
        wishlist_listing = WishlistListing.objects.get(pk=pk)
        
        wishlist_listing.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class WishlistListingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WishlistListing
        fields = 'id', 'user', 'listing'
        depth = 1
