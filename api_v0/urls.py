from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'photographs', PhotographsViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users', RegistrationAPIView.as_view()),
    path('users/login', LoginAPIView.as_view()),
    path('profiles/<str:username>', ProfileRetrieveAPIView.as_view()),
]