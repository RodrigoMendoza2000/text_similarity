from nltk.corpus import stopwords
from nltk import download
from nltk.stem import SnowballStemmer
import re
from nltk.stem import WordNetLemmatizer
import inflect
import num2words
from nltk.tokenize import word_tokenize

download('punkt', quiet=True)
download('stopwords', quiet=True)
ENGLISH_STOPWORDS = stopwords.words("english")

# Regex compilations for additional performance
EMAIL_PATTERN = re.compile(r"\S*@\S*\s?")
MENTION_PATTERN = re.compile(r"@\S*\s?")
URL_PATTERN = re.compile(r"http\S+|www.\S+")
# symbols_punctuations_pattern = re.compile(r'\?|\\|\!|\"|\#|\$|\%|\&|\'|\[|\^|\||\,|\¿|\¡|\_|\=|\>|\[|\^|\`|\{
# |\}|\~|\[|\]|\*|\+|\@|\/|\-|\:|\?|\¡|\¿||\.|\\|\“|\”|\(|\)|\;|\’|\;|\`|\´|\-|\·|\<|\º|\ª')
SYMBOL_PATTERN = re.compile(r"[^\w\sñ]")
SPECIAL_CASE_1 = re.compile(r"\nd")
SPECIAL_CASE_2 = re.compile(r"\n")
HASTAG_PATTERN = re.compile(r"\B(\#[a-zA-Z]+\b)(?!;)")
WORD_LENGTH_PATTERN = re.compile(r"\b(?!\d)\w{1,2}\b")
A_ACCENT_PATTERN = re.compile(r"[áàäâ]")
E_ACCENT_PATTERN = re.compile(r"[éèëê]")
I_ACCENT_PATTERN = re.compile(r"[íìïî]")
O_ACCENT_PATTERN = re.compile(r"[óòöô]")
U_ACCENT_PATTERN = re.compile(r"[úùüû]")
ALPHA_NUMERIC_PATTERN = re.compile(r"[^a-zA-Z\d|\s|ñ]")


class Preprocessing:

    def __init__(self):
        self.prompt = ""

    # Performs all preprocessing steps with an option to tokenize the text and return a list or to return the full
    # un-tokenized text. Also an option to decide if the text will be lemmatized or stemmed
    def transform_prompt(self, prompt, tokenize=True, lemmatize_or_stemming='lemmatize'):
        self.prompt = prompt.lower()
        self.convert_to_numeric()
        self.replace_words()
        # print(self.prompt)
        self.remove_stopwords()
        self.strip_formatting()
        if lemmatize_or_stemming == 'lemmatize':
            self.lemmatize_prompt()
        else:
            self.stem_prompt()
        if tokenize:
            self.tokenize()

        return self.prompt

    def tokenize(self):
        self.prompt = word_tokenize(self.prompt)

    # remove special characters and certain patterns.
    def strip_formatting(self):
        replace_to_blank = [
            EMAIL_PATTERN,
            MENTION_PATTERN,
            URL_PATTERN,
            SYMBOL_PATTERN,
            SPECIAL_CASE_1,
            SPECIAL_CASE_2,
            HASTAG_PATTERN,
            WORD_LENGTH_PATTERN
        ]

        for pattern in replace_to_blank:
            self.prompt = pattern.sub("", self.prompt)

    def stem_prompt(self):
        stemmer = SnowballStemmer("english")
        self.prompt = stemmer.stem(self.prompt)

    def lemmatize_prompt(self):
        wnl = WordNetLemmatizer()
        words = re.findall(r"\w+", self.prompt)

        self.prompt = " ".join(
            [
                wnl.lemmatize(word) for word in words
            ]
        )

    def remove_stopwords(self):
        words = re.findall(r"\w+", self.prompt)
        important_words = (
            word for word in words if word not in ENGLISH_STOPWORDS
        )
        self.prompt = " ".join(important_words)

    # Convert all numbers to their word format ex. 42 -> forty-two
    def convert_to_numeric(self):
        new_prompt = []
        words = re.findall(r"\w+", self.prompt)
        for word in words:
            try:
                new_prompt.append(num2words.num2words(word))
            except Exception as e:
                new_prompt.append(word)

        self.prompt = " ".join(new_prompt)

    # Replace certain words into other words defined in list_of_replaces.txt ex. AI -> Artificial intelligence
    def replace_words(self):
        word_replaces = {}
        with open("list_of_replaces.txt", 'r') as file:
            for line in file:
                line_splitted = line.split()
                key = line_splitted[0]
                val = " ".join([w for w in line_splitted[1:]])
                word_replaces[key] = val
        for replace_from, replace_to in word_replaces.items():
            # print(replace_from, ' ', replace_to)
            self.prompt = re.sub(r"\b"+replace_from+r"\b", replace_to, self.prompt)


if __name__ == "__main__":
    text = r"Artificial intelligence (AI) mirrors human intelligence by enabling machines to execute tasks " \
           "traditionally handled by humans, leveraging technologies like machine learning and neural networks. While " \
           "AI systems can adapt and improve through learning, concerns persist regarding ethical implications such " \
           "as privacy infringement and biases in decision-making. 42 As AI continues to evolve, responsible " \
           "development practices become imperative to navigate its societal impact. \n Hello"

    preprocesser = Preprocessing()

    new_text = preprocesser.transform_prompt(text, True)

    print(new_text)