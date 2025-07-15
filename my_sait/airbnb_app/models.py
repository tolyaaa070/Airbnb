from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('арендодатель' ,'арендодатель'),
        ('гость','гость')
    )
    phone_number = PhoneNumberField()
    role = models.CharField(choices=ROLE_CHOICES, default='гость')
    avatar = models.ImageField(upload_to='users_avatar/', null=True, blank=True)

    def __str__(self):
        return f'{self.role},{self.username}, {self.last_name},{self.first_name}'


class Property(models.Model):
    description = models.TextField()
    title = models.CharField()
    price_per_night = models.IntegerField()
    city = models.CharField()
    address = models.CharField()
    PROPERTY_TYPE_CHOICES=(
        ('apartment','apartment'),
        ('house','house'),
        ('studio','studio')
    )
    property_type = models.CharField(choices=PROPERTY_TYPE_CHOICES)
    RULES_CHOICES=(
        ('no_smoking','no_smoking'),
        ('pets_allowed','pets_allowed'),
    )
    rules = models.CharField(choices=RULES_CHOICES)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='properties')
    max_guests = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.owner},{self.city}'

    def get_avg_rating(self):
        ratin=self.reviews_property.all()
        if ratin.exists():
            return round(sum([i.rating for i in ratin]) / ratin.count(),1)
        return 0
    def get_count_reviews(self):
        return self.reviews_property.count()

class ImageProperty(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name ='image')
    image = models.ImageField(upload_to='property_image/')

class Booking(models.Model):
    property= models.ForeignKey(Property, on_delete=models.CASCADE)
    guest  = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    STATUS_CHOICES = (
        ('pending','pending'),
        ('approved','approved'),
        ('rejected','rejected'),
        ('cancelled','cancelled')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.property}, {self.guest}'

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE , related_name = 'reviews_property')
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.property},{self.guest}'

