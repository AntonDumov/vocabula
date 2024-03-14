# Part of speeches
NOUN = 'noun'
PRONOUN = 'pronoun'
VERB = 'verb'
ADJECTIVE = 'adjective'
ADVERB = 'adverb'
PREPOSITION = 'preposition'
CONJUNCTION = 'conjunction'
INTERJECTION = 'interjection'
DETERMINER = 'determiner'
PARTICLE = 'particle'

# Tuple of choices for the part_of_speech field
PART_OF_SPEECHES = (
    (NOUN, 'Noun'),
    (PRONOUN, 'Pronoun'),
    (VERB, 'Verb'),
    (ADJECTIVE, 'Adjective'),
    (ADVERB, 'Adverb'),
    (PREPOSITION, 'Preposition'),
    (CONJUNCTION, 'Conjunction'),
    (INTERJECTION, 'Interjection'),
    (DETERMINER, 'Determiner'),
    (PARTICLE, 'Particle')
)

MASCULINE = 'masculine'
FEMININE = 'feminine'
NEUTER = 'neuter'
NOT_APPLICABLE = 'not_applicable'  # For languages or words where gender is not applicable

# Tuple of choices for the word_gender field
WORD_GENDERS = (
    (MASCULINE, 'Masculine'),
    (FEMININE, 'Feminine'),
    (NEUTER, 'Neuter'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

SINGULAR = 'singular'
DUAL = 'dual'
TRIAL = 'trial'
PAUCAL = 'paucal'
QUADRAL = 'quadral'
QUINTAL = 'quintal'
PLURAL = 'plural'
SUPERPLURAL = 'superplural'
DISTRIBUTIVE_PLURAL = 'distributive_plural'

GRAMMATICAL_NUMBERS = [
    (SINGULAR, 'Singular'),
    (DUAL, 'Dual'),
    (TRIAL, 'Trial'),
    (PAUCAL, 'Paucal'),
    (QUADRAL, 'Quadral'),
    (QUINTAL, 'Quintal'),
    (PLURAL, 'Plural'),
    (SUPERPLURAL, 'Superplural'),
    (DISTRIBUTIVE_PLURAL, 'Distributive Plural')
]
