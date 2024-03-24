from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from flashcards.views import DeckViewSet, FlashCardViewSet, MyProfileView

router = DefaultRouter()
router.register(r'decks', DeckViewSet, basename='deck')

deck_router = NestedSimpleRouter(router, r'decks', lookup='deck')
deck_router.register(r'flashcards', FlashCardViewSet, basename='deck-flashcards')

deck_view = TemplateView.as_view(template_name='flashcards/mydecks.html')
flashcards_view = TemplateView.as_view(template_name='flashcards/deck_flashcards.html')

app_name = 'flashcards'
urlpatterns = [
    path('api/my/', MyProfileView.as_view(), name="my-profile"),
    path('api/my/', include(router.urls)),
    path('api/my/', include(deck_router.urls)),
    path('my-decks/', deck_view, name='my-decks'),
    path('my-decks/<int:deck_id>/flashcards/', flashcards_view, name='deck-flashcards'),
]
