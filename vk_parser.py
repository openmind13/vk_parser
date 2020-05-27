
import os
import re


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup


VK_URL = "https://vk.com"
VK_FEED_URL = "https://vk.com/feed"


class VK_parser:
    def __init__(self, login, password):
        PATH = os.path.dirname(os.path.abspath(__file__))

        DRIVER_PATH = PATH + r"\chromedriver\chromedriver.exe"
        OPTIONS_PATH = r"user-data-dir=C:\Users\openmind\AppData\Local\Google\Chrome\User Data"

        self.driver = webdriver.Chrome(DRIVER_PATH)
        self.driver.get(VK_URL)

        login_form = self.driver.find_element_by_css_selector("#index_email")
        login_form.send_keys(login)

        password_form = self.driver.find_element_by_css_selector("#index_pass")
        password_form.send_keys(password)

        submit_form = self.driver.find_element_by_css_selector("#index_login_button")
        submit_form.click()

        print("auth")
        assert self.driver.current_url is not VK_FEED_URL, "authorization failed"

    def parse(self):
        self.driver.get(VK_FEED_URL)
        # feed_posts = self.driver.find_elements_by_css_selector("div[class^='_post post page_block post--with-likes deep_active']")

        feed_posts = self.driver.find_elements_by_css_selector("div[class^='_post post page_block']")
        # print(feed_posts)
        print()
        print()

        # page = self.driver.page_source

        # element = self.driver.find_elements_by_css_selector("div[class='wall_post_text']")
        # print(element)

        record_text = []
        record_images = []
        record_links = []

        for post in feed_posts:
            post_id = post.get_attribute("id")

            # if post.find_element_by_css_selector("div[class='wall_post_text']"):
            #     wall_post_text = post.find_element_by_css_selector("div[class='wall_post_text']")
            #     links = wall_post_text.find_element_by_css_selector("a[href^='/away.php?']")
            #
            #
            #
            # print(id)
            # print(wall_post_text)
            # print(links)

            try:
                # post.find_element_by_css_selector("div[class='wall_post_text']")
                if post.find_element_by_css_selector("div.wall_post_text"):
                    # parse texts
                    wall_post_text = post.find_element_by_css_selector("div[class='wall_post_text']")
                    # record_text.append({"id": post_id, "text": wall_post_text})
                    # wall_post_text.get_property("textContent")
                    record_text.append({'id': post_id, 'text': wall_post_text.get_property("textContent")})

                    # parse links
                    feed_links_part_1 = [link.get_property("textContent") for link in
                                         wall_post_text.find_elements_by_css_selector("a[href^='/away.php?']")
                                         if link.get_property("textContent")[-1] != '.']
                    feed_links_part_2 = [link.get_attribute("title") for link in
                                         wall_post_text.find_elements_by_css_selector("a[href^='/away.php?']")
                                         if link.get_attribute("title") != ""]
                    feed_links = feed_links_part_1 + feed_links_part_2
                    if feed_links:
                        record_links.append({'id': post_id, 'links': feed_links})

                # parse images
                if post.find_elements_by_css_selector("div[class='page_post_sized_thumbs  clear_fix']"):
                    sized_thumbs = post.find_element_by_css_selector("div[class='page_post_sized_thumbs  clear_fix']")
                    images = [re.search(r"\(\"(.+)\"\)",
                              image.get_attribute("style")).group(1)
                              for image in sized_thumbs.find_elements_by_tag_name("a")]

                    record_images.append({'id': post_id, 'images': images})

            except NoSuchElementException as e:
                print(e)
                continue

            # print("post_id:")
            # print(post_id)
            # print("wall_post_text:")
            # print(wall_post_text.get_property("textContent"))
            # print("urls:")
            # print(feed_links)
            # print("images:")
            # print(images)
            # print()
            # print()

        return [record_text, record_images, record_links]

    def quit(self):
        self.driver.quit()







