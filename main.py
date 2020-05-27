import threading
import json
import time
import sys
import os.path

from vk_parser import VK_parser
from write_thread import WriteThread



text_records = []
image_records = []
link_records = []


# events
text_event = threading.Event()
image_event = threading.Event()
link_event = threading.Event()
read_files_event =   threading.Event()


# lock-objects
text_file_lock = threading.Semaphore()
image_file_lock = threading.Semaphore()
link_file_lock = threading.Semaphore()



def write_text():
    if not os.path.exists("texts.json"):
        with open("texts.json", 'w', encoding='utf-8') as file1:
            file1.write('[]')

    while True:
        text_event.wait()
        print("w1")
        text_file_lock.acquire()
        if text_records != []:
            with open("texts.json", "r", encoding='utf-8') as file:
                text = json.load(file)

            new_item = text_records.pop(0)
            if new_item not in text:
                text += new_item

            with open("texts.json", "w", encoding='utf-8') as file:
                json.dump(text, file, indent=4, sort_keys=True, ensure_ascii=False)

            # json.dump(full_data)
            # json.dump(text_records.pop(0), file, indent=4, sort_keys=True)
        text_file_lock.release()
        text_event.clear()


def write_images():
    if not os.path.exists("images.json"):
        with open("images.json", 'w', encoding='utf-8') as file2:
            file2.write('[]')

    while True:
        image_event.wait()
        print("w2")
        image_file_lock.acquire()
        if image_records != []:
            with open("images.json", "r", encoding="utf-8") as file:
                all_images = json.load(file)

            new_image_item = image_records.pop(0)
            if new_image_item not in all_images:
                all_images += new_image_item

            with open("images.json", "w", encoding="utf-8") as file:
                json.dump(all_images, file, indent=4, sort_keys=True, ensure_ascii=False)
        image_file_lock.release()
        image_event.clear()


def write_links():
    if not os.path.exists("links.json"):
        with open("links.json", 'w', encoding='utf-8') as file3:
            file3.write('[]')

    while True:
        link_event.wait()
        print("w3")
        link_file_lock.acquire()
        if link_records != []:
            with open("links.json", "r", encoding="utf-8") as file:
                all_links = json.load(file)

            new_link_item = link_records.pop(0)
            if new_link_item not in all_links:
                all_links += new_link_item

            with open("links.json", "w", encoding="utf-8") as file:
                json.dump(all_links, file, indent=4, sort_keys=True, ensure_ascii=False)
        link_file_lock.release()
        link_event.clear()


def read():
    time.sleep(1)
    text_event.clear()
    image_event.clear()
    link_event.clear()

    text_event.set()
    image_event.set()
    link_event.set()

    time.sleep(1)

    while True:
        # 1
        text_file_lock.acquire()
        image_event.set()
        link_event.set()
        print("reading text (file 1)")
        with open("texts.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            # data = file.read()
            print(data)
        text_file_lock.release()
        # time.sleep(1)

        # 2
        image_file_lock.acquire()
        text_event.set()
        link_event.set()
        print("reading images (file 2)")
        with open("images.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            # data = file.read()
            print(data)
        image_file_lock.release()
        # time.sleep(1)

        # 3
        link_file_lock.acquire()
        text_event.set()
        image_event.set()
        print("reading links (file3)")
        with open("links.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            # data = file.read()
            print(data)
        link_file_lock.release()
        # time.sleep(1)

        # 4
        text_event.set()
        image_event.set()
        link_event.set()
        print("not reading")
        # time.sleep(1)


def start_threads():

    w1 = threading.Thread(target=write_text, args=(), name="w1")
    w2 = threading.Thread(target=write_images, args=(), name="w2")
    w3 = threading.Thread(target=write_links, args=(), name="w3")
    r = threading.Thread(target=read, args=(), name="r")

    text_event.clear()
    image_event.clear()
    link_event.clear()
    read_files_event.clear()

    w1.start()
    print("start w1")
    w2.start()
    print("start w2")
    w3.start()
    print("start w3")
    r.start()
    print("start r")


def main():
    # login = str(input("enter login"))
    # password = str(input("enter password"))

    with open("auth.json", "r") as auth_file:
        auth = json.load(auth_file)

    parser = VK_parser(auth["login"], auth["password"])
    time.sleep(0.5) # time for loading

    data = parser.parse()
    text_records.append(data[0])
    image_records.append(data[1])
    link_records.append(data[2])

    start_threads()

    while True:
        data = parser.parse()
        text_records.append(data[0])
        image_records.append(data[1])
        link_records.append(data[2])

        # time.sleep(5)
        break

    parser.quit()


if __name__ == "__main__":
    main()