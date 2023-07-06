import dateutil.parser
from functools import wraps
from django.core.cache import cache
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response


def grab_error(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with atomic():
                return func(*args, **kwargs)
        except Exception as exp:
            return Response(
                {
                    'status': False,
                    'error': f'{exp.__class__.__name__}: {exp}'
                },
                status=status.HTTP_400_BAD_REQUEST)

    return wrapper


def is_token_valid(token):
    data = cache.get(token)
    return data


def split_word_for_search(word):
    words = word.split(' ')
    for x in words:
        if x == '':
            words.pop(x)
    return words


def remove_spaces(word):
    result = ''
    word = list(word)
    last_word_space = True
    for w in word:
        if w == ' ':
            if last_word_space:
                pass
            else:
                last_word_space = True
                result = result + w
        else:
            last_word_space = False
            result = result + w
    return result


def str_to_datetime(datetime_str):
    return dateutil.parser.parse(datetime_str)


def parse_range(ranges):
    try:
        ranges = str(ranges).replace('[', '').replace(']', '').replace(
            '(', '').replace(')', '')
        ranges = ranges.split(',')
        return {'from': ranges[0], 'upto': ranges[1]}
    except Exception as exp:
        raise Exception(f'Ranges must be given in [__from__, __upto__]'
                        f' or (__from__, __upto__) format. Error: {exp}')


def validate_order_by(valid_orders, order_by):
    des = ''
    if order_by[:1] == "-":
        des = order_by[:1]
        order_by = order_by[1:len(order_by)]
    if order_by.lower() in valid_orders:
        return f"{des}{order_by.lower()}"
    else:
        raise Exception(f"{order_by} is a Invalid order argument.")


def clean_data(keys, data):
    for key in keys:
        data.pop(key, None)
    return data
