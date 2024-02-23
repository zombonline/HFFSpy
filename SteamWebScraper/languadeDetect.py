from langdetect import detect_langs
chinese = "我是中国人"
english = "I am an American"
french = "Je suis français"
german = "Ich bin Deutscher"
spanish = "Soy español"
japanese = "私は日本人です"
korean = "나는 한국인이다"
russian = "Я русский"
arabic = "أنا عربي"
hindi = "मैं हिंदी हूँ"
thai = "ฉันเป็นคนไทย"
afrikaans = "Ek is 'n Suid-Afrikaner"

output = detect_langs("女巫婆婆")
print(output)

#detect if output is east asian language
def isEastAsian(lang):
    if lang == 'zh-cn' or lang == 'ja' or lang == 'ko':
        return True
    else:
        return False
print(isEastAsian(output[0].lang))