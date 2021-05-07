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
        arg = list(map(lambda x: int(x), info[2:]))
        print(*arg,op)
        result = {
            '日期': self.selectDay,
            '月份': self.selectMonth,
            '年份': self.selectYear,
            '精确': self.selectData
        }
        return result[op](*arg)


    def selectData(self, yearCnt=0, monthCnt=0, dayCnt=0):
        print(dayCnt)
        print(self.data)
        now = arrow.now()
        lastTime = now.shift(years=-yearCnt, months=-monthCnt, days=-dayCnt)
        tupleTime = lastTime.year, lastTime.month,  lastTime.day
        data = filter(lambda x: x[1] == tupleTime and x[0] != '[图片]', self.data)
        data = map(lambda x: x[0], data)
        
        return ' '.join(data)
    
    def selectDay(self, dayCnt=0):
        now = arrow.now()
        lastTime = now.shift(days=-dayCnt)
        data = filter(lambda x: x[1][2] == lastTime.day and x[0] != '[图片]', self.data)
        data = map(lambda x: x[0], data)
        return ' '.join(data)

    def selectMonth(self, monthCnt=0):
        now = arrow.now()
        lastTime = now.shift(months=-monthCnt)
        data = filter(lambda x: x[1][1] == lastTime.month and x[0] != '[图片]', self.data)
        data = map(lambda x: x[0], data)
        return ' '.join(data)

    def selectYear(self, yearCnt=0):
        now = arrow.now()
        lastTime = now.shift(years=-yearCnt)
        data = filter(lambda x: x[1][0] == lastTime.year and x[0] != '[图片]', self.data)
        data = map(lambda x: x[0], data)
        return ' '.join(data)

    def solve(self, data):
        default_mode = jieba.cut(data, cut_all=False)
        default_mode = list(filter(lambda x: len(x) > 1, default_mode))
        text = ' '.join(default_mode)
        alice_mask = np.array(Image.open('./res/a.png'))
        cnStopWords = set(map(str.strip, open('./res/stopwords.txt', encoding='utf8').readlines()))
        stopwords = STOPWORDS|cnStopWords
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
