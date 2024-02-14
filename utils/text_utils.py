from aiogram.utils.markdown import text, bold
from aiogram.utils.text_decorations import markdown_decoration


def get_caption_dish(name: str, description: str, price: str):
    price = price[:-2] + '.' + price[-2:]
    return text(
        bold(name),
        text(markdown_decoration.quote(description),
             markdown_decoration.quote(f'{price} руб.'), sep='\n'),
        sep='\n\n'
    )
