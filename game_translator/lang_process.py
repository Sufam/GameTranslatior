from tqdm import tqdm
import time
import translator

def translatetxt(translateFile, outputfile, targetLang):
    translatedText = []

    with open(translateFile, 'r', encoding='utf-8') as f_in, \
        open(outputfile, 'w', encoding='utf-8') as f_out:
        
        lines = f_in.readlines()
        
        for i, line in enumerate(tqdm(lines, desc="Translation progress")):

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
            
            translated_value = translator.translateText(value, targetLang)
            
            translatedText.append(f"{key}={translated_value}\n")


        if len(translatedText) != 0:
            f_out.writelines(translatedText)
            translatedText.clear()
            f_out.flush()

    print("Translation successful")