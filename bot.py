import asyncio
from quncolud import qunCloud
import time
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain, Image
from graia.application.session import Session
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt import InterruptControl
from worddb import wordDB

loop = asyncio.get_event_loop()


bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="",
        authKey="",
        account=123456,
        websocket=True  
    )
)
inc = InterruptControl(bcc)

adminId = 123456

@bcc.receiver("GroupMessage")
async def group_message_handler(
        message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group, member: Member,
):
    msgText = message.asDisplay()
    if msgText.startswith('/云图'):
        cloud = qunCloud(group.id)
        if msgText.split()[1] != '屏蔽词':
            data = cloud.getData(msgText)
            cloud.solve(data)
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Image.fromLocalFile('./res/1.png')
            ]))
        else:
            words = msgText.split()[2:]
            if member.id == adminId and words[0] == '全局':
                cloud.addGlobalStopWords(words[1:])
            else:
                cloud.addQunStopWords(words)
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain('屏蔽词添加成功\n' + str((msgText.split()[2:])))
            ]))
    else:
        qqid = member.id
        qunid = group.id
        sendtime = int(time.time())
        wordDB().insertvalue(msgText, qqid, qunid, sendtime)

app.launch_blocking()
