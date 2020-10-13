import MeCab
import re
from typing import List, Tuple, Iterator

# スペース、人名の間の中黒、"VS"は切れ目にする
KEYWORD_FOR_SPLIT = re.compile(r"(\s|・|VS)")

wakati_tagger = MeCab.Tagger("-Owakati")
ochasen_tagger = MeCab.Tagger('-Ochasen')


def generate_keywords(title: str):
    """
    Get word and class tuples list.
    """
    result = wakati_tagger.parse(title)

    # Make word list
    tokens: List[str] = list(filter(lambda w: not KEYWORD_FOR_SPLIT.fullmatch(
        w) and w != '\n', KEYWORD_FOR_SPLIT.split(result)))
    pos_list = list(_to_pos(tokens=tokens))

    keywords = []
    for idx in range(len(pos_list)):
        word, tok = pos_list[idx]
        if tok != '名詞':
            continue
        keywords.append(word)
        complex_word_list = _generate_complex_word(idx, pos_list)
        for complex_word in complex_word_list:
            if complex_word not in keywords:
                keywords.append(complex_word)
    return keywords


def _to_pos(tokens: List[str]) -> Iterator[Tuple[str, str]]:
    for token in tokens:
        parsed_token = ochasen_tagger.parse(token).splitlines()[
            0].rstrip().split('\t')
        if parsed_token[0] == 'EOS':
            yield (token, "スペース")
            continue
        tok = parsed_token[3].split('-')[0]
        yield (token, tok)


def _generate_complex_word(
        idx: int, pos_list: List[Tuple[str, str]]) -> List[str]:
    result_list: List[str] = []
    result = pos_list[idx][0]
    for jdx in reversed(list(range(idx))):
        if jdx == 0:
            break
        word, tok = pos_list[jdx]
        if tok != '名詞':
            break
        result = word + result
        result_list.append(result)
    return result_list
