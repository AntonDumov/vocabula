from rest_framework import viewsets

from .models import Deck, FlashCard
from .serializers import DeckSerializer, FlashCardSerializer


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer


class FlashCardViewSet(viewsets.ModelViewSet):
    serializer_class = FlashCardSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = FlashCard.objects.all()
        deck_id = self.kwargs.get('deck_id')
        if deck_id is not None:
            queryset = queryset.filter(deck_id=deck_id)
        return queryset
