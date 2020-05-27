import threading
import time


text_records = []
image_records = []
link_records = []

# events
write_file1 = threading.Event()
write_file2 = threading.Event()
write_file3 = threading.Event()
read_file =   threading.Event()

# lock-objects
lock_file1 = threading.Semaphore()
lock_file2 = threading.Semaphore()
lock_file3 = threading.Semaphore()


def write1():
    # if not os.path.exists("texts.json"):
    #     with open("texts.json", 'w') as file1:
    #         file1.write('[]')
    with open("texts.json", "w") as f:
        json.dump(f, {"hello":"world"})

    while True:
        write_file1.wait()
        print("w1")
        lock_file1.acquire()
        if text_records != []:
            with open("texts.json", "w") as file1:
                old_data = json.load(file1)

                print(old_data)
                time.sleep(1000)
                data = old_data + text_records.pop(0)
                json.dump(data, file1, indent=4, sort_keys=True)
        lock_file1.release()
        write_file1.clear()


def write2():
    # if not os.path.exists("images.json"):
    #     with open("images.json", 'w') as file2:
    #         file2.write('[]')

    while True:
        write_file2.wait()
        print("w2")
        lock_file2.acquire()
        if image_records != []:
            with open("images.json", "a") as file2:
                json.dump(image_records.pop(0), file2, indent=4, sort_keys=True)
        lock_file2.release()
        write_file2.clear()


def write3():
    # if not os.path.exists("links.json"):
    #     with open("links.json", 'w') as file3:
    #         file3.write('[]')

    while True:
        write_file3.wait()
        print("w2")
        lock_file3.acquire()
        if link_records != []:
            with open("links.json", "a") as file3:
                json.dump(link_records.pop(0), file3, indent=4, sort_keys=True)
        lock_file3.release()
        write_file3.clear()
