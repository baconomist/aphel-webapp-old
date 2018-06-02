import os


class ProfanityFilter(object):
    profane_words = []
    chars_to_remove = [" ", ".", ","]

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "profane_words.txt"), "r") as profane_words_file:
            self.profane_words = profane_words_file.read().split("\n")

    def is_profane(self, text):
        # Convert to lowercase
        no_spaces = text.lower()

        for c in self.chars_to_remove:
            no_spaces = no_spaces.replace(c, "")

        for i in self.profane_words:
            if i in no_spaces:
                return True
            else:
                pass

        return False
