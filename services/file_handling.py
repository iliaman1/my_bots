BOOK_PATH = 'books/book1.txt'
PAGE_SIZE = 1050
book: dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    symbols = [',', '?', '!', ':', ';', '.']
    current_index = start + size if start + size < len(text) else start + len(text[start:]) - 1
    end = start + size if start + size <= len(text) else len(text[start:])
    flag1 = 2
    flag2 = 2
    while current_index > start:
        if text[end - 1] in symbols and text[end] in symbols and flag1 == 2:
            flag1 -= 1
            while text[current_index] in symbols:
                current_index -= 1
        elif text[end] in symbols and flag2 == 2:
            flag2 -= 1
            current_index -= 1
        elif text[current_index] in symbols:
            break
        current_index -= 1
    return text[start:current_index + 1], len(text[start:current_index]) + 1


def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as ftext:
        text = ftext.read()

    current_char = 0
    current_page = 1
    while _get_part_text(text, current_char, PAGE_SIZE)[0]:
        book[current_page] = _get_part_text(text, current_char, PAGE_SIZE)[0].lstrip()
        current_char += _get_part_text(text, current_char, PAGE_SIZE)[1]
        current_page += 1


prepare_book(BOOK_PATH)
