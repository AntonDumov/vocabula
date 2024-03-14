from django.contrib import admin
from .models import Word, WordForm, FormTranslation, Language, PronunciationAudio


# Register your models here.

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('spelling', 'part_of_speech', 'gender', 'language')
    search_fields = ('spelling', 'translations__spelling', 'synonyms__spelling', 'antonyms__spelling')
    list_filter = ('part_of_speech', 'gender', 'language')
    raw_id_fields = ('translations', 'synonyms', 'antonyms')
    # filter_horizontal = ('translations', 'synonyms', 'antonyms')



@admin.register(WordForm)
class WordFormAdmin(admin.ModelAdmin):
    list_display = ('word', 'form_name', 'form_value')
    search_fields = ('word__spelling', 'form_name', 'form_value')
    list_filter = ('word__language',)


@admin.register(FormTranslation)
class FormTranslationAdmin(admin.ModelAdmin):
    list_display = ('text', 'language')
    search_fields = ('text', 'word_form__word__spelling', 'language__name')
    list_filter = ('language',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'iso_code',
        'google_tts_name',
        'preferred_voice_male',
        'preferred_voice_female',
        'preferred_voice_neutral'
    )
    search_fields = (
        'name',
        'iso_code',
        'google_tts_name',
        'preferred_voice_male',
        'preferred_voice_female',
        'preferred_voice_neutral'
    )
    list_filter = ('iso_code',)


@admin.register(PronunciationAudio)
class PronunciationAudioAdmin(admin.ModelAdmin):
    list_display = ('audio_file', 'description', 'date_added', 'date_updated')
    search_fields = ('description',)
    list_filter = ('date_added', 'date_updated')
