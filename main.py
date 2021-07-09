import random
import traceback
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
while True:
	for event in longpoll.listen():
		try:
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.object.message['peer_id'] != event.object.message['from_id']  and event.object.message['from_id'] > 0:
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
						cls.buyMilitaryObj()
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
					elif command.startswith("/nickname"):
						cls.changeNickForAdms()
					elif command.startswith("/nick"):
						cls.changeNickname()
					elif command.startswith("/getstats"):
						cls.getCount()
					elif command.startswith("/getlot"):
						cls.getLot()
					elif command.startswith("/gettrans"):
						cls.getTransaction()
					elif command.startswith("/event"):
						cls.showEvent()
					elif command.startswith("/event"):
						cls.help()	
		except Exception:
			vk.messages.send(
					peer_id=2e9 + 4,
					random_id=random.randint(0, 10000000000),
					message=f"[ERROR]\n{traceback.format_exc()}\n\nLAST_EVENT: {event}"
					)
