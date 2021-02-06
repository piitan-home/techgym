from typing import Iterable, List


def extract_words(text: Iterable[str], obj_list: Iterable[str] = ('名詞', '動詞', '形容詞', '副詞')) -> List[List[str]]:
    from janome.tokenizer import Tokenizer
    t = Tokenizer()

    def __extract_words(text_: str) -> List[str]:
        tokens = t.tokenize(text_)
        r = [token.base_form for token in tokens if token.part_of_speech.split(',')[
            0] in obj_list]
        return r
    return [__extract_words(t) for t in text]
