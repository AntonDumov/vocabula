from django.shortcuts import render
from rest_framework import viewsets

from .models import Deck, FlashCard
from .serializers import DeckSerializer, FlashCardSerializer


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer


class FlashCardViewSet(viewsets.ModelViewSet):
    serializer_class = FlashCardSerializer

    def queryset(self, *args, **kwargs):
        return FlashCard.objects.filter(deck=self.kwargs['deck_pk'])
