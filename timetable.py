import sys
import json
import os  
import secrets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, 
    QMessageBox, QVBoxLayout, QWidget, QTextEdit
)

# File to save and load the timetable data
TIMETABLE_FILE = "timetable_data.json"

# Define the slot timings
slot_timings = {
    0: "9:00-9:55 AM",
    1: "10:00-10:55 AM",
    2: "11:00-11:55 PM",
    3: "12:00-12:55 PM",
    4: "1:00-1:55 PM",
    5: "2:00-2:55 PM"
}

# subjects
subs = ["C Programming", "Engineering Maths", "Linux Lab", "Managing Self", "Free","Free", "Physics","Problem Solving", "Environmental Studies"]

# Load timetable from file or initialize default
def load_timetable():
    try:
        with open(TIMETABLE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Return default timetable if file does not exist
        return {
            "Batch A": {
                "Monday": ["C Programming", "Linux Lab", "Free", "Lunch","Managing Self","Free"],
                "Tuesday": ["Problem Solving", "Engineering Maths", "Environmental Studies", "Lunch","Engineering Maths","C Programming"],
                "Wednesday": ["C Programming", "Free", "Engineering Maths", "Lunch","Free","Free"],
                "Thursday": ["Problem Solving", "Free", "Physics", "Lunch","Engineering Maths","Free"],
                "Friday": ["Environmental Studies", "C Programming", "Free", "Lunch","Linux Lab", "Problem Solving"]
            }
        }

# Save timetable to file
def save_timetable(timetable):
    with open(TIMETABLE_FILE, "w") as file:
        json.dump(timetable, file)

# Initialize timetable
timetable = load_timetable()

class TimetableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timetable Generator by CRACK JACKS")
        self.setGeometry(400, 100, 500, 600)
        
        # Initialize UI elements
        self.initUI()

    def initUI(self):
        # Layout setup
        layout = QVBoxLayout()
        
        # Batch selection
        self.batch_label = QLabel("Batch:")
        layout.addWidget(self.batch_label)
        self.batch_combo = QComboBox()
        self.batch_combo.addItems(timetable.keys())
        layout.addWidget(self.batch_combo)

        # Day selection
        self.day_label = QLabel("Day:")
        layout.addWidget(self.day_label)
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        layout.addWidget(self.day_combo)

        # Time Slot Entry
        self.slot_label = QLabel("Time Slot (0-5):")
        layout.addWidget(self.slot_label)
        self.slot_entry = QLineEdit()
        layout.addWidget(self.slot_entry)

        # Subject Entry
        self.subject_label = QLabel("Subject:")
        layout.addWidget(self.subject_label)
        self.subject_entry = QLineEdit()
        layout.addWidget(self.subject_entry)

        # Buttons for adding, deleting, showing free slots, and exporting timetable
        self.add_class_btn = QPushButton("Add Lecture")
        self.add_class_btn.clicked.connect(self.add_extra_class)
        layout.addWidget(self.add_class_btn)

        self.delete_class_btn = QPushButton("Delete Lecture")
        self.delete_class_btn.clicked.connect(self.delete_extra_class)
        layout.addWidget(self.delete_class_btn)

        self.show_slots_btn = QPushButton("Show Free Slots")
        self.show_slots_btn.clicked.connect(self.show_free_slots)
        layout.addWidget(self.show_slots_btn)

        # Delete batch button
        self.delete_batch_btn = QPushButton("Delete Selected Batch")
        self.delete_batch_btn.clicked.connect(self.delete_batch)
        layout.addWidget(self.delete_batch_btn)

        self.export_btn = QPushButton("Export Timetable")
        self.export_btn.clicked.connect(self.export_timetable)
        layout.addWidget(self.export_btn)

        # New batch addition
        self.new_batch_label = QLabel("New Batch Name:")
        layout.addWidget(self.new_batch_label)
        self.new_batch_entry = QLineEdit()
        layout.addWidget(self.new_batch_entry)

        self.add_batch_btn = QPushButton("Add New Batch")
        self.add_batch_btn.clicked.connect(self.add_new_batch)
        layout.addWidget(self.add_batch_btn)

        #Auto generate
        self.auto_generate_btn = QPushButton("Auto generate timetable")
        self.auto_generate_btn.clicked.connect(self.automatic_generation)
        layout.addWidget(self.auto_generate_btn)

        # Display timetable
        self.timetable_display = QTextEdit()
        self.timetable_display.setReadOnly(True)
        layout.addWidget(self.timetable_display)

        # Set central widget and layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initial display of the timetable
        self.show_timetable()

    def get_free_slots(self, batch, day):
        return [i for i, slot in enumerate(timetable[batch][day]) if slot == "Free"]

    def add_extra_class(self):
        try:
            batch = self.batch_combo.currentText()
            day = self.day_combo.currentText()
            time_slot = int(self.slot_entry.text())
            subject = self.subject_entry.text()

            if timetable[batch][day][time_slot] == "Free":
                timetable[batch][day][time_slot] = subject
                QMessageBox.information(self, "Success", f"Added {subject} to {batch} on {day} at slot {time_slot} ({slot_timings[time_slot]})")
                self.show_timetable()
                save_timetable(timetable)
            elif timetable[batch][day][time_slot] == "Lunch" :
                if subject.lower() == "free":
                    QMessageBox.warning(self, "Warning", "cannot add a free class in place of lunch.")
                else:    
                    confirmation = QMessageBox.question(self, "Confirm", "adding class at the time of lunch will result in no lunch break. Do you still wish to continue ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if confirmation == QMessageBox.Yes:
                        timetable[batch][day][time_slot] = subject
                        QMessageBox.information(self, "Success", f"Added {subject} to {batch} on {day} at slot {time_slot} ({slot_timings[time_slot]})")
                        self.show_timetable()
                        save_timetable(timetable)
            else:
                alternate_slots = self.get_free_slots(batch, day)
                QMessageBox.warning(self, "Conflict", f"Slot {time_slot} is occupied! Available slots: {', '.join(str(slot) for slot in alternate_slots)}")
        except:
            QMessageBox.warning(self, "Warning", "Slot cannot be empty or contain any invalid input.")
            # QMessageBox.critical(self, "Error", str(e))

    def delete_extra_class(self):
        try:
            batch = self.batch_combo.currentText()
            day = self.day_combo.currentText()
            time_slot = int(self.slot_entry.text())
            if timetable[batch][day][time_slot] != "Lunch" and timetable[batch][day][time_slot] != "Free":
                if timetable[batch][day][time_slot] == timetable[batch][day][3]:
                    subject = timetable[batch][day][time_slot]
                    timetable[batch][day][time_slot] = "Lunch"
                    QMessageBox.information(self, "Success", f"Removed {subject} from {batch} on {day} at slot {time_slot}")
                    self.show_timetable()
                    save_timetable(timetable)
                else:
                    subject = timetable[batch][day][time_slot]
                    timetable[batch][day][time_slot] = "Free"
                    QMessageBox.information(self, "Success", f"Removed {subject} from {batch} on {day} at slot {time_slot}")
                    self.show_timetable()
                    save_timetable(timetable)
            else:
                QMessageBox.warning(self, "Warning", "Cannot delete a lunch break or a free slot!")
        except:
            QMessageBox.warning(self,"Warning!", "Slot cannot be empty or contain any invalid input.")    
            # QMessageBox.critical(self, "Error", str(e))

    def show_free_slots(self):
        batch = self.batch_combo.currentText()
        day = self.day_combo.currentText()
        if batch in timetable and day in timetable[batch]:
            free_slots = self.get_free_slots(batch, day)
            QMessageBox.information(self, "Free Slots", f"Free slots for {batch} on {day}: {', '.join(f'{slot} ({slot_timings[slot]})' for slot in free_slots)}")
        else:
            QMessageBox.warning(self, "Warning", "Invalid batch or day!")

    def show_timetable(self):
        timetable_text = ""
        for batch, days in timetable.items():
            timetable_text += f"{batch}:\n"
            for day, classes in days.items():
                timetable_text += f"  {day}:\n"
                for i, subject in enumerate(classes):
                    timetable_text += f"    Slot {i} ({slot_timings[i]}): {subject}\n"
        self.timetable_display.setText(timetable_text)

    def add_new_batch(self):
        new_batch_name = self.new_batch_entry.text()
        if new_batch_name and new_batch_name not in timetable:
            timetable[new_batch_name] = {day: ["Free", "Free", "Lunch", "Free", "Free","Free"] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
            self.batch_combo.addItem(new_batch_name)
            QMessageBox.information(self, "Success!", f"New batch '{new_batch_name}' has been added!")
            self.new_batch_entry.clear()
            self.show_timetable()
            save_timetable(timetable)
        else:
            QMessageBox.warning(self, "Warning", "Batch name is empty or already exists!") 

    def delete_batch(self):
        batch = self.batch_combo.currentText()
        if batch: 
            confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete the batch '{batch}'?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                timetable.pop(batch, None)
                self.batch_combo.removeItem(self.batch_combo.currentIndex())
                QMessageBox.information(self, "Success", f"Batch '{batch}' has been deleted.")
                self.show_timetable()
                save_timetable(timetable)
        else:
            QMessageBox.warning(self, "Warning", "No batch selected!")

    def export_timetable(self):
        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, "timetable.txt")

        try:
            with open(file_path, "w") as file:
                for batch, days in timetable.items():
                    file.write(f"{batch}:\n")
                    for day, classes in days.items():
                        file.write(f"  {day}:\n")
                        for i, subject in enumerate(classes):
                            file.write(f"    Slot {i} ({slot_timings[i]}): {subject}\n")
            QMessageBox.information(self, "Export", f"Timetable has been exported to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export timetable: {str(e)}")
    
    def automatic_generation(self):
        try:
            auto_batch = self.new_batch_entry.text()
            if auto_batch not in timetable:
                timetable[auto_batch] = {day: [secrets.choice(subs), secrets.choice(subs), secrets.choice(subs),"Lunch", secrets.choice(subs),secrets.choice(subs)] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
                self.batch_combo.addItem(auto_batch)
                QMessageBox.information(self, "Success!", f"New batch '{auto_batch}' has been added. ")
                self.show_timetable()
                self.new_batch_entry.clear()
                save_timetable(timetable)
            elif auto_batch in timetable:
                QMessageBox.warning(self, "Warning", "Batch already exists!")

        except:
            QMessageBox.warning(self, "Warning!","slot cannot be empty or contain any invalid value.")


# Run the application
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = TimetableApp()
    window.show()
    sys.exit(app.exec_())
