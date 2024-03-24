from rest_framework import permissions

from flashcards.models import Deck, FlashCardsProfile


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, FlashCardsProfile):
            return obj.user == request.user
        elif isinstance(obj, Deck):
            return obj.profile.user == request.user
        return False
