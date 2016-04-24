import re

def contains_whole_word(text, word):
    compile = re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE)
    search_result = compile.search(text)
    return search_result is not None


def remove_empty_lines(text):
    lines = text.split("\n")
    filtered_lines = filter(lambda line:
                            line.strip() != '',
                            lines)
    return "\n".join(filtered_lines)


def differ(text1, text2, trim):
    if (trim):
        text1 = trim_text(text1)
        text2 = trim_text(text2)

    return text1 != text2


def trim_text(text):
    lines = text.split("\n")
    trimmed_lines = [line.strip() for line in lines]
    trimmed_text = "\n".join(trimmed_lines)

    return remove_empty_lines(trimmed_text)
