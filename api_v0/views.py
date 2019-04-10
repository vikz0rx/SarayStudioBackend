from rest_framework import status
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import *
from .renderers import *
from .serializers import *
from .exceptions import *

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'profile': {
                'firstname': user_data.get('firstname', request.user.profile.firstname),
                'lastname': user_data.get('lastname', request.user.profile.lastname),
                'middlename': user_data.get('middlename', request.user.profile.middlename),
                'birthdate': user_data.get('birthdate', request.user.profile.birthdate),
                'p_series': user_data.get('p_series', request.user.profile.p_series),
                'p_number': user_data.get('p_number', request.user.profile.p_number),
                'insurance': user_data.get('insurance', request.user.profile.insurance),
                'sms_notification': user_data.get('sms_notification', request.user.profile.sms_notification),
                'email_notification': user_data.get('email_notification', request.user.profile.email_notification)
            }
        }

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    renderer_classes = (ProfileJSONRenderer, )
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)