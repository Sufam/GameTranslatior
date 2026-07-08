import locale, json, io, os
from tqdm import tqdm
from deep_translator import GoogleTranslator
from pathlib import Path

import json_process, lang_process, translator, xml_process

def main():
    targetLang = input("Please enter your target language:")
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    if targetLang == "":
        localeLang = locale.getlocale()[0]
        targetLang = langs_dict[localeLang.split("_")[0].lower()]
        print(f"The system default language will be used:{targetLang}\n")
    elif targetLang not in langs_dict.values():
        print("Not suppout lang\nSupport lang:")
        for i in langs_dict:
            print(langs_dict[i], end = ", ")
        return "Lang input error"

    filetype = input("Enter the file type:").lower()
    print()
    rawFile = input("Enter the file you want to translate:")
    print()
    saveFile = os.path.join(os.path.dirname(rawFile), f"{input("Enter output file name:")}.{filetype}")
    if os.path.isfile(saveFile):
        print("有同名的文件將被取代，是否繼續執行(y/n)")
        if input().lower() == "n":
            return "File name error"
    print("\nTranslating, please wait...")

    if filetype == "json":
        file = open(rawFile, "r")
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
                    translated[j] = translator.translateText(temp[j], targetLang)
                else:
                    translated[j] = temp[j]
            
            if type(value) != str:
                output[i] = json_process.process_Data(translated[i], translated)
            else:
                output[i] = translated[i]

        with io.open(saveFile, "w", encoding= "utf-8") as file:
        
            saveData = json.dumps(output, indent = 4, ensure_ascii = False)
            file.write(saveData)

    elif filetype == "lang" or filetype == "txt":
        lang_process.translatetxt(rawFile, saveFile, targetLang)
    else:
        print("Not Support")

if __name__ == '__main__':
    main()
