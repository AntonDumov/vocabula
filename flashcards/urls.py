from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from flashcards import views as flashcards_views

router = DefaultRouter()
router.register(r'decks', flashcards_views.DeckViewSet)
router.register(r'cards', flashcards_views.FlashCardViewSet, basename='flashcards')

urlpatterns = [
    path('api/', include(router.urls)),
]