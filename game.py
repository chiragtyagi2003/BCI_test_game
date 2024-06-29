import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import tkinter as tk
import os

# Initialize the Firebase app with your service account key
cred = credentials.Certificate('major.json')
firebaseDatabaseURl = os.getenv("firebaseDatabaseUrl")
firebase_admin.initialize_app(cred, {
    'databaseURL': firebaseDatabaseURl
})

# Reference to your database path
ref = db.reference('/')

# Define the GUI application
class MovingObjectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moving Object Game")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.object = self.canvas.create_rectangle(270, 170, 330, 230, fill="blue")
        self.position_x = 300  # Center position
        self.object_width = 60
        self.canvas_width = 600

    def move_left(self):
        if self.position_x - self.object_width // 2 > 0:
            self.canvas.move(self.object, -10, 0)
            self.position_x -= 10
            print(f"Moved left to position: {self.position_x}")

    def move_right(self):
        if self.position_x + self.object_width // 2 < self.canvas_width:
            self.canvas.move(self.object, 10, 0)
            self.position_x += 10
            print(f"Moved right to position: {self.position_x}")

    def stay_neutral(self):
        print(f"Stayed neutral at position: {self.position_x}")

    def update_position(self, data):
        left_enabled = data.get('left', {}).get('enabled', False)
        right_enabled = data.get('right', {}).get('enabled', False)
        neutral_enabled = data.get('neutral', {}).get('enabled', False)

        if left_enabled:
            self.move_left()
        elif right_enabled:
            self.move_right()
        elif neutral_enabled:
            self.stay_neutral()

# Create the main window
root = tk.Tk()
app = MovingObjectApp(root)

# Define a listener function
def listener(event):
    print(f"Event Type: {event.event_type}")  # can be 'put' or 'patch'
    print(f"Path: {event.path}")  # relative to the database root
    print(f"Data: {event.data}")  # new data at that location

    # Get the latest state of the database
    data = ref.get()
    if data:
        app.update_position(data)

# Attach the listener to the reference
ref.listen(listener)

# Start the GUI event loop
root.mainloop()
