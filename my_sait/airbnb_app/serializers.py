from .models import UserProfile, Booking, ImageProperty,Review, Property
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
class UserPofileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'avatar']
class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageProperty
        fields = ['image']
class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['property','guest','rating','comment','created_at']


class PropertyListSerializers(serializers.ModelSerializer):
    image = ImageSerializers(read_only=True,many=True)
    avg_rating = serializers.SerializerMethodField()
    count_reviews = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['id','image', 'city' , 'avg_rating', 'count_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_reviews(self, obj):
        return obj.get_count_reviews()

class PropertyDetailSerializers(serializers.ModelSerializer):
    image = ImageSerializers(read_only=True,many=True)
    owner = UserPofileSerializers()

    class Meta:
        model = Property
        fields = ['image','description','title', 'price_per_night',
                  'city', 'address','property_type','rules',
                  'owner','max_guests','bedrooms','bathrooms','is_active']
class PropertyCreateSerializers(serializers.ModelSerializer):
    image = ImageSerializers(read_only=True,many=True)

    class Meta:
        model = Property
        fields = ['image','description','title', 'price_per_night',
                  'city', 'address','property_type','rules',
                  'owner','max_guests','bedrooms','bathrooms','is_active']

class BookingListSerializers(serializers.ModelSerializer):
    check_in = serializers.DateTimeField(format='%d-%m-%y , %H:%M')
    check_out = serializers.DateTimeField(format='%d-%m-%y , %H:%M')
    created_at = serializers.DateTimeField(format='%d-%m-%y , %H:%M')



    class Meta :
        model = Booking
        fields = ['property','guest','check_in',
                  'check_out','created_at']

