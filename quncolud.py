from PIL import Image
import numpy as np
from worddb import wordDB
import jieba
import arrow
from wordcloud import WordCloud, STOPWORDS

class qunCloud:
    def __init__(self, qunid):
        self.qunid = qunid
        db = wordDB()
        self.data = db.select(self.qunid)
    
    def getData(self, msgText):
        info = msgText.split()
        op = info[1]
        args = list(map(lambda x: int(x), info[2:]))
        argDict = {
            '年份': (args[0], 0),
            '月份': ((0, args[0]), 1),
            '日期': ((0, 0, args[0]), 2),
        }
        if op == '精确':
            return self.selectDate(*args)
        args = argDict[op]
        return self.selectLastTime(*(args[0]), timeType=args[1])


    def selectDate(self, year=-1, month=-1, day=-1):
        timeTuple = year, month, day
        print(year, month, day)
        if year == -1:
            data = self.selectLastTime(0, timeType=0)
        elif month == -1:
            data = filter(lambda x: x[1][0] == year, self.data)
        elif day == -1:
            data = filter(lambda x: x[1][:2] == timeTuple[:2], self.data)
        else:
            data = filter(lambda x: x[1] == timeTuple, self.data)
        data = map(lambda x: x[0], data)
        return ' '.join(data)

    def addStopWords(self, words):
        open('./res/userstopwords.txt', 'a', encoding='utf8').write('\n'.join(words))

    def selectLastTime(self, yearCnt=0, monthCnt=0, dayCnt=0, timeType=0):
        now = arrow.now()
        lastTime = now.shift(years=-yearCnt, months=-monthCnt, days=-dayCnt)
        timeTuple = lastTime.year, lastTime.month, lastTime.day
        data = filter(lambda x: x[1][timeType] == timeTuple[timeType], self.data)
        data = map(lambda x: x[0], data)
        return ' '.join(data)

    def solve(self, data):
        default_mode = jieba.cut(data, cut_all=False)
        default_mode = list(filter(lambda x: len(x) > 1, default_mode))
        text = ' '.join(default_mode)
        alice_mask = np.array(Image.open('./res/a.png'))
        cnStopWords = set(map(str.strip, open('./res/stopwords.txt', encoding='utf8').readlines()))
        userStopWords = set(map(str.strip, open('./res/userstopwords.txt', encoding='utf8').readlines()))
        stopwords = STOPWORDS|cnStopWords|userStopWords
        wc = WordCloud(
            font_path=r'./font/simhei.ttf',
            background_color="white",
            max_words=50,
            mask=alice_mask,
            collocations=False,
            stopwords=stopwords
        )
        wc.generate(text)
        wc.to_file('./res/1.png')
