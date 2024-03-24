from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Deck, FlashCard, FlashCardsProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']
        read_only_fields = ['email']


class FlashCardsProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FlashCardsProfile
        fields = ['user']


class DeckSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Deck
        fields = ['id', 'name', 'description', 'flashcards_count', 'created_at', 'updated_at', 'profile']


class FlashCardSerializer(serializers.ModelSerializer):
    deck = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FlashCard
        fields = ['id', 'question', 'answer', 'deck']
