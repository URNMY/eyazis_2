import fasttext
from bs4 import BeautifulSoup


params = {
    'lr': 0.1,
    'epoch': 25,
    'wordNgrams': 2,
    'verbose': 2,
    'minCount': 1,
    'bucket': 200000,
    'dim': 50
}
convert = {
    "__label__de": "german",
    "__label__fr": "french"
}
train_data_file = "TrainingData/training.txt"
model = fasttext.train_supervised(input=train_data_file, **params)


def predict(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.label.get_text(strip=True).replace("\n", "")
    result = model.predict(text)
    return convert[result[0][0]]
