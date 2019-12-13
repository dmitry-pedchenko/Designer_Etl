import json
import xml.etree.ElementTree as et
import os


class Adapter:
    def __init__(self):
        with open(os.path.join(os.getcwd(), "System", "config.json")) as file:
            data = json.load(file)
        self.cur_language = et.parse(os.path.join(os.getcwd(), "System", "lan_config.xml")).getroot().find(f"{data['language']}")

    def take_translate(self, folder, tag):
        return self.cur_language.find(folder).find(tag).text

