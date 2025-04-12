from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog

from ui import Ui_MainWindow
import json
app = QApplication([])
win = QMainWindow()
ui = Ui_MainWindow()


ui.setupUi(win)

NOTES ={}

#---------------------------------------



with open("notes_data.json", "r", encoding="utf-8") as file:
    NOTES = json.load(file)

ui.notes_list.addItems(NOTES)



def show_note():
    print("note selected")
    if ui.notes_list.currentItem():
        note_name = ui.notes_list.currentItem().text()
        note = NOTES[note_name]

        ui.textEdit.setText( note['текст'] )

        ui.tags_list.clear()
        ui.tags_list.addItems(note["теги"] )





ui.notes_list.currentItemChanged.connect(show_note)



def add_note():
    note_name, OK = QInputDialog.getText(win,'Додати нову нотатку', "Назва нотатки:")
    if OK:
        NOTES[note_name] = {
            "текст": "",
            "теги": [],
        }

        ui.notes_list.addItem(note_name)

ui.add_note.clicked.connect(add_note)

def save_note():
    if ui.notes_list.currentItem():
        text = ui.textEdit.toPlainText()
        note_name = ui.notes_list.currentItem().text()
        NOTES[note_name]["текст"] = text


        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(NOTES, file)

ui.save_note.clicked.connect(save_note)

def del_note():
    if ui.notes_list.currentItem():
        note_name = ui.notes_list.currentItem().text()
        del NOTES[note_name]


        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(NOTES, file)

        ui.notes_list.clear()
        ui.notes_list.addItems(NOTES)


ui.del_note.clicked.connect(del_note)


def add_tag():
    if ui.notes_list.currentItem():
        note_name = ui.notes_list.currentItem().text()
        note = NOTES[note_name]

        new_tag = ui.tag_input.text()

        if new_tag not in note["теги"]:
            note["теги"].append(new_tag)


            ui.tags_list.addItem(new_tag)
        ui.tag_input.clear()

ui.add_tag.clicked.connect(add_tag)

def del_tag():
    if ui.tags_list.currentItem():
        tag = ui.tags_list.currentItem().text()
        note_name = ui.notes_list.currentItem().text()
        note = NOTES[note_name]

        if tag in note["теги"]:
            note["теги"].remove(tag)

            ui.tags_list.clear()
            ui.tags_list.addItems(note["теги"])

ui.del_tag.clicked.connect(del_tag)


def search_tag():
    if ui.search_btn.text() == "шукати нотатки по тегу":

        tag =ui.tag_input.text()

        filterad_notes = []
        for note_name, note in NOTES.items():
            if tag in note["теги"]:
                filterad_notes.append(note_name)

        ui.notes_list.clear()
        ui.notes_list.addItems(filterad_notes)


        ui.search_btn.setText("Скинути пошук")

    elif ui.search_btn.text() == "Скинути пошук":
        ui.tag_input.clear()
        ui.notes_list.clear()
        ui.notes_list.addItems(NOTES)

        ui.search_btn.setText('шукати нотатки по тегу')

ui.search_btn.clicked.connect(search_tag)











win.show()
app.exec()