import threading
import json


class WriteThread(threading.Thread):
    def __init__(self, file_name, data, file_semaphore, event):
        threading.Thread.__init__(self)
        self.file_name = file_name
        self.data = data
        self.file_semaphore = file_semaphore
        self.event = event

    def start(self):

        while True:
            self.event.wait()
            print("write " + self.file_name)
            self.file_semaphore.acquire()
            with open("texts.json", "w") as file:
                old_data = json.load(file)
                print(old_data)
                data = old_data + text_records.pop(0)
                json.dump(data, file1, indent=4, sort_keys=True)
            self.file_semaphore.release()
            self.event.clear()