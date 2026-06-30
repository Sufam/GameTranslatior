from deep_translator import GoogleTranslator
from tqdm import tqdm
import locale, json, io
import json_process, translator

targetLang = input("Please enter your target language:")

if targetLang == "":
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    localeLang = locale.getlocale()[0]
    targetLang = langs_dict[localeLang.split("_")[0].lower()]
    print(f"The system default language will be used:{targetLang}\n")

filetype = input("Enter the file type:").lower()
print()
rawFile = input("Enter the file you want to translate:")
print()
saveFile = input("Enter the file storage location:")
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
