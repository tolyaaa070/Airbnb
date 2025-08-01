from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import PropertyFilter
from rest_framework.pagination import PageNumberPagination
from .permission import CheckRoleReview, CheckRole , CheckOffer, CheckOwner
from .models import UserProfile,Booking,Property,Review
from rest_framework import generics, viewsets, status , serializers , permissions
from .serializers import UserPofileSerializers, UserSerializer, LoginSerializer,PropertyCreateSerializers, ReviewSerializers, BookingListSerializers, PropertyListSerializers,PropertyDetailSerializers

class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PropertyListAPIViewSet(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializers
    filter_backends = [DjangoFilterBackend , OrderingFilter, SearchFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['price_per_night',]
    pagination_class = CustomPagination
    search_fields = ['city']

class PropertyDetailViewSet(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializers

class PropertyCreateViewSet(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializers
    # permission_classes = [CheckOffer]
    def create(self, request, *args, **kwargs):
        try :
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            property = serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        except serializers.ValidationError:
            return Response({'detail': 'Maalymat tuura emes berildi'}, status.HTTP_400_BAD_REQUEST)
        except NameError as e:
            return Response({'detail' : f' {e} , Oshibka v kode'} , status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'detail' : 'Server ne rabotaet'} , status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyUpdateAPIViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializers
    def create(self, request, *args, **kwargs):
        try :
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product = serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        except serializers.ValidationError:
            return Response({'detail': 'Maalymat tuura emes berildi'}, status.HTTP_400_BAD_REQUEST)
        except NameError as e:
            return Response({'detail' : f' {e} , Oshibka v kode'} , status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'detail' : 'Server ne rabotaet'} , status.HTTP_500_INTERNAL_SERVER_ERROR)
    permission_classes = [CheckOffer]


class BookingListViewSet(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializers

class BookingCreateViewSet(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializers
    # permission_classes = [CheckRoleReview]


class ReviewsListApiViewSet(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

class ReviewsCreateApiViewSet(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    # permission_classes =  [CheckRoleReview]
    def create(self, request, *args, **kwargs):
        try :
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product = serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        except serializers.ValidationError:
            return Response({'detail': 'Maalymat tuura emes berildi'}, status.HTTP_400_BAD_REQUEST)
        except NameError as e:
            return Response({'detail' : f' {e} , Oshibka v kode'} , status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'detail' : 'Server ne rabotaet'} , status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewEditApiViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserPofileSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

