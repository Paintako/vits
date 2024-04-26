""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.
'''

# Indonesian phonemes

_pad        = '_'
_punctuation = ';:,.!?¡¿—…-–"«»“” '
_tone = '0123456789'
_sym = [' ', '!', ',', '.', '?', 'a', 'b', 'd', 'e', 'f', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'w', 'x', 'z', 'ŋ', 'ɔ', 'ə', 'ɛ', 'ɡ', 'ɪ', 'ɲ', 'ʃ', 'ʊ', 'ʒ', 'ʔ', 'ˈ']

with open(f'text/lang_phones.txt','r',encoding='utf-8') as f:
  phonemes = f.readlines()
phonemes = [p.strip() for p in phonemes]

# Export all symbols:
# symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa) + list(_tone) + list(_extra_indo) + list(_special)
symbols = [_pad] + list(_punctuation) + list(_sym) + list(_tone) + list(phonemes)
SPACE_ID = symbols.index(" ")


_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

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


if __name__ == "__main__":
  text = "tsch2 iu23 tsch2 ioong23 h2 e23 it24 k2 e23 iu23 n2 un23 sil t2 et24 gn2 in25 sc2 iak24 iu23 m2 oo25 an22 k2 ien22 t2 an21 v2 a22 kh2 iun21 k2 e23 s2 irp28 tsch2 it24 s2 e23 s2 e23 a21 m2 ooi23 sil"
  print(cleaned_text_to_sequence(text))