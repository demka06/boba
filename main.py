from random import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import func_class
import os
# ------------- [ CONNECT TO VK ] -----------
token = str(os.environ.get("VK-TOKEN"))
group_id = str(os.environ.get("VK-GROUP"))
vk_session = vk_api.VkApi(token=token)  # Обработка access_token
longpoll = VkBotLongPoll(vk_session, group_id)  # Данные для работы в сообществе
vk = vk_session.get_api()  # For api requests

# ----------------[ ENIGNE ]-----------------
admins = []
while True:
    try:

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['peer_id'] != event.object.message['from_id']:
                    command = event.obj.message["text"].lower()
                    user_id = event.object.message["from_id"]
                    peer_id = event.object.message["peer_id"]
                    cls = func_class.Main(vk, event, vk_session)
                    cls.registrationConv()
                    cls.registrarionUser()
                    if command.startswith("/addres"):
                        cls.addResourse()
                    elif command.startswith("/addmil"):
                        cls.addMilitary()
                    elif command.startswith("/addbld"):
                        cls.addBuild()
                    elif command.startswith("/collres"):
                        cls.collectResourses()
                    elif command.startswith("/collexp"):
                        cls.collectExpirience()
                    elif command.startswith("/listbld"):
                        cls.listOfBuilds()
                    elif command.startswith("/listmil"):
                        cls.listOfMillitaryObj()
                    elif command.startswith("/buybld"):
                        cls.buyBuild()
                    elif command.startswith("/buymil"):
                        cls.buyMillitaryObj()
                    elif command.startswith("/trans"):
                        cls.transaction()
                    elif command.startswith("/rejt"):
                        cls.transactionRejection()
                    elif command.startswith("/setrace"):
                        cls.setRace()
                    elif command.startswith("/st"):
                        cls.raceInformation()
                    elif command.startswith("/goods"):
                        cls.listOfGoods()
                    elif command.startswith("/addgood"):
                        cls.addGood()
                    elif command.startswith("/buygood"):
                        cls.buyGood()
                    elif command.startswith("/rejg"):
                        cls.rejectonLot()
                    elif command.startswith("/prof"):
                        cls.getProfile()
                    elif command.startswith("/races"):
                        cls.races()

    except Exception as error:
        vk.messages.send(
                peer_id=peer_id,
                random_id=2e9 + 1,
                message=f"[ERROR]\n{error}"
                )
