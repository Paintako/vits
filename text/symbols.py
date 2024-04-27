""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.
'''

# Indonesian phonemes

# _pad        = '_'
# _punctuation = ';:,.!?¡¿—…-–"«»“” '
# _tone = '0123456789'
# _sym = [' ', '!', ',', '.', '?', 'a', 'b', 'd', 'e', 'f', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'w', 'x', 'z', 'ŋ', 'ɔ', 'ə', 'ɛ', 'ɡ', 'ɪ', 'ɲ', 'ʃ', 'ʊ', 'ʒ', 'ʔ', 'ˈ']

# # Export all symbols:
# # symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa) + list(_tone) + list(_extra_indo) + list(_special)
# symbols = [_pad] + list(_punctuation) + list(_sym) + list(_tone)
# SPACE_ID = symbols.index(" ")

# old version

# _conn = '-'
# SPACE = ' '
# _symbols = ['', '-', '0', '1', '2', '3', '4', '5', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '。']

# symbols = [_conn] + [SPACE] + _symbols
# languages_nums = 4
# base_offset = len(symbols)
# symbols = symbols * languages_nums


# newest version

_conn = '-'
SPACE = ' '

_symbols = ['', '!', '"', ',', '-', '.', '0', '1', '2', '3', '4', '5', '7', '8', '9', ':', ';', '?', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'æ', 'ç', 'ð', 'ŋ', 'ɐ', 'ɑ', 'ɔ', 'ə', 'ɚ', 'ɛ', 'ɜ', 'ɡ', 'ɪ', 'ɬ', 'ɲ', 'ɹ', 'ɾ', 'ʃ', 'ʊ', 'ʌ', 'ʒ', 'ʔ', 'ʲ', 'ˈ', 'ˌ', 'ː', '̃', '̩', 'θ', 'ᵻ', '。']
symbols = [_conn] + [SPACE] + _symbols
languages_nums = 4
base_offset = len(symbols)
symbols = symbols * languages_nums

_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


def cleaned_text_to_sequence(cleaned_text, language):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = []
  for char in cleaned_text:
    if char == '':
      raise Exception('Found empty string!')
    symbols_id = symbols.index(char) + language * base_offset
    sequence.append(symbols_id)
  return sequence


def sequence_to_cleaned_text(sequence, language, symbols):
    '''Converts a sequence of IDs to a string of text corresponding to the symbols.
    Args:
        sequence: list of integers representing the sequence
        language: integer representing the language offset
        symbols: list of symbols used in the conversion
    Returns:
        String corresponding to the sequence of IDs
    '''
    cleaned_text = ''
    base_offset = len(symbols)
    for symbol_id in sequence:
        if symbol_id % base_offset == 0 and symbol_id != 0:
            raise Exception('Invalid symbol ID!')
        char_index = (symbol_id - language * base_offset) % base_offset
        cleaned_text += symbols[char_index]
    return cleaned_text

if __name__ == "__main__":
  
  lang_map = {
      'HAK' : 0,
      'TW' : 1,
      'ZH' : 2,
      'TZH' : 3,
  }

  for lang in lang_map:
    result = cleaned_text_to_sequence('ni3 hao2 qen2', lang_map[lang])
    print(result)
    print(sequence_to_cleaned_text(result, lang_map[lang], symbols))
    