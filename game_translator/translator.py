from deep_translator import GoogleTranslator
import time, locale

temp = {}#快取

#區隔出變數
def tokenize_with_nested_braces(text):
    tokens = [{"content": "", "type": "text"}]
    brances = 0
    inbrance = False

    for i in text:
        if i != "{":
            tokens[-1]["content"] = tokens[-1]["content"] + i
        if i == "{":
            brances += 1
            if inbrance != True:
                tokens.append({"content": "{", "type": "variable"})
            else:
                tokens[-1]["content"] = tokens[-1]["content"] + i
            inbrance = True
        elif i == "}":
            brances -= 1
            if brances <= 0:
                inbrance = False
        
    return tokens

#翻譯
def translate(text, tryTimes = 0):
    result = translator.translate(text)
    if text == None:
        return text
    
    if result == None:
        if tryTimes >= 5:
            return text
        time.sleep(tryTimes/5)
        return translate(text, tryTimes + 1)
    if result == "Error 500 (Server Error)!!1500.That’s an error.There was an error. Please try again later.That’s all we know.":
        time.sleep(5)
        return translate(text)
    return result

#翻譯準備
def translateText(text, targetLang = locale.getlocale()[0]):
    global translator
    tokens = tokenize_with_nested_braces(text)
    translated_pieces = []
    translator = GoogleTranslator(source = 'auto', target = targetLang)#翻譯器
    
    for item in tokens:
        if item["type"] == "text":
            raw_text = item["content"]
            if raw_text.strip():
                try:
                    if raw_text in temp:
                        result = temp[raw_text]
                    else:
                        result = normalize_text(translate(raw_text))
                        temp[raw_text] = result
                    translated_pieces.append(result)
                except Exception as e:
                    print(f"Error:{e}")
                    translated_pieces.append(raw_text)
            else:
                translated_pieces.append(raw_text)
        else:
            translated_pieces.append(item["content"])
            
    return "".join(translated_pieces)

def normalize_text(text):
    text = text.replace('（', '(').replace('）', ')')
    return text