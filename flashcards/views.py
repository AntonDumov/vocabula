from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Deck, FlashCard, FlashCardsProfile
from .permissions import IsOwnerOrReadOnly
from .serializers import DeckSerializer, FlashCardSerializer, FlashCardsProfileSerializer


class MyProfileView(RetrieveUpdateAPIView):
    serializer_class = FlashCardsProfileSerializer

    def get_object(self):
        return FlashCardsProfile.objects.get(
            user=self.request.user
        )


class DeckViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
    DestroyModelMixin
    ):
    serializer_class = DeckSerializer

    def get_queryset(self):
        return Deck.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            profile=FlashCardsProfile.objects.get(
                user=self.request.user
            )
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.profile.user == request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        instance = self.get_object()
        if not instance.profile.user == self.request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()


class FlashCardViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = FlashCardSerializer

    def get_queryset(self):
        return FlashCard.objects.filter(
            deck_id=self.kwargs['deck_pk'],
            deck__profile__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            deck=Deck.objects.get(
                id=self.kwargs['deck_pk']
            )
        )
