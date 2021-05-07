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
        host='',  # 填入 httpapi 服务运行的地址
        authKey='',  # 填入 authKey
        account=123456,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
inc = InterruptControl(bcc)
@bcc.receiver("GroupMessage")
async def group_message_handler(
        message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group, member: Member,
):
    msgText = message.asDisplay()
    if msgText.startswith('/云图'):
        cloud = qunCloud(group.id)
        data = cloud.getData(msgText)
        cloud.solve(data)
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Image.fromLocalFile('./res/1.png')
        ]))
    else:
        qqid = member.id
        qunid = group.id
        sendtime = int(time.time())
        db = wordDB()
        if msgText.startswith('/s'):
            data = str(db.select(qunid))
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(data)
            ]))
        else:
            db.insertvalue(msgText, qqid, qunid, sendtime)

app.launch_blocking()
