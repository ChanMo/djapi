from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import *

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('group', GroupViewSet, basename='group')

urlpatterns = router.urls
urlpatterns += [
    path('profile/', ProfileView.as_view()),
    path('password/', ChangePasswordView.as_view()),
    path('password/reset/', ResetPasswordView.as_view()),

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
