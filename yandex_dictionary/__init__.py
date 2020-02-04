
import requests
from .models import TextDescription
from . import errors


"""
API is used to get detailed dictionary entries from machine Yandex.Dictionaries.
https://yandex.ru/dev/dictionary/

Basic usage:
    >>> from yandex_dictionary_relative import Dictionary
    >>> dct = Dictionary("YOUR API KEY", "en", "ru")
    >>> text = dct.lookup("house")
    >>> text.is_found
    True
    >>> text.get_tr()
    ['дом', 'палата представителей', 'жилье', 'хаус', 'квартира', 'изба']
    >>> text.get_ex()
    ['auction house', "father's house", 'single storey house', 'old wooden house', 'build new houses', ...]
    >>> text.get_ex(translate=True)
    ['аукционный дом', 'отчий дом', 'одноэтажный дом', 'старый деревянный дом', 'строить новые дома', ...]
"""

API_URL = "https://dictionary.yandex.net/api/v1/dicservice.json"

# Translation directions supported by the service
LANGUAGE_PAIRS = (
    'be-be', 'be-ru', 'bg-ru', 'cs-cs', 'cs-en', 'cs-ru', 'da-en', 'da-ru', 'de-de', 'de-en', 'de-ru',
    'de-tr', 'el-en', 'el-ru', 'en-cs', 'en-da', 'en-de', 'en-el', 'en-en', 'en-es', 'en-et', 'en-fi',
    'en-fr', 'en-it', 'en-lt', 'en-lv', 'en-nl', 'en-no', 'en-pt', 'en-ru', 'en-sk', 'en-sv', 'en-tr',
    'en-uk', 'es-en', 'es-es', 'es-ru', 'et-en', 'et-ru', 'fi-en', 'fi-ru', 'fi-fi', 'fr-fr', 'fr-en',
    'fr-ru', 'hu-hu', 'hu-ru', 'it-en', 'it-it', 'it-ru', 'lt-en', 'lt-lt', 'lt-ru', 'lv-en', 'lv-ru',
    'mhr-ru', 'mrj-ru', 'nl-en', 'nl-ru', 'no-en', 'no-ru', 'pl-ru', 'pt-en', 'pt-ru', 'ru-be', 'ru-bg',
    'ru-cs', 'ru-da', 'ru-de', 'ru-el', 'ru-en', 'ru-es', 'ru-et', 'ru-fi', 'ru-fr', 'ru-hu', 'ru-it',
    'ru-lt', 'ru-lv', 'ru-mhr', 'ru-mrj', 'ru-nl', 'ru-no', 'ru-pl', 'ru-pt', 'ru-ru', 'ru-sk', 'ru-sv',
    'ru-tr', 'ru-tt', 'ru-uk', 'ru-zh', 'sk-en', 'sk-ru', 'sv-en', 'sv-ru', 'tr-de', 'tr-en', 'tr-ru',
    'tt-ru', 'uk-en', 'uk-ru', 'uk-uk', 'zh-ru'
)

# Search options (bitmask flags)
FLAGS_LOOKUP = {
    "FAMILY": 0x0001,
    "SHORT_POS": 0x0002,
    "MORPHO": 0x0004,
    "POS_FILTER": 0x0008,
}


class Dictionary:
    """Base class"""
    def __init__(self, api_key: str = None, from_lang: str = None, to_lang: str = None, ui: str = None):
        """
        :param api_key: your API-key from https://yandex.ru/dev/keys/get/?service=dict
        :type api_key: str
        :param from_lang: search language.
        :type from_lang: str
        :param to_lang: translation language.
        :type to_lang: str
            The service works not only with translation dictionaries.
            For example, you can specify the direction "ru-ru" or "en-en"
            and get all possible meanings of the searched word in Russian or English.
        :param ui: the language of the user interface in which names of the parts of speech will be displayed.
            Default - 'en'.
        :type ui: str
            Possible values for ui: 'en' (English), 'ru' (Russian), 'uk' (Ukrainian), 'tr' (Turkish).
        """
        self.api_key = api_key
        self.from_lang = from_lang.lower()
        self.to_lang = to_lang.lower()
        self.ui = ui or 'en'

    def lookup(self, text: str = None, **kwargs):
        """Searches for a word or phrase in the dictionary.
        :param text: The word or phrase to find in the dictionary.
        :type text: str
        :param kwargs: from_lang (str), to_lang (str), ui (str), flags (int)
            kwargs will not be saved on subsequent calls
        :rtype: models.TextDescription
        """
        from_lang = kwargs.pop('from_lang'.lower(), self.from_lang)
        to_lang = kwargs.pop('to_lang'.lower(), self.to_lang)
        ui = kwargs.pop('ui'.lower(), self.ui)
        flags = kwargs.pop('flags', 0)
        if text is None or from_lang is None or to_lang is None:
            raise errors.YandexDictionaryError("Не переданы все аргументы")
        url = "{}/lookup?key={}&lang={}-{}&text={}&ui={}&flags={}".format(
            API_URL, self.api_key, from_lang, to_lang, text, ui, flags
        )
        try:
            resp = requests.get(url=url)
        except requests.exceptions.ConnectionError as err:
            raise err

        if resp.status_code == 200:
            return TextDescription(text, resp.json())
        else:
            raise errors.YandexAPIError(resp.json())

    def get_langs(self):
        """
        :return: a list of translation directions supported by the service.
        :rtype: list
        """
        url = f"{API_URL}/getLangs?key={self.api_key}"
        resp = requests.get(url=url)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise errors.YandexAPIError(resp.json())
