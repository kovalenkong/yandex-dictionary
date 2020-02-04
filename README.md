# yandex-dictionary
Python library to work with the [yandex-dictionary API](https://yandex.ru/dev/dictionary/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install yandex-dictionary.

```bash
pip install yandex-dictionary
```

## Base usage

```python
>>> from yandex_dictionary_relative import Dictionary
...
>>> dct = Dictionary("YOUR API KEY", "en", "ru")
>>> dct.lookup("house")
{"text": "house", "is_found": True}
```
Read more in docs/.