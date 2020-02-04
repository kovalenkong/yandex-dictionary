from . import errors


class TextDescription:
    """Class for working with text. Created with Dictionary.lookup()"""
    def __init__(self, text: str = None, description: dict = None):
        if type(text) is not str or type(description) is not dict:
            raise errors.YandexDictionaryError
        h, d = description.keys() if len(description) == 2 else [None, None]
        if h != 'head' or d != 'def':
            raise errors.YandexDictionaryError

        self.__text = text
        self.__description = description

    @property
    def text(self):
        """
        :return: The text of the article, translation or synonym.
        :rtype: str
        """
        try:
            return self.__description.get('def')[0].get('text')
        except (IndexError, KeyError):
            return None

    @property
    def dict_array(self):
        """
        :return: An array of dictionary entries.
        :rtype: list
        """
        try:
            return self.__description.get('def')
        except (IndexError, KeyError):
            return []

    @property
    def pos(self):
        """
        :return: Part of speech.
        :rtype: str or None
        """
        try:
            return self.__description.get('def')[0].get('pos')
        except (IndexError, KeyError):
            return None

    @property
    def gen(self):
        """
        :return: Gender of a noun for those languages ​​where it is relevant.
        :rtype: str or None
        """
        try:
            return self.__description.get('def')[0].get('gen')
        except (IndexError, KeyError):
            return None

    @property
    def anm(self):
        """
        :return: Animate or inanimate.
        :rtype: str or None
        """
        try:
            return self.__description.get('def')[0].get('anm')
        except (IndexError, KeyError):
            return None

    @property
    def ts(self):
        """
        :return: The transcription of the search word.
        :rtype: str or None
        """
        try:
            return self.__description.get('def')[0].get('ts')
        except (IndexError, KeyError):
            return None

    def get_tr(self, *args) -> list:
        """All translations.
        :param args: text, pos, syn, mean, ex
        :return: list of translations or list with dicts if args
        :rtype: list
        """
        try:
            if args:
                return [{arg: tr_l.get(arg) for arg in args} for tr_l in self.__description.get('def')[0].get('tr')]
            else:
                return [tr_l.get('text') for tr_l in self.__description.get('def')[0].get('tr')]
        except (IndexError, KeyError):
            return list()

    def get_syn(self, *args) -> list:
        """All synonyms.
        :param args: text, pos, gen
            If you want to use all available args, you can call get_tr("syn")
        :return: list of synonyms or list with dicts if args
        :rtype: list
        """
        try:
            tr = self.__description.get('def')[0].get('tr')
            syn = [x.get('syn') for x in tr if x.get('syn') is not None]
            if args:
                return [{arg: tr_list.get(arg) for arg in args} for syn_list in syn for tr_list in syn_list]
            else:
                return [syn_list.get('text') for tr_list in syn for syn_list in tr_list]
        except (IndexError, KeyError):
            return list()

    def get_mean(self) -> list:
        """All meanings.
        :return: list of all meanings
        :rtype: list
        """
        try:
            tr = self.__description.get('def')[0].get('tr')
            mean = [tr_list.get('mean') for tr_list in tr if tr_list.get('mean') is not None]
            return [mean_list.get('text') for tr_list in mean for mean_list in tr_list]
        except (IndexError, KeyError):
            return list()

    def get_ex(self, *args, **kwargs) -> list:
        """All examples.
        :param args: text, tr
            If you indicate args, 'translate' :argument will be ignored.
            If you want to use all available args, you can call get_tr("ex")
        :param kwargs: translate (bool, default is False)
            If False - all examples will be used in language you search.
            If True - all examples will be used in language you translate.
        :return: list of all examples or list with dicts if args
        :rtype: list
        """
        translate = kwargs.pop('translate', False)
        try:
            tr = self.__description.get('def')[0].get('tr')
            ex = [x.get('ex') for x in tr if x.get('ex') is not None]
            if args:
                return [{arg: ex_list.get(arg) for arg in args} for tr_list in ex for ex_list in tr_list]
            else:
                if translate is True:
                    ex_list = [ex_list.get('tr') for tr_list in ex for ex_list in tr_list if ex_list.get('tr') is not None]
                    return [ex_tr_list.get('text') for ex_list in ex_list for ex_tr_list in ex_list]
                else:
                    return [ex_list.get('text') for tr_list in ex for ex_list in tr_list]
        except (IndexError, KeyError):
            return list()

    def json(self) -> dict:
        """
        :return: Original JSON API response
        :rtype: dict
        """
        return self.__description

    @property
    def is_found(self) -> bool:
        """
        :return: Was the text found (True or False)
        :rtype: bool
        """
        return True if len(self.__description.get('def')) > 0 else False

    def __str__(self):
        return {"text": self.__text, "is_found": self.is_found}.__str__()

    def __repr__(self):
        return {"text": self.__text, "is_found": self.is_found}.__str__()
