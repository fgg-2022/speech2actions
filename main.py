
from speech2text.asr_json import get_sentence
from text2action.semantic_parse import translate
from text2action.extract import parse_sent


def main():
    file_path = 'audio/record1.m4a'
    recorded_sent_result = eval(get_sentence(file_path))
    assert 'result' in recorded_sent_result.keys()
    recorded_sent = recorded_sent_result['result'][0]
    print(f"Text to Speech Result:\n\t Chinese: {recorded_sent} ")
    en_recorded_sent = translate(recorded_sent)
    print(f"\t English: {en_recorded_sent} \n")
    actions = parse_sent(en_recorded_sent)
    print(f"Speech to Action Result:\n\t : {actions} ")

    pass


if __name__ == '__main__':
    main()
