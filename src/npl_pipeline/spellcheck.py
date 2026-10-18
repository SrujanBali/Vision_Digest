import os
from symspellpy import SymSpell, Verbosity

current_dir = os.path.dirname(os.path.abspath(__file__))
dictionary_path = os.path.join(current_dir, "frequency_dictionary_en_82_765.txt")
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary(fr"{dictionary_path}", term_index=0, count_index=1)

def spelling_autocorrector(input_text: str) -> str:
    if not input_text or not input_text.strip():
        return ""
    corrected_words = []
    normalized_input = " ".join(input_text.split())
    words = normalized_input.split()

    for word in words:
        if word.isupper() or any(char.isdigit() for char in word) or len(word) <= 2:
            corrected_words.append(word)
            continue

        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        if suggestions:
            corrected_words.append(suggestions[0].term)
        else:
            corrected_words.append(word)

    return " ".join(corrected_words)
