from rest_framework import serializers
from .models import Deck, FlashCard


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['id', 'name', 'description']


class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = ['id', 'question', 'answer', 'deck']
