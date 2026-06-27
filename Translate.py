from deep_translator import GoogleTranslator
from tqdm import tqdm
import time, locale

langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

localeLang = locale.getlocale()[0]
targetLang = input("請輸入翻譯後的語言:")

if targetLang == "":
    targetLang = langs_dict[localeLang.split("_")[0].lower()]
    print(f"將使用系統預設語言:{targetLang}")
print()

translator = GoogleTranslator(source='auto', target=targetLang)#翻譯器
translatedText = []#翻譯好的文字
temp = {}#快取

#區隔出變數
def tokenize_with_nested_braces(text):
    tokens = []
    stack = []
    start_idx = 0
    
    for i, char in enumerate(text):
        if char == '{':
            if len(stack) == 0:
                if i > start_idx:
                    tokens.append({"type": "text", "content": text[start_idx:i]})
                start_idx = i
            stack.append(char)
        elif char == '}':
            if stack:
                stack.pop()
                if len(stack) == 0:
                    tokens.append({"type": "brace", "content": text[start_idx : i + 1]})
                    start_idx = i + 1
                    
    if start_idx < len(text):
        tokens.append({"type": "text", "content": text[start_idx:]})
        
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
                    if raw_text in temp:
                        result = temp[raw_text]
                    else:
                        result = normalize_text(translate(raw_text))
                        temp[raw_text] = result
                    translated_pieces.append(result)
                except Exception as e:
                    print(f"出現錯誤:{e}")
                    translated_pieces.append(raw_text)
            else:
                translated_pieces.append(raw_text)
        else:
            translated_pieces.append(item["content"])
            
    return "".join(translated_pieces)

def normalize_text(text):
    text = text.replace('（', '(').replace('）', ')')
    return text



translateFile = input("請輸入要翻譯的文件:")
print()
outputfile = input("請輸入文件儲存位置:")
print("\n開始翻譯文件，請稍等......")



with open(translateFile, 'r', encoding='utf-8') as f:
    total_lines = sum(1 for _ in f)

with open(translateFile, 'r', encoding='utf-8') as f_in, \
     open(outputfile, 'w', encoding='utf-8') as f_out:
    
    lines = f_in.readlines()

    
    for i, line in enumerate(tqdm(lines, desc="翻譯進度")):
        text = line.strip()

        if i % 2000 == 0 and i > 0:
            time.sleep(5)#緩衝五秒

        #每翻譯100個就儲存一次
        if len(translatedText) >= 100:
            f_out.writelines(translatedText)
            translatedText.clear()
            f_out.flush()
            
        if not text or "=" not in text:
            translatedText.append(line)
            continue
            
        key, value = text.split("=", 1)
        
        translated_value = translate_Prepare(value)
        
        translatedText.append(f"{key}={translated_value}\n")


    if len(translatedText) != 0:
        f_out.writelines(translatedText)
        translatedText.clear()
        f_out.flush()

temp.clear()
print("翻譯完成")