# Generated by Django 5.0.2 on 2024-03-06 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Language Name')),
                ('iso_code', models.CharField(max_length=10, unique=True, verbose_name='ISO Code')),
                ('google_tts_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Google TTS Language Name')),
                ('preferred_voice_male', models.CharField(blank=True, max_length=100, null=True, verbose_name='Preferred Male Voice')),
                ('preferred_voice_female', models.CharField(blank=True, max_length=100, null=True, verbose_name='Preferred Female Voice')),
                ('preferred_voice_neutral', models.CharField(blank=True, max_length=100, null=True, verbose_name='Preferred Neutral Voice')),
            ],
        ),
        migrations.CreateModel(
            name='PronunciationAudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(upload_to='pronunciations/', verbose_name='Audio File')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='pronunciations', related_query_name='pronunciation', to='dictionary.language', verbose_name='Language')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spelling', models.CharField(max_length=256, verbose_name='Word')),
                ('part_of_speech', models.CharField(choices=[('noun', 'Noun'), ('pronoun', 'Pronoun'), ('verb', 'Verb'), ('adjective', 'Adjective'), ('adverb', 'Adverb'), ('preposition', 'Preposition'), ('conjunction', 'Conjunction'), ('interjection', 'Interjection'), ('determiner', 'Determiner'), ('particle', 'Particle')], max_length=64, verbose_name='Part of speech')),
                ('gender', models.CharField(choices=[('masculine', 'Masculine'), ('feminine', 'Feminine'), ('neuter', 'Neuter'), ('not_applicable', 'Not Applicable')], max_length=64, verbose_name='Word Gender')),
                ('definition', models.TextField(blank=True)),
                ('phonetic_transcription', models.CharField(blank=True, help_text='Transcription of the word in phonetic language.', max_length=256, null=True, verbose_name='Phonetic Transcription')),
                ('image', models.ImageField(upload_to='')),
                ('specific_fields', models.JSONField(blank=True, default=list, help_text='Some additional fields specific to language', verbose_name='Specific fields')),
                ('antonyms', models.ManyToManyField(blank=True, related_query_name='antonym', to='dictionary.word', verbose_name='Antonyms')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='words', related_query_name='word', to='dictionary.language', verbose_name='Language')),
                ('pronunciation_audio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='words', related_query_name='word', to='dictionary.pronunciationaudio', verbose_name='Pronunciation Audio')),
                ('synonyms', models.ManyToManyField(blank=True, related_query_name='synonym', to='dictionary.word', verbose_name='Synonyms')),
                ('translations', models.ManyToManyField(blank=True, to='dictionary.word', verbose_name='Translations')),
            ],
        ),
        migrations.CreateModel(
            name='WordForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(max_length=124, verbose_name='Form Name')),
                ('form_value', models.CharField(max_length=124, verbose_name='Form Value')),
                ('phonetic_transcription', models.CharField(blank=True, help_text='Transcription of the form in phonetic language.', max_length=256, null=True, verbose_name='Phonetic Transcription')),
                ('grammatical_number', models.CharField(blank=True, choices=[('singular', 'Singular'), ('dual', 'Dual'), ('trial', 'Trial'), ('paucal', 'Paucal'), ('quadral', 'Quadral'), ('quintal', 'Quintal'), ('plural', 'Plural'), ('superplural', 'Superplural'), ('distributive_plural', 'Distributive Plural')], max_length=64, null=True, verbose_name='Grammatical Number')),
                ('gender', models.CharField(blank=True, choices=[('masculine', 'Masculine'), ('feminine', 'Feminine'), ('neuter', 'Neuter'), ('not_applicable', 'Not Applicable')], max_length=64, null=True, verbose_name='Word Gender')),
                ('pronunciation_audio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forms', related_query_name='form', to='dictionary.pronunciationaudio', verbose_name='Pronunciation Audio')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_forms', related_query_name='form', to='dictionary.word', verbose_name='Word Form')),
            ],
        ),
        migrations.CreateModel(
            name='FormTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='Text')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='dictionary.language')),
                ('pronunciation_audio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='form_translations', related_query_name='form_translation', to='dictionary.pronunciationaudio', verbose_name='Pronunciation Audio')),
                ('word_form', models.ManyToManyField(related_name='translations', related_query_name='translation', to='dictionary.wordform', verbose_name='Word Form')),
            ],
        ),
    ]
