import json, io, os, tkinter, threading
from tkinter import filedialog, ttk
from deep_translator.mymemory import MY_MEMORY_LANGUAGES_TO_CODES
from functools import partial
from pathlib import Path


import json_process, lang_process, translator, xml_process

#Load file
def loadFile(file):
    global filePreview
    with open(file, "r", encoding = "utf-8") as f:
        lines = f.readlines() 
    filePreview.set(lines)
    
#Choose translate file
def chooseFile():
    global inputPath, fileName, file_Information
    filePath = filedialog.askopenfilename()
    if filePath == "":
        return 0
    inputPath.set(f"{filePath}")
    fileName = os.path.split(filePath)[1]
    loadFile(filePath)
    file_Information.pack(fill = "both", padx = 10, pady = 10)

#Check input not blank
def checkInput(path, name, sourcelang, targetlang, filetype):
    if path == "" or name == "" or sourcelang == "Source Language" or targetlang == "Target Language" or filetype == "File Type":
        return False
    return True

#Start translate
def start():
    global inputPath, outputNameEnter, sourceLangOption, targetLangOption, fileTypeOption, progress, run_prompt_text

    sourceLang = sourceLangOption.get()
    targetLang = targetLangOption.get()
    fileType = fileTypeOption.get()
    rawFile = inputPath.get()
    outputName = outputNameEnter.get()

    if not checkInput(rawFile, outputName, sourceLang, targetLang, fileTypeOption):
        run_prompt_text.set("Input error, please check again.")
        return "input error"

    saveFile = os.path.join(f"{os.path.abspath(os.path.split(rawFile)[0])}", f"{outputName}.{fileType}")

    run_prompt_text.set("Start Translate")
    print(f"Start Translate\n Raw File:{rawFile}\n Save File:{saveFile}\n Source Lang:{sourceLang}\n Target Lnag:{targetLang}")

    if fileType == "json":
        file = open(rawFile, "r")
        data = json.load(file)
        output = {}

        for i in data:
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
                    translated[j] = translator.translateText(temp[j], sourceLang, targetLang)
                else:
                    translated[j] = temp[j]
            
            if type(value) != str:
                output[i] = json_process.process_Data(translated[i], translated)
            else:
                output[i] = translated[i]

        with io.open(saveFile, "w", encoding= "utf-8") as file:
        
            saveData = json.dumps(output, indent = 4, ensure_ascii = False)
            file.write(saveData)

    elif fileType == "lang" or fileType == "txt":
        lang_process.translatetxt(rawFile, saveFile, sourceLang, targetLang)
    elif fileType == "xml":
        xml_process.translate()
    else:
        run_prompt_text.set("Not Support fule type")
        print("Not Support")

    print("Translate Successful")
    run_prompt_text.set("Translate Successful")

def threading_control(fun):
    if fun == 1:
        start_thread = threading.Thread(target = start)
        start_thread.start()


def window_Start():
    global inputPath, outputNameEnter, sourceLangOption, targetLangOption, fileTypeOption, file_Information, filePreview, progress, run_prompt_text
    
    langs_dict = MY_MEMORY_LANGUAGES_TO_CODES #Supported languages

    all_file_type = ("txt", "lang", "json") #Supported file types

    #Create window
    window = tkinter.Tk()
    window.title("GameTranslator")
    window.geometry("600x700")
    window.resizable(True, True)
    window.configure(background = "#9E9F9F")

    #Close window message
    def closeWindow():
        if tkinter.messagebox.askokcancel("Leave", "Are you sure to close the window?"):
            window.destroy()
    
    #Set variables
    inputPath = tkinter.StringVar()
    filePreview = tkinter.StringVar()
    run_prompt_text = tkinter.StringVar()

    #Area
    input_Area = tkinter.Frame(window, bg = "#9E9F9F")
    select_Area = tkinter.LabelFrame(input_Area, text = "Input File Path", height = 80, bg = "#A4AAC7", bd = 3, relief = tkinter.RIDGE)
    output_Area = tkinter.LabelFrame(input_Area, text = "Output Name", height = 80, bg = "#A4AAC7", bd = 3, relief = tkinter.RIDGE)
    set_Area = tkinter.LabelFrame(input_Area, text = "Translate Set", height = 80, bg = "#A4AAC7", bd = 3, relief = tkinter.RIDGE)
    file_Information = tkinter.LabelFrame(input_Area, text = "File Preview", bg = "#A4AAC7", bd = 3, relief = tkinter.RIDGE)

    input_Area.pack(fill = "both", padx = 10, pady = 10)
    select_Area.pack(fill = "x", padx = 10, pady = 10)
    output_Area.pack(fill = "x", padx = 10, pady = 10)
    set_Area.pack(fill = "x", padx = 10, pady = 10)

    #File information
    fileTextPreview = tkinter.Frame(file_Information, bg = "#B1B0B0", bd = 3, relief = tkinter.RIDGE)
    textScrollbar = tkinter.Scrollbar(fileTextPreview, bg = "#B1B0B0")
    fileContent = tkinter.Listbox(fileTextPreview, bg = "#FFFFFF", listvariable = filePreview, yscrollcommand = textScrollbar.set)

    textScrollbar.config(command = fileContent.yview)

    fileTextPreview.pack(fill = "both", padx = 5, pady = 5)
    textScrollbar.pack(fill = "y", side = "right")
    fileContent.pack(fill = "x", side = "left", expand = 1)


    #Input file
    fileLocation = tkinter.Label(select_Area, textvariable = inputPath, background = "#FFFFFF", bd = 3, relief = tkinter.SUNKEN)
    selectFile_btn = tkinter.Button(select_Area, text="Select File", background="#7D9BB3", command = chooseFile, bd = 3, relief = tkinter.RIDGE)

    fileLocation.pack(fill = "both", side = "left", padx = 5, pady = 5, expand = 1)
    selectFile_btn.pack(fill = "both", side = "right", padx = 5, pady = 5, expand = 0)

    #outputname
    outputNameEnter = tkinter.Entry(output_Area, bd = 3, relief = tkinter.SUNKEN)

    outputNameEnter.pack(fill = "both", padx = 5 , pady = 5, expand = 1)

    #Translate option
    sourceLangOption = ttk.Combobox(set_Area, value = [i for i in langs_dict], state = "readonly")
    targetLangOption = ttk.Combobox(set_Area, value = [i for i in langs_dict], state = "readonly")
    fileTypeOption = ttk.Combobox(set_Area, value = all_file_type, state = "readonly")

    sourceLangOption.set("Source Language")
    targetLangOption.set("Target Language")
    fileTypeOption.set("File Type")

    sourceLangOption.pack(fill = "both", side = "left", padx = 5, pady = 5, expand = 1)
    targetLangOption.pack(fill = "both", side = "left", padx = 5, pady = 5, expand = 1)
    fileTypeOption.pack(fill = "both", side = "right", padx = 5, pady = 5, expand = 1)

    #Start translate
    start_btn = tkinter.Button(window, text = "Start Translate", background = "#7D9BB3", command = partial(threading_control, 1), bd = 3, relief = tkinter.RIDGE)
    progress = ttk.Progressbar(window, orient = "horizontal", length = 600, mode = "determinate")
    run_prompt = tkinter.Label(window, textvariable = run_prompt_text, background = "#FFFFFF")

    start_btn.pack(fill = "x", padx = 10, pady = 10)
    run_prompt.pack(fill = "x", padx = 10, pady = 10)
    #progress.pack(fill = "x", padx = 10, pady = 10)

    window.protocol("WM_DELETE_WINDOW", closeWindow)

   
    window.mainloop()

if __name__ == '__main__':
    window_Start()
    window_thread = threading.Thread(target = window_Start, daemon = True)
    window_thread.start()
