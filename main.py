import random
import traceback

import pymysql
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

user = str(os.environ.get("SQL-USER"))
passw = str(os.environ.get("SQL-PASS"))

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
					if command.split(" ")[0] in ("/addres", ""):
						cls.addResourse()
					elif command.split(" ")[0] in ("/addmil", ""):
						cls.addMilitary()
					elif command.split(" ")[0] in ("/addbld", ""):
						cls.addBuild()
					elif command.split(" ")[0] in ("/collres", ""):
						cls.collectResourses()
					elif command.split(" ")[0] in ("/collexp", ""):
						cls.collectExpirience()
					elif command.split(" ")[0] in ("/listbld", ""):
						cls.listOfBuilds()
					elif command.split(" ")[0] in ("/listmil", ""):
						cls.listOfMillitaryObj()
					elif command.split(" ")[0] in ("/buybld", ""):
						cls.buyBuild()
					elif command.split(" ")[0] in ("/buymil", ""):
						cls.buyMilitaryObj()
					elif command.split(" ")[0] in ("/transm", ""):
						cls.transaction()
					elif command.split(" ")[0] in ("/rejt", ""):
						cls.transactionRejection()
					elif command.split(" ")[0] in ("/setrace", ""):
						cls.setRace()
					elif command.split(" ")[0] in ("/st", ""):
						cls.raceInformation()
					elif command.split(" ")[0] in ("/goods", ""):
						cls.listOfGoods()
					elif command.split(" ")[0] in ("/addgood", ""):
						cls.addGood()
					elif command.split(" ")[0] in ("/buygood", ""):
						cls.buyGood()
					elif command.split(" ")[0] in ("/rjgood", ""):
						cls.lotRejection()
					elif command.split(" ")[0] in ("/rejg", ""):
						cls.rejectonLotForAdms()
					elif command.split(" ")[0] in ("/prof", ""):
						cls.getProfile()
					elif command.split(" ")[0] in ("/races", ""):
						cls.races()
					elif command.split(" ")[0] in ("/nickname", ""):
						cls.changeNickForAdms()
					elif command.split(" ")[0] in ("/nick", ""):
						cls.changeNickname()
					elif command.startswith("/getstats"):
						cls.getCount()
					elif command.startswith("/getlot"):
						cls.getLot()
					elif command.startswith("/gettrans"):
						cls.getTransaction()
					elif command.startswith("/event"):
						cls.showEvent()
					elif command.split(" ")[0] in ("/help", ""):
						cls.help()
					elif command.split(" ")[0] in ("/transr", ""):
						cls.addResTransactions()
					elif command.split(" ")[0] in ("/trnacc", ""):
						cls.acceptPersonalTrans()
					elif command.split(" ")[0] in ("/trnrej", ""):
						cls.personalTransRejection()
					elif command.split(" ")[0] in ("/rjtrns", ""):
						cls.PersonalTransRejForAdms()
					elif command.split(" ")[0] in ("/lsttrn", ""):
						cls.listOfPersonalTrans()
					elif command.split(" ")[0] in ("/pid", ""):
						cls.setChat()
					elif command.startswith("/delprof"):
						cls.deleteProfile()
					elif command.split(" ")[0] in ("/setfort", ""):
						cls.changeFortName()
					elif command.split(" ")[0] in ("/chngfort", ""):
						cls.changeFortNameForAdms()
					elif command.startswith("/verif"):
						cls.verificationConv()
					elif command.startswith("/unverif"):
						cls.unverificationConv()
					elif command.startswith("/from"):
						cls.attachForm()
					elif command.startswith("/getform"):
						cls.getForm()
							
						
		except Exception:
			vk.messages.send(
					peer_id=2e9 + 4,
					random_id=random.randint(0, 10000000000),
					message=f"[ERROR]\n{traceback.format_exc()}\n\nLAST_EVENT: {event}"
					)
			print(traceback.format_exc())
