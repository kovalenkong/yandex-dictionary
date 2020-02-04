# yandex-dictionary
## Установка
```bash
pip install yandex-dictionary
```
## Быстрый старт
```python
>>> from yandex_dictionary_relative import Dictionary
...
>>> dct = Dictionary("API key", 'ru', 'en')
>>> dct.lookup('программирование')
{"text": "программирование", "is_found": True}
```

### Класс `Dictionary`
Аргументы, которые принимает класс при вызове: `api_key`, `from_lang`, `to_lang`, `ui`.
- `api_key`: API-ключ, можно получить на [yandex](https://yandex.ru/dev/keys/get/?service=dict);
- `from_lang`, `to_lang`: языковая пара, при вызове `lookup()` можно переопределять;
- `ui`: язык интерфейса пользователя, на котором будут отображаться названия частей речи. По умолчанию `en`.

Вызов `lookup()` принимает следуюшие параметры:
- `text`: текст для поиска;
- `from_lang`, `to_lang`: языковая пара;
- `ui`: язык интерфейса частей речи.

Получить список доступных языковых пар:
```python
dct.get_langs()
```

### Класс `models.Dictionary`
Создается экземпляр класса при вызове `lookup()`
Доступные методы и атрибуты:
- `json()`: искомый ответ API-запроса в формате json;
- `get_tr()`: массив с переводами;
- `get_syn()`: массив с синонимами;
- `get_men()`: массив значений исходного текста;
- `get_ex()`: массив с примерами.
- `is_found`: возвращает `True` если словарный массив был найден;
- `anm`: одушевленность (возвращает `None` если одушевленность отсутствует);
- `gen`: род (возвращает `None` если род отсутствует);
- `pos`: часть речи (возвращает `None` если отсутствует);
- `ts`: транскрипция (возвращает `None` если отсутствует);
- `dict_array`: массив словарных статей.

#### Пример использования
```python
>>> text = dct.lookup('дом', from_lang='ru', to_lang='en', ui='ru')

>>> text.is_found
True

>>> text.json()
{'head': {}, 'def': [{'text': 'дом', 'pos': 'noun', 'gen': 'м', 'anm': 'неодуш', 'tr': [{'text': 'house', 'pos': 'noun', 'syn': [{'text': 'building', 'pos': 'noun'}], 'mean': [{'text': 'домик'}, {'text': 'здание'}], 'ex': [{'text': 'белый дом', 'tr': [{'text': 'white house'}]}, {'text': 'многоквартирный дом', 'tr': [{'text': 'apartment building'}]}]}, {'text': 'home', 'pos': 'noun', 'syn': [{'text': 'household', 'pos': 'noun'}], 'ex': [{'text': 'детский дом', 'tr': [{'text': "children's home"}]}, {'text': 'императорский дом', 'tr': [{'text': 'imperial household'}]}]}, {'text': 'dwelling', 'pos': 'noun', 'mean': [{'text': 'жилище'}], 'ex': [{'text': 'сельский дом', 'tr': [{'text': 'rural dwelling'}]}]}, {'text': 'door', 'pos': 'noun', 'mean': [{'text': 'дверь'}]}, {'text': 'premise', 'pos': 'noun', 'mean': [{'text': 'помещение'}]}, {'text': 'establishment', 'pos': 'noun', 'mean': [{'text': 'создание'}]}]}]}

>>> text.pos
существительное

>>> text.anm
неодуш

# Получаем список переводов 
>>> text.get_tr()
['house', 'home', 'dwelling', 'door', 'premise', 'establishment']

# Список с вложенными словарями переводов с перечислением аргументов
>>> text.get_tr('text', 'pos')
[{'text': 'house', 'pos': 'существительное'}, {'text': 'home', 'pos': 'существительное'}, {'text': 'dwelling', 'pos': 'существительное'}, {'text': 'door', 'pos': 'существительное'}, {'text': 'premise', 'pos': 'существительное'}, {'text': 'establishment', 'pos': 'существительное'}]

# Список примеров (по умолчанию на языке, который указан в from_lang)
>>> text.get_ex()
['белый дом', 'многоквартирный дом', 'детский дом', 'императорский дом', 'сельский дом']

# Список примеров на языке to_lang  
>>> text.get_ex(translate=True)
['white house', 'apartment building', "children's home", 'imperial household', 'rural dwelling']

# Список значений 
>>> text.get_mean()
['домик', 'здание', 'жилище', 'дверь', 'помещение', 'создание']

# Список всех синонимов 
>>> text.get_syn()
['building', 'household']

# Массив всех синонимов с перечислением аргументов
>>> text.get_syn('text', 'pos')
[{'text': 'building', 'pos': 'существительное'}, {'text': 'household', 'pos': 'существительное'}]
```

