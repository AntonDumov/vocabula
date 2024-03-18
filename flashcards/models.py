from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Deck(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Deck Name"))
    description = models.TextField(verbose_name=_("Deck Description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='decks')

    def __str__(self):
        return f'{self.pk}:{self.name}'

    class Meta:
        verbose_name = _("Deck")
        verbose_name_plural = _("Decks")


class FlashCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField(verbose_name=_("FlashCard Question"))
    answer = models.TextField(verbose_name=_("FlashCard Answer"))

    def __str__(self):
        return f'{self.deck}:{self.question}'

    class Meta:
        verbose_name = _("FlashCard")
        verbose_name_plural = _("FlashCards")