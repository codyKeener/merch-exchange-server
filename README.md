# Welcome to the Merch Exchange server!

This is the backend server for the Merch Exchange app.

## Get Started

Please see the [API Documentation](https://documenter.getpostman.com/view/35026527/2sAYdeNXjY)

1. Fork this repo
2. Clone repo to your machine
3. Activate the Pipenv environment with ```pipenv shell```
4. Install the dependencies using ```pipenv install```
5. Open the project in Visual Studio Code
6. Ensure that the correct interpreter is selected
7. Run ```python manage.py runserver``` to start the server

## About the User
- The ideal user for this application is anyone who wants to buy and sell used band merch while supporting their favorite artists
- They want to list their items for sale and browse listings from other users
- The problem this app solves is that it gives users a platform to safely interact with other music fans to buy and sell used band merch

## Features
- Create, Read, Update, and Delete listings
- Create, Read, Update, and Delete users
- Create, Read, Update, and Delete artists
- Create, Read, Update, and Delete categories
- Create, Read, Update, and Delete wishlistListings (many-to-many relationship for adding listings to your wishlist)

## Video Walkthrough of Simply Books Django server assessment
[Loom Video Walkthrough](https://www.loom.com/share/8c6ca4edc8ad4df78984c2cdca4b6098?sid=58197d6c-952f-4525-bb49-6ea242914eb0)

## Relevant Links
- Please see the [API Documentation](https://documenter.getpostman.com/view/35026527/2sAYdeNXjY)
- You can find the ERD [here](https://dbdiagram.io/d/Merch-Exchange-MVP-67b41eb1263d6cf9a08468dc)
- Check out this [Loom Video](https://www.loom.com/share/8c6ca4edc8ad4df78984c2cdca4b6098?sid=58197d6c-952f-4525-bb49-6ea242914eb0) for a demonstration of some the endpoints in Postman
- Check out this [Loom Video](https://www.loom.com/share/43337f176aa14cbda914b14e3fa5f2d7?sid=1eade0c8-d31f-4258-9f8c-bf01acea5026) to see the tests being run for all entities

## Code Snippet

<!-- // Listing Model -->

```
class Listing(models.Model):
  
  title = models.CharField(max_length=50)
  artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='listings')
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  description = models.CharField(max_length=280)
  price = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, validators=[MinValueValidator(Decimal('0.01'))])
  size = models.CharField(max_length=50)
  condition = models.CharField(max_length=50)
  image = models.URLField()
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
  created_at = models.DateTimeField(auto_now_add=True)
  published = models.BooleanField(default=False)
  sold = models.BooleanField(default=False)
```

## Contributors
- Cody Keener (https://github.com/codyKeener)
