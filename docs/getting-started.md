# yandex-dictionary
## Установка
```bash
pip install yandex-dictionary
```
## Быстрый старт
```python
>>> from yandex_dictionary import Dictionary
...
>>> dct = Dictionary("API key", 'ru', 'en')
>>> dct.lookup('программирование')
{"text": "программирование", "is_found": True}
```

> Примечание: библиотека работает только с json данными.

### Класс `Dictionary`
Конструктор класса принимает обязательный параметр `api_key`, а также необязательные (можно указать отдельно при вызове `lookup()`):
- `api_key`: API-ключ (обязательно), можно получить на [yandex](https://yandex.ru/dev/keys/get/?service=dict);
- `from_lang`, `to_lang`: языковая пара, можно переопределить при вызове `lookup()`;
- `ui`: язык интерфейса пользователя, на котором будут отображаться названия частей речи. По умолчанию `en`.

> `ui` поддерживает следуюшие языки: 
> - `en` - английский
> - `ru` - русский
> - `uk` - украинский
> - `tr` - турецкий.

Вызов `lookup()` принимает обязательный параметр `text`, а также именованные аргументы:
- `from_lang`, `to_lang`: языковая пара;
- `ui`: язык интерфейса частей речи;
- `flags`: опции поиска (битовая маска флагов).
> Возможные значения `flags`:
> - *0x0001*: применить семейный фильтр;
> - *0x0002*: отображать названия частей речи в краткой форме;
> - *0x0004*: включать поиск по форме слова;
> - *0x0008*: включать фильтр, требующий соответствия частей речи искомого слова и перевода


Получить список доступных языковых пар:
```python
>>> dct.get_langs()
```

### Класс `models.TextDescription`
Экземпляр класса создается при вызове `lookup()`.
Доступные методы и атрибуты:
- `json()`: искомый ответ API-запроса в формате json;
- `get_tr()`: список переводов;
- `get_syn()`: список синонимов;
- `get_men()`: список значений исходного текста;
- `get_ex()`: список с примерами.
- `is_found`: возвращает `True` если словарный массив был найден;
- `anm`: одушевленность (возвращает `None` если одушевленность отсутствует);
- `gen`: род (возвращает `None` если род отсутствует);
- `pos`: часть речи (возвращает `None` если отсутствует);
- `ts`: транскрипция (возвращает `None` если отсутствует);
- `dict_array`: массив словарных статей;
- `text`: исходный текст

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

# Список словарей переводов
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

# Список словарей всех синонимов
>>> text.get_syn('text', 'pos')
[{'text': 'building', 'pos': 'существительное'}, {'text': 'household', 'pos': 'существительное'}]
```
