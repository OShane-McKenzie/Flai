import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QVBoxLayout, QLabel, QPushButton,QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtWidgets import QComboBox
import openai
import os

class InputThread(QThread):
    responseReady = pyqtSignal(str)

    def __init__(self,parent, input_text):
        super().__init__(parent)
        self.input_text = input_text
        self.parent = parent

    def run(self):
       
        getInput=self.input_text
        thisChat="Your name is "+self.parent.combo_box.currentText()+" from this point onwards."

        ##########################################################################################

        openai.api_key = "ab-cdefghijklmnopqrstuvwxyz"#your api key goes here, You can find safer ways to load this, if you choose.
                                                                                                #May crash if key is not valid.
        ##########################################################################################

        if self.parent.chatStarted==False:

            blueResponse="" #("_")

            response = openai.Completion.create(model="text-davinci-003", prompt=thisChat+"\n"+getInput, temperature=1, max_tokens=1000)
            while True:
                if response.choices[0].text=="":
                    response = openai.Completion.create(model="text-davinci-003", prompt=getInput, temperature=1, max_tokens=1000)
                else:
                    blueResponse = response.choices[0].text+"\n..........\n" 
                    break 
            self.parent.thisChat+=getInput+"\n\n"+self.parent.combo_box.currentText()+":"+response.choices[0].text
            self.responseReady.emit(blueResponse)
            self.parent.chatStarted=True
        else:
            thisInput=self.parent.thisChat+"\n"+getInput
            response = openai.Completion.create(model="text-davinci-003", prompt=thisInput, temperature=1, max_tokens=1000)
            counter = 5
            blueResponse=""
            while counter > 0:
                if response.choices[0].text=="":
                    response = openai.Completion.create(model="text-davinci-003", prompt=thisInput, temperature=1, max_tokens=1000)
                    counter=counter-1
                    if counter == 1:
                        blueResponse = response.choices[0].text+"\n..........\n"
                        break
                else:
                    blueResponse = response.choices[0].text+"\n..........\n"
                    break
            self.parent.thisChat+=getInput+"\n\n"+self.parent.combo_box.currentText()+":"+response.choices[0].text
            self.responseReady.emit(blueResponse)
            

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.chatStarted=False
        self.thisChat="Your name is OpenAI from this point onwards."
        layout.addWidget(self.text_edit)
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.submit)
        layout.addWidget(self.button)

        personalities = ["OpenAI", "Light Yagami", 
        "Isaac Newton", "Albert Einstein", "William Shakespeare", 
        "Sherlock Holmes", "Plato", "Mahatma Gandhi", "Martin Luther King Jr.", 
        "Charles Darwin","Programming Guru"]

        self.combo_box = QComboBox()
        self.combo_box.addItems(personalities)
        layout.addWidget(self.combo_box)

        self.clear_button = QPushButton("New chat")
        self.clear_button.clicked.connect(self.clear_text)

        layout.addWidget(self.clear_button)
        self.setLayout(layout)
        self.setFixedWidth(600)
        self.resize(600, 300)
        self.setWindowIcon(QIcon("img/FloatingAI.png"))
        
        self.text_input.setPlaceholderText("Type anything....")
    def clear_text(self):
        self.text_edit.clear()
        
        self.text_input.setPlaceholderText("Type anything....")
        self.chatStarted=False
        self.thisChat="Your name is "+self.combo_box.currentText()+" from this point onwards."
    global usrText
    usrText=""
    def submit(self):
        global usrText
        input_text = self.text_input.toPlainText()
        usrText="Me:\n"+input_text+"\n..........\n"
        self.text_input.clear()
        self.text_input.setPlaceholderText("Awaiting "+self.combo_box.currentText()+" to respond...")
        self.getResponse(input_text)

    def getResponse(self,input_text):
        self.inputThread = InputThread(self,input_text)
        self.inputThread.responseReady.connect(self.threadComplete)
        self.inputThread.start()
    
    def threadComplete(self,choices):
        self.text_edit.append(usrText+"\n\n"+self.combo_box.currentText()+":"+choices)
        self.text_input.clear()
        self.text_input.setPlaceholderText("Type anything....")
        print(choices)


app = QApplication(sys.argv)
dialog = InputDialog()


dialog.show()

sys.exit(app.exec_())
