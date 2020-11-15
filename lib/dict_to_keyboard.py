from telebot import types


def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

def dict_to_keyboard(d, chunk_size=None):
    kb = types.InlineKeyboardMarkup()
    items = list(d.items())
    if (chunk_size == None):
        rows = [items]
    else:
        rows = chunks(items, 2)

    for row in rows:
        keys = [
            types.InlineKeyboardButton(
                text=text,
                callback_data=callback,
            ) for (text, callback) in row
        ]

        kb.add(*keys)

    return kb
