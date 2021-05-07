import sqlite3
import time
class wordDB:
    def __init__(self):
        self.con = sqlite3.connect('./database/word.db')
        self.cur = self.con.cursor()
        # 建表
        # sql = '''
        #     create table qunword(
        #         msg text,
        #         qqid text,
        #         qunid text,
        #         sendtime text
        #     )
        # '''
        # try:
        #     self.cur.execute(sql)
        # except Exception as e:
        #     print(e)

    def insertvalue(self, msg, qqid, qunid, sendtime):
        sql = '''
            insert into qunword values('%s', %s, %s, %s)
        '''
        self.cur.execute(sql%(msg, qqid, qunid, sendtime))
        self.con.commit()

    @classmethod
    def _getym (self, sendTime):
        sendTimeMsg = time.localtime(float(sendTime))
        return (sendTimeMsg.tm_year, sendTimeMsg.tm_mon, sendTimeMsg.tm_mday)

    def select(self, qunid):
        sql = '''
            select msg, sendtime from qunword where qunid = %s
        '''%qunid
        data = self.cur.execute(sql).fetchall()
        data = list(map(lambda x: (x[0], self._getym(x[1])), data))
        return data

    def selectall(self):
        sql = '''
            select * from qunword
        '''
        data = self.cur.execute(sql).fetchall()
        data = list(map(lambda x: (x[0], self._getym(x[1])), data))
        return data


