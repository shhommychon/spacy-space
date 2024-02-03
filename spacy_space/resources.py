# Check spaCy document (https://spacy.io/usage/models#languages)
# for full details on language support.

_SUPPORTED_LANGUAGES = {
  # Afrikaans
  "af": {},

  # Albanian
  "sq": {},

  # Amharic
  "am": {},

  # Ancient Greek
  "grc": {},

  # Arabic
  "ar": {},

  # Armenian
  "hy": {},

  # Azerbaijani
  "az": {},

  # Basque
  "eu": {},

  # Bengali
  "bn": {},

  # Bulgarian
  "bg": {},

  # Catalan
  "ca": {
    # ref) https://spacy.io/models/ca
    "sm": "ca_core_news_sm", # small - 18MB of model trained with written text (news, media)
    "md": "ca_core_news_md", # medium - 46MB of model trained with written text (news, media)
    "lg": "ca_core_news_lg", # large - 547MB of model trained with written text (news, media)
    "trf": "ca_core_news_trf", # transformer - 435MB of model trained with written text (news, media)
  },

  # Chinese
  "zh": {
    # ref) https://spacy.io/models/zh
    "sm": "zh_core_web_sm", # small - 46MB of model trained with written text (blogs, news, comments)
    "md": "zh_core_web_md", # medium - 74MB of model trained with written text (blogs, news, comments)
    "lg": "zh_core_web_lg", # large - 575MB of model trained with written text (blogs, news, comments)
    "trf": "zh_core_web_trf", # transformer - 396MB of model trained with written text (blogs, news, comments)
  },

  # Croatian
  "hr": {
    # ref) https://spacy.io/models/hr
    "sm": "hr_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "hr_core_news_md", # medium - 64MB of model trained with written text (news, media)
    "lg": "hr_core_news_lg", # large - 220MB of model trained with written text (news, media)
  },

  # Czech
  "cs": {},

  # Danish
  "da": {
    # ref) https://spacy.io/models/da
    "sm": "da_core_news_sm", # small - 11MB of model trained with written text (news, media)
    "md": "da_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "da_core_news_lg", # large - 540MB of model trained with written text (news, media)
    "trf": "da_core_news_trf", # transformer - 420MB of model trained with written text (news, media)
  },

  # Dutch
  "nl": {
    # ref) https://spacy.io/models/nl
    "sm": "nl_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "nl_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "nl_core_news_lg", # large - 541MB of model trained with written text (news, media)
  },

  # English
  "en": {
    # ref) https://spacy.io/models/en
    "sm": "en_core_web_sm", # small - 12MB of model trained with written text (blogs, news, comments)
    "md": "en_core_web_md", # medium - 40MB of model trained with written text (blogs, news, comments)
    "lg": "en_core_web_lg", # large - 560MB of model trained with written text (blogs, news, comments)
    "trf": "en_core_web_trf", # transformer - 436MB of model trained with written text (blogs, news, comments)
  },

  # Estonian
  "et": {},

  # Finnish
  "fi": {
    # ref) https://spacy.io/models/fi
    "sm": "fi_core_news_sm", # small - 13MB of model trained with written text (news, media)
    "md": "fi_core_news_md", # medium - 65MB of model trained with written text (news, media)
    "lg": "fi_core_news_lg", # large - 220MB of model trained with written text (news, media)
  },

  # French
  "fr": {
    # ref) https://spacy.io/models/fr
    "sm": "fr_core_news_sm", # small - 15MB of model trained with written text (news, media)
    "md": "fr_core_news_md", # medium - 43MB of model trained with written text (news, media)
    "lg": "fr_core_news_lg", # large - 545MB of model trained with written text (news, media)
    "trf": "fr_dep_news_trf", # transformer - 379MB of model trained with written text (news, media)
  },

  # German
  "de": {
    # ref) https://spacy.io/models/de
    "sm": "de_core_news_sm", # small - 13MB of model trained with written text (news, media)
    "md": "de_core_news_md", # medium - 42MB of model trained with written text (news, media)
    "lg": "de_core_news_lg", # large - 541MB of model trained with written text (news, media)
    "trf": "de_dep_news_trf", # transformer - 391MB of model trained with written text (news, media)
  },

  # Greek
  "el": {
    # ref) https://spacy.io/models/el
    "sm": "el_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "el_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "el_core_news_lg", # large - 542MB of model trained with written text (news, media)
  },

  # Gujarati
  "gu": {},

  # Hebrew
  "he": {},

  # Hindi
  "hi": {},

  # Hungarian
  "hu": {},

  # Icelandic
  "is": {},

  # Indonesian
  "id": {},

  # Irish
  "ga": {},

  # Italian
  "it": {
    # ref) https://spacy.io/models/it
    "sm": "it_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "it_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "it_core_news_lg", # large - 541MB of model trained with written text (news, media)
  },

  # Japanese
  "ja": {
    # ref) https://spacy.io/models/ja
    "sm": "ja_core_news_sm", # small - 11MB of model trained with written text (news, media)
    "md": "ja_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "ja_core_news_lg", # large - 529MB of model trained with written text (news, media)
    "trf": "ja_core_news_trf", # transformer - 320MB of model trained with written text (news, media)
  },

  # Kannada
  "kn": {},

  # Korean
  "ko": {
    # ref) https://spacy.io/models/ko
    "sm": "ko_core_news_sm", # small - 13MB of model trained with written text (news, media)
    "md": "ko_core_news_md", # medium - 65MB of model trained with written text (news, media)
    "lg": "ko_core_news_lg", # large - 220MB of model trained with written text (news, media)
  },

  # Kyrgyz
  "ky": {},

  # Latin
  "la": {},

  # Latvian
  "lv": {},

  # Ligurian
  "lij": {},

  # Lithuanian
  "lt": {
    # ref) https://spacy.io/models/lt
    "sm": "lt_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "lt_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "lt_core_news_lg", # large - 541MB of model trained with written text (news, media)
  },

  # Lower Sorbian
  "dsb": {},

  # Luganda
  "lg": {},

  # Luxembourgish
  "lb": {},

  # Macedonian
  "mk": {
    # ref) https://spacy.io/models/mk
    "sm": "mk_core_news_sm", # small - 17MB of model trained with written text (news, media)
    "md": "mk_core_news_md", # medium - 42MB of model trained with written text (news, media)
    "lg": "mk_core_news_lg", # large - 310MB of model trained with written text (news, media)
  },

  # Malay
  "ms": {},

  # Malayalam
  "ml": {},

  # Marathi
  "mr": {},

  # Nepali
  "ne": {},

  # Norwegian Bokmål
  "nb": {
    # ref) https://spacy.io/models/nb
    "sm": "nb_core_news_sm", # small - 11MB of model trained with written text (news, media)
    "md": "nb_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "nb_core_news_lg", # large - 542MB of model trained with written text (news, media)
  },

  # Persian
  "fa": {},

  # Polish
  "pl": {
    # ref) https://spacy.io/models/pl
    "sm": "pl_core_news_sm", # small - 19MB of model trained with written text (news, media)
    "md": "pl_core_news_md", # medium - 47MB of model trained with written text (news, media)
    "lg": "pl_core_news_lg", # large - 547MB of model trained with written text (news, media)
  },

  # Portuguese
  "pt": {
    # ref) https://spacy.io/models/pl
    "sm": "pt_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "pt_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "pt_core_news_lg", # large - 541MB of model trained with written text (news, media)
  },

  # Romanian
  "ro": {
    # ref) https://spacy.io/models/ro
    "sm": "ro_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "ro_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "ro_core_news_lg", # large - 542MB of model trained with written text (news, media)
  },

  # Russian
  "ru": {
    # ref) https://spacy.io/models/ru
    "sm": "ru_core_news_sm", # small - 14MB of model trained with written text (news, media)
    "md": "ru_core_news_md", # medium - 39MB of model trained with written text (news, media)
    "lg": "ru_core_news_lg", # large - 489MB of model trained with written text (news, media)
  },

  # Sanskrit
  "sa": {},

  # Serbian
  "sr": {},

  # Setswana
  "tn": {},

  # Sinhala
  "si": {},

  # Slovak
  "sk": {},

  # Slovenian
  "sl": {
    # ref) https://spacy.io/models/sl
    "sm": "sl_core_news_sm", # small - 13MB of model trained with written text (news, media)
    "md": "sl_core_news_md", # medium - 64MB of model trained with written text (news, media)
    "lg": "sl_core_news_lg", # large - 221MB of model trained with written text (news, media)
    "trf": "sl_core_news_trf", # transformer - 397MB of model trained with written text (news, media)
  },

  # Spanish
  "es": {
    # ref) https://spacy.io/models/es
    "sm": "es_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "es_core_news_md", # medium - 40MB of model trained with written text (news, media)
    "lg": "es_core_news_lg", # large - 541MB of model trained with written text (news, media)
    "trf": "es_dep_news_trf", # transformer - 388MB of model trained with written text (news, media)
  },

  # Swedish
  "sv": {
    # ref) https://spacy.io/models/sv
    "sm": "sv_core_news_sm", # small - 12MB of model trained with written text (news, media)
    "md": "sv_core_news_md", # medium - 63MB of model trained with written text (news, media)
    "lg": "sv_core_news_lg", # large - 218MB of model trained with written text (news, media)
  },

  # Tagalog
  "tl": {},

  # Tamil
  "ta": {},

  # Tatar
  "tt": {},

  # Telugu
  "te": {},

  # Thai
  "th": {},

  # Tigrinya
  "ti": {},

  # Turkish
  "tr": {},

  # Ukrainian
  "uk": {
    # ref) https://spacy.io/models/uk
    "sm": "uk_core_news_sm", # small - 14MB of model trained with written text (news, media)
    "md": "uk_core_news_md", # medium - 65MB of model trained with written text (news, media)
    "lg": "uk_core_news_lg", # large - 220MB of model trained with written text (news, media)
    "trf": "uk_core_news_trf", # transformer - 391MB of model trained with written text (news, media)
  },

  # Upper Sorbian
  "hsb": {},

  # Urdu
  "ur": {},

  # Vietnamese
  "vi": {},

  # Yoruba
  "yo": {},

  # Multi-language
  "xx": {
    # ref) https://spacy.io/models/mk
    # "sm": "xx_ent_wiki_sm", # small - 10MB of model trained with Wikipedia
    # "sm": "xx_sent_ud_sm", # small - 4MB
  },
}

_LANG_ALIASES = {
  # Catalan
  "cat": "ca",

  # Chinese
  "zho": "zh",
  "cn": "zh",

  # Croatian
  "hrv": "hr",

  # Danish
  "dan": "da",

  # Dutch
  "nld": "nl",

  # English
  "eng": "en",

  # Finnish
  "fin": "fi",

  # French
  "fra": "fr",

  # German
  "deu": "de",
  "ger": "de",

  # Greek
  "ell": "el",
  "grk": "el",
  "gr": "el",

  # Italian
  "ita": "it",
  "itl": "it",

  # Japanese
  "jpn": "ja",

  # Korean
  "kor": "ko",
  "kr": "ko",

  # Lithuanian
  "lit": "lt",

  # Macedonian
  "mkd": "mk",

  # Norwegian Bokmål
  "nob": "nb",

  # Polish
  "pol": "pl",

  # Portuguese
  "por": "pt",

  # Romanian
  "ron": "ro",

  # Russian
  "rus": "ru",

  # Slovenian
  "slv": "sl",

  # Spanish
  "spa": "es",
  "sp": "es",

  # Swedish
  "swe": "sv",
  "sw": "sv",

  # Ukrainian
  "ukr": "uk",
}

_SIZE_ALIASES = {
  # small
  "s": "sm",
  "sml": "sm",
  "small": "sm",

  # middle
  "m": "md",
  "mid": "md",
  "mdl": "md",

  # large
  "l": "lg",
  "lr": "lg",
  "lrg": "lg",

  # transformer
  "t": "trf",
  "trans": "trf",
  "trsf": "trf",
  "trsfm": "trf",
}