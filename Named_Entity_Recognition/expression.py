import re
import data as d


class Expression:
    def __init__(self, token_name, classification_name, class_index):
        self.class_name = classification_name
        self.tokens = []
        self.tokens.append(token_name)
        self.class_index = class_index
        self.general_class_name = re.findall(d.ROUGHER_REGEX, classification_name)[0]

    def __str__(self):
        tokens = ''
        for token in self.tokens:
            tokens += token + ' '
        return self.class_name + ' ' + tokens

    def get_tokens(self):
        tokens = ''
        for token in self.tokens:
            tokens += token + ' '
        return tokens.strip()
