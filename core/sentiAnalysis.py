from cemotion import Cemotion

'''
功能：根据输入的字符串数组来进行计算情感值使用微调的bert进行情感分析
'''
c = Cemotion()

def singleSentiment(text):
    Ssenti = []
    for w in text:
        if not isinstance(w, str):
            print(f"非字符串值: {w}, 跳过")
            Ssenti.append(0.0)
        elif len(w) < 1:
            Ssenti.append(0.0)
        else:
            sent = (c.predict(w) - 0.5) * 2
            Ssenti.append(sent)
            print(f"{w}：的情感值为：{sent}")
    return Ssenti
