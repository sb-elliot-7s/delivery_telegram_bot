from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def reply_keyboard_builder(texts: str | list[str], sizes: int | list[int], **kwargs):
    builder = ReplyKeyboardBuilder()
    texts = [texts] if isinstance(texts, str) else texts
    sizes = [sizes] if isinstance(sizes, int) else sizes
    [builder.button(text=txt) for txt in texts]
    builder.adjust(*sizes)
    return builder.as_markup(**kwargs)


def inline_keyboard_builder(texts: str | list[str], callback_datas: str | list[str], sizes: int | list[int], **kwargs):
    builder = InlineKeyboardBuilder()
    texts = [texts] if isinstance(texts, str) else texts
    callback_datas = [callback_datas] if isinstance(callback_datas, str) else callback_datas
    sizes = [sizes] if isinstance(sizes, int) else sizes
    [builder.button(text=text, callback_data=cb) for text, cb in zip(texts, callback_datas)]
    builder.adjust(*sizes)
    return builder.as_markup(**kwargs)
