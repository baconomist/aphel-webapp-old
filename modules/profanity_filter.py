import os
import re


class ProfanityFilter(object):
    profane_words = []
    chars_to_remove = [" ", ".", ","]

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "profane_words.txt"), "r") as profane_words_file:
            self.profane_words = profane_words_file.read().split("\n")

    def is_profane(self, text):
        result = ""
        # Convert to lowercase
        no_spaces = text.lower()
        # Strip HTML tags from input
        no_tags = re.sub('<[^<]+?>', '', no_spaces)
        for c in self.chars_to_remove:
            result = no_tags.replace(c, "")

        for i in self.profane_words:
            if i in result:
                return True
            else:
                pass

        return False
