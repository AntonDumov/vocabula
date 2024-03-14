from django.db import models
from django.utils.translation import gettext_lazy as _

from dictionary.consts import GRAMMATICAL_NUMBERS, PART_OF_SPEECHES, WORD_GENDERS


# Create your models here.

class Word(models.Model):
    spelling = models.CharField(
        max_length=256,
        verbose_name=_('Word')
    )
    translations = models.ManyToManyField(
        'self', blank=True,
        verbose_name=_('Translations'),
    )
    synonyms = models.ManyToManyField(
        "self", related_query_name='synonym', blank=True,
        verbose_name=_('Synonyms')
    )
    antonyms = models.ManyToManyField(
        "self", related_query_name='antonym', blank=True,
        verbose_name=_('Antonyms')
    )
    part_of_speech = models.CharField(
        choices=PART_OF_SPEECHES, max_length=64,
        verbose_name=_('Part of speech')
    )
    gender = models.CharField(
        choices=WORD_GENDERS, max_length=64,
        verbose_name=_('Word Gender')
    )
    definition = models.TextField(blank=True)
    phonetic_transcription = models.CharField(
        max_length=256,
        verbose_name=_('Phonetic Transcription'),
        help_text=_('Transcription of the word in phonetic language.'),
        blank=True, null=True
    )
    language = models.ForeignKey(
        'Language',
        on_delete=models.RESTRICT,
        verbose_name=_('Language'),
        related_name='words',
        related_query_name='word'
    )
    pronunciation_audio = models.ForeignKey(
        'PronunciationAudio',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Pronunciation Audio'),
        related_name='words',
        related_query_name='word'
    )
    image = models.ImageField()

    specific_fields = models.JSONField(
        verbose_name=_('Specific fields'),
        help_text=_('Some additional fields specific to language'),
        blank=True, default=list
    )

    def __str__(self):
        return self.spelling


class WordForm(models.Model):
    word = models.ForeignKey(
        'Word', on_delete=models.CASCADE, related_name='word_forms',
        related_query_name='form', verbose_name=_('Word Form')
    )
    form_name = models.CharField(  # e.g., "Plural", "Comparative", "Past Tense"
        max_length=124,
        verbose_name=_('Form Name')
    )
    form_value = models.CharField(
        max_length=124,
        verbose_name=_('Form Value')
    )
    phonetic_transcription = models.CharField(
        max_length=256,
        verbose_name=_('Phonetic Transcription'),
        help_text=_('Transcription of the form in phonetic language.'),
        blank=True, null=True
    )
    pronunciation_audio = models.ForeignKey(
        'PronunciationAudio',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Pronunciation Audio'),
        related_name='forms',
        related_query_name='form'
    )

    grammatical_number = models.CharField(
        choices=GRAMMATICAL_NUMBERS, max_length=64,
        verbose_name=_('Grammatical Number'), null=True, blank=True
    )

    gender = models.CharField(
        choices=WORD_GENDERS, max_length=64,
        verbose_name=_('Word Gender'), null=True, blank=True
    )

    def __str__(self):
        return f"{self.word.spelling} - {self.form_name}: {self.form_value}"


class FormTranslation(models.Model):
    word_form = models.ManyToManyField(
        'WordForm',
        related_name='translations',
        related_query_name='translation', verbose_name=_('Word Form')
    )
    language = models.ForeignKey('Language', on_delete=models.RESTRICT)
    text = models.TextField(max_length=200, verbose_name=_('Text'))
    pronunciation_audio = models.ForeignKey(
        'PronunciationAudio',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Pronunciation Audio'),
        related_name='form_translations',
        related_query_name='form_translation'
    )

    def __str__(self):
        return f"{self.text} [{self.language}]"


class Language(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Language Name'))
    iso_code = models.CharField(max_length=10, verbose_name=_('ISO Code'), unique=True)
    google_tts_name = models.CharField(
        max_length=100, verbose_name=_('Google TTS Language Name'),
        blank=True, null=True
    )
    preferred_voice_male = models.CharField(
        max_length=100, verbose_name=_('Preferred Male Voice'),
        blank=True, null=True
    )
    preferred_voice_female = models.CharField(
        max_length=100, verbose_name=_('Preferred Female Voice'),
        blank=True, null=True
    )
    preferred_voice_neutral = models.CharField(
        max_length=100, verbose_name=_('Preferred Neutral Voice'),
        blank=True, null=True
    )

    def __str__(self):
        return self.name


class PronunciationAudio(models.Model):
    audio_file = models.FileField(upload_to='pronunciations/', verbose_name=_('Audio File'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Description'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Added'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date Updated'))

    language = models.ForeignKey(
        'Language', verbose_name=_('Language'),
        related_name='pronunciations', related_query_name='pronunciation',
        on_delete=models.RESTRICT,
    )

    def __str__(self):
        return self.description or "Pronunciation Audio"
