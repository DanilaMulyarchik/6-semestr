from typing import Dict, Tuple, Union, Optional
from collections import defaultdict
import re

import nltk

from conf.metadata import metadata

not_tokens = [
    "are",
    "is",
    "a",
    "the",
    "am",
    "at",
    "of",
    "and",
    "in",
    "on",
    "or",
    "but",
    "by",
    "to",
]


def filter_rows(
    flag: str,
    data: Dict[str, Dict[str, Union[str, int]]],
    search_type: Optional[str] = None,
    frequency: Optional[Tuple[int, int]] = None,
) -> Dict[str, Dict[str, str | int]]:
    filters = {
        "word": filter(
            lambda x: search_type is not None and search_type in x[0], data.items()
        ),
        "frequency": filter(
            lambda x: frequency is not None
            and frequency[0] <= int(x[1]["frequency"])
            and frequency[1] >= int(x[1]["frequency"]),
            data.items(),
        ),
        "extra information": filter(
            lambda x: search_type is not None
            and isinstance(search_type, str)
            and search_type in x[1]["additional information"],
            data.items(),
        ),
    }

    return dict(filters[flag])


def process_item(item: str) -> str:
    reg_exp = r"((?<![a-zA-Z])\.?\S\.)|[\‘\’\/\.\,:;!\?\"\(\)…\“\”]|\d+(-\d+)?|^[–\-]$"
    item = re.sub(reg_exp, "", item)

    return item


def parse_text(text: str) -> Dict[str, Dict[str, Union[str, int]]]:
    parsed_text = defaultdict(lambda: 0)
    words = dict()
    for i in text.split():
        i = process_item(i)
        if (
            i not in not_tokens
            and i not in [j.capitalize() for j in not_tokens]
            and i.isalpha()
        ):
            parsed_text[i.lower()] += 1

    for key, value in parsed_text.items():
        words[key] = {
            "frequency": value,
            "additional information": metadata[nltk.pos_tag([key])[0][1]],
        }

    return words


def morphy_logic_main(text: str) -> Dict[str, Dict[str, Union[str, int]]]:
    words = dict(sorted(parse_text(text=text).items(), key=lambda x: x[0]))

    return words
