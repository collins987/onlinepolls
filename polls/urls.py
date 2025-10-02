from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, VoteCreateAPIView

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')

urlpatterns = [
    path('', include(router.urls)),
    path('vote/', VoteCreateAPIView.as_view(), name='vote'),
]
