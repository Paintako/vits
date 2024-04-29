import argparse

def arg_parse():
    parser = argparse.ArgumentParser(description='Corpus Count')
    parser.add_argument('--path', type=str, default='filelists', help='Path to the filelists')
    return parser.parse_args()

def count(path):
    file_parse = ['mixed_5_test_new.txt', 'mixed_5_train_new.txt']
    language = {
        'ZH' : 0,
        'EN' : 0,
        'ID' : 0,
        'TW' : 0,
        'HAK' : 0,
        'TZH' : 0
    }

    speaker_cnt = {
        'ZH' : set(),
        'EN' : set(),
        'ID' : set(),
        'TW' : set(),
        'HAK' : set(),
        'TZH' : set()
    }

    for file in file_parse:
        with open(f'{path}/{file}','r',encoding='utf-8') as f:
            lines = f.readlines()
    
    for line in lines:
        lang, speaker = line.strip().split('|')[2], int(line.strip().split('|')[1])
        language[lang] += 1

        speaker_set = speaker_cnt[lang]
        if speaker not in speaker_set:
            speaker_cnt[lang].add(speaker)

    print(language)
    for lang in speaker_cnt:
        print(f'{lang} -> Speaker count: {len(speaker_cnt[lang])}, Utternces: {language[lang]}')

if __name__ == '__main__':
    args = arg_parse()
    count(args.path)