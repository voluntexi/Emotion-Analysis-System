import jieba
import pandas as pd

def wordFrequency(filename):
    df = pd.read_excel(filename)
    comments = df.iloc[:, 2].tolist()
    comments = [str(comment) for comment in comments]
    word = " ".join(comments)
    words = jieba.lcut(word)
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    dict = {}
    for i in range(20):
        word, count = items[i]
        dict[word] = count

    return dict
