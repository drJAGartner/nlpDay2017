import re
import traceback
from polyglot.text import Text

class SentimentFilter:
    def __init__(self):
        self.good_langs = ['en', 'ar', 'fr']

    def which_languages(self):
        return self.good_langs

    def is_scoreable(self, caption, lang):
        all_words = self.tokenize(caption, lang)
        scorable_words = 0
        for word in all_words:
            if word[0] == '@':
                continue
            if len(word)>4:
                if word[:4] == 'http' or word.find('.com')!=-1:
                    continue
            scorable_words += 1
        if scorable_words >2:
            return True
        return False


    def tokenize(self, caption, lang):
        if lang in ['en', 'fr']:
            caption = re.sub('[\s#]',' ',caption.lower(),flags=re.UNICODE)
            caption = re.sub('[^\w\s@]','',caption,flags=re.UNICODE)
            return filter(lambda x: x!='', caption.strip().split(' '))
        elif lang=='ar':
            try:
                return filter(lambda x: len(x)>1, Text(caption).words)
            except:
                traceback.print_exc()
                return []
        else:
            return []


    def pres_tokenize(self, caption, lang):
        caption = re.sub('[\s]',' ',caption.lower(),flags=re.UNICODE)
        caption = re.sub('[#]', ' #',caption,flags=re.UNICODE)
        if lang==['en', 'fr']:
            return filter(lambda x: x!='', caption.strip().split(' '))
        elif lang=='ar':
            try:
                caption = re.sub('[#]', ' #',caption,flags=re.UNICODE)
                return filter(lambda x: len(x)>1, Text(caption).words)
            except:
                traceback.print_exc()
                return []
        else:
            return []

    def extract_loc(self, caption):
        try:
            text = Text(caption)
            ll = [u' '.join(list(x)) for x in filter(lambda x: x.tag=='I-LOC', text.entities)]
            return set(ll)
        except:
            traceback.print_exc()
            return set([])