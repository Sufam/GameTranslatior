from deep_translator import GoogleTranslator
from tqdm import tqdm
import time, locale, json
import json_process

langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

localeLang = locale.getlocale()[0]
targetLang = input("Please enter your target language:")

if targetLang == "":
    targetLang = langs_dict[localeLang.split("_")[0].lower()]
    print(f"The system default language will be used:{targetLang}")
print()

translator = GoogleTranslator(source='auto', target=targetLang)#翻譯器
translatedText = []#翻譯好的文字
translated_temp = {}#快取

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
def translate_Prepare(text):
    global translator
    tokens = tokenize_with_nested_braces(text)
    translated_pieces = []
    
    for item in tokens:
        if item["type"] == "text":
            raw_text = item["content"]
            if raw_text.strip():
                try:
                    if raw_text in translated_temp:
                        result = translated_temp[raw_text]
                    else:
                        result = normalize_text(translate(raw_text))
                        translated_temp[raw_text] = result
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

filetype = input("Enter the file type:").lower()
print()
translateFile = input("Enter the file you want to translate:")
print()
outputfile = input("Enter the file storage location:")
print("\nTranslating, please wait...")



if filetype == "json":
    file = open(translateFile, "r")
    data = json.load(file)
    output = {}

    for i in tqdm(data, desc = "Translation progress"):
        temp = {}
        translated = {}
        value = data[i]
        if type(value) != str:
            temp[i] = [j for j in value]
            temp = json_process.read_Data(value, temp)
        else:
            temp[i] = value

        for j in temp:
            if type(temp[j]) == str:
                translated[j] = translate_Prepare(temp[j])
            else:
                translated[j] = temp[j]
        
        if type(value) != str:
            output[i] = json_process.process_Data(translated[i], translated)
        else:
            output[i] = translated[i]

    print(output)
