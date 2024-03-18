from django.contrib import admin
from .models import Deck, FlashCard


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'created_at', 'updated_at')

@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('deck', 'question', 'answer')
    search_fields = ('deck', 'question', 'answer')
