import json
import os.path
from typing import List

from tqdm import tqdm
from django.core.management import BaseCommand, CommandError
from django.db import transaction

from dictionary.consts import *
from dictionary.models import FormTranslation, Language, Word, WordForm

LANGUAGE_ENGLISH, _ = Language.objects.get_or_create(name="English", iso_code='en')
LANGUAGE_HEBREW, _ = Language.objects.get_or_create(name="Hebrew", iso_code='he')


def get_transcription_with_bold(text, bold_index):
    if text:
        return text[:bold_index] + f'<b>{text[bold_index]}</b>' + text[bold_index + 1:]
    else:
        return None


def save_adjective(spelling, gender, transcription):
    return Word.objects.get_or_create(
        spelling=spelling, gender=gender, phonetic_transcription=transcription, part_of_speech=ADJECTIVE,
        language=LANGUAGE_HEBREW
    )[0]


def get_number_and_gender_from_cell_form(cell_form):
    number, gender = tuple(map(lambda x: x.strip(), cell_form.split('-')))
    if number == 'Singular':
        number = SINGULAR
    else:
        number = PLURAL
    if gender == 'Masculine':
        gender = MASCULINE
    else:
        gender = FEMININE
    return number, gender


def create_django_objects_from_json(json_data):
    for word_data in json_data:
        spelling = word_data['word']
        data = word_data['data_en']
        with transaction.atomic():
            specific_fields = {}
            word = None

            pos_type = tuple(map(lambda x: x.strip(), data['paragraphs'][0].split('–')))
            if len(pos_type) == 2:
                pos, type = pos_type
            else:
                pos = pos_type[0]
                type = None

            if pos == 'Verb':
                pos = VERB
                specific_fields['binyan'] = type
            elif pos == 'Adjective':
                pos = ADJECTIVE
            elif pos == 'Preposition':
                pos = PREPOSITION
            elif pos == 'Noun':
                pos = NOUN
                if type and ',' in type:
                    specific_fields['pattern'], gender, *_ = type.split(', ')
                elif type:
                    gender = type
                else:
                    gender = NOT_APPLICABLE
            elif pos == 'Adverb':
                pos = ADVERB
                gender = NOT_APPLICABLE

            if len(data['paragraphs']) > 1:
                root = data['paragraphs'][1].split(':')[-1].replace(' - ', '').strip()
                specific_fields['root'] = root

            if len(data['paragraphs']) > 2:
                specifics = data['paragraphs'][2]
                specific_fields['additional_data'] = specifics
            translations = list(map(lambda x: x.strip(), data['lead_text'].replace(', ', ';').split(';')))

            if pos == VERB:
                infinitive_row = next(
                    (row for row in data['tables'][0]['rows'] if row['description'] == 'Infinitive'), None
                )
                if infinitive_row is not None:
                    infinitive = infinitive_row['cells'][0]['word']
                    transcription = get_transcription_with_bold(
                        infinitive_row['cells'][0]['transcription'], infinitive_row['cells'][0]['bold_letter_index']
                    )
                else:
                    infinitive = '-'
                    transcription = '-'

                word, _ = Word.objects.get_or_create(
                    spelling=infinitive,
                    part_of_speech=pos,
                    gender=NOT_APPLICABLE,
                    language=LANGUAGE_HEBREW,
                    phonetic_transcription=transcription
                )
                word.specific_fields = specific_fields
                word.save()
                for table in data['tables']:
                    if table['title'] == 'Meaning':
                        for row in table['rows']:
                            form_name = row['description']
                            for cell, cell_form in zip(row['cells'], table['header'][2:]):
                                number, gender = get_number_and_gender_from_cell_form(cell_form)

                                form, _ = WordForm.objects.get_or_create(
                                    word=word,
                                    form_name=form_name,
                                    form_value=cell['word'],
                                    grammatical_number=number,
                                    gender=gender,
                                    phonetic_transcription=get_transcription_with_bold(
                                        cell['transcription'], cell['bold_letter_index']
                                    )
                                )
                                if cell['meaning'] is not None:
                                    form_translation, _ = FormTranslation.objects.get_or_create(
                                        text=cell['meaning'],
                                        language=LANGUAGE_ENGLISH,
                                    )
                                    form_translation.word_form.add(form)
            elif pos == ADJECTIVE:
                for table in data['tables']:
                    if table['title'] == 'Meaning':
                        first_row = table['rows'][0]
                        word_created = False
                        for cell, cell_form in zip(first_row['cells'], table['header']):
                            number, gender = get_number_and_gender_from_cell_form(cell_form)
                            if cell['transcription']:
                                transcription = get_transcription_with_bold(
                                    cell['transcription'], cell['bold_letter_index']
                                    )
                            else:
                                transcription = ''
                            if cell['word'] and not word_created:
                                word = save_adjective(
                                    spelling=cell['word'],
                                    gender=gender,
                                    transcription=transcription,
                                )
                                word.specific_fields = specific_fields
                                word.save()
                                word_created = True
                            if cell['word']:
                                word_form, _ = WordForm.objects.get_or_create(
                                    word=word,
                                    form_name=cell_form,
                                    form_value=cell['word'],
                                    phonetic_transcription=transcription,
                                    grammatical_number=number,
                                    gender=gender
                                )
                                if cell['meaning']:
                                    word_form_translation, _ = FormTranslation.objects.get_or_create(
                                        text=cell['meaning'],
                                        language=LANGUAGE_ENGLISH
                                    )
                                    word_form_translation.word_form.add(word_form)
            elif pos == NOUN:
                table_wo_affixes = next((table for table in data['tables'] if table['title'] in ['Forms without pronominal affixes', 'Meaning']), None)
                if table_wo_affixes:
                    main_cell = table_wo_affixes['rows'][0]['cells'][0]
                    word, _ = Word.objects.get_or_create(
                        spelling=main_cell['word'],
                        part_of_speech=pos,
                        gender=gender,
                        phonetic_transcription=main_cell['transcription'],
                        language=LANGUAGE_HEBREW,
                        specific_fields=specific_fields
                    )
                    for row in table_wo_affixes['rows']:
                        form_name = row['description']
                        for cell, number in zip(row['cells'], table_wo_affixes['header'][1:]):
                            form, _ = WordForm.objects.get_or_create(
                                word=word,
                                form_name=form_name,
                                form_value=cell['word'],
                                grammatical_number=number,
                                gender=gender,
                                phonetic_transcription=get_transcription_with_bold(
                                    cell['transcription'], cell['bold_letter_index']
                                )
                            )
                            if cell['meaning'] is not None:
                                form_translation, _ = FormTranslation.objects.get_or_create(
                                    text=cell['meaning'],
                                    language=LANGUAGE_ENGLISH,
                                )
                                form_translation.word_form.add(form)
            elif pos == ADVERB:
                word, _ = Word.objects.get_or_create(
                    spelling=spelling,
                    part_of_speech=pos,
                    gender=gender,
                    language=LANGUAGE_HEBREW
                )

            elif pos == PREPOSITION:
                word, _ = Word.objects.get_or_create(
                    spelling=spelling,
                    part_of_speech=pos,
                    gender=NOT_APPLICABLE,
                    language=LANGUAGE_HEBREW
                )
                if data['tables']:
                    table = data['tables'][0]
                    for row in table['rows']:
                        for cell, cell_form in zip(row['cells'], table['header'][1:]):
                            person = row['description']
                            form, _ = WordForm.objects.get_or_create(
                                word=word,
                                form_value=cell['word'],
                                form_name=f'{cell_form} / {person}'
                            )
                            if cell['transcription']:
                                form.phonetic_transcription = get_transcription_with_bold(cell['transcription'], cell['bold_letter_index'])
                                form.save()
                            form_translation, _ = FormTranslation.objects.get_or_create(
                                language=LANGUAGE_ENGLISH,
                                text=cell['meaning']
                            )
                            form_translation.word_form.add(form)

            if word:
                for translation in translations:
                    translation_word = Word.objects.create(
                        spelling=translation,
                        part_of_speech=pos,
                        language=LANGUAGE_ENGLISH,
                    )
                    if not word.translations.contains(translation_word):
                        word.translations.add(translation_word)
            else:
                print('No word')


def import_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        create_django_objects_from_json(data)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Directory containing JSON files')

    @transaction.atomic
    def handle(self, *args, **options):
        directory = options['directory']
        if not os.path.isdir(directory):
            raise CommandError(f'The directory "{directory}" does not exist')

        for filename in tqdm(os.listdir(directory)):
            if filename.endswith('.json'):
                import_json(os.path.join(directory, filename))
