""" from https://github.com/keithito/tacotron """
from text import cleaners
from text.symbols import symbols


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


def text_to_sequence(text, cleaner_names, langauge):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = []
  for char in text:
    if char == '':
      continue
    symbol_id = symbols.index(char)
    sequence.append(symbol_id)
  return sequence


def cleaned_text_to_sequence(cleaned_text):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = []
  for ph in cleaned_text.split(' '):
    if ph == '':
      raise Exception('Found empty string!')
    sequence.append(_symbol_to_id[ph])
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


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
  return text
