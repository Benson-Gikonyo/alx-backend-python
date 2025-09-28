from rest_framework import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
# router.register(r"messages", MessageViewSet, basename="message")


conversation_router = routers.NestedDefaultRouter(
    router, r"conversations", lookup="conversations"
)
conversation_router.register(r"messages", MessageViewSet, basename="message")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversation_router.urls)),
]
