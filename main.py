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
vk = vk_session.get_api( )  # For api requests

# ----------------[ ENIGNE ]-----------------
while True:
	for event in longpoll.listen( ):
		try:
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.object.message['peer_id'] != event.object.message['from_id'] and event.object.message[
					'from_id'] > 0 and event.object.message['peer_id'] != 2e9 + 20:
					command = event.obj.message["text"].lower( )
					user_id = event.object.message["from_id"]
					peer_id = event.object.message["peer_id"]
					cls = func_class.Main(vk, event, vk_session)
					# cls.registrationConv( ) - перенесено на многопоточку
					# cls.registrarionUser( ) - переход на анкетную форму регистрации
					if command.startswith(("/addres", "")):
						cls.addResourse( )
					elif command.startswith(("/addmil", "")):
						cls.addMilitary( )
					elif command.startswith(("/addbld", "")):
						cls.addBuild( )
					elif command.startswith(("/collres", "/ресы")):
						cls.collectResourses( )
					elif command.startswith(("/collexp", "/опыт")):
						cls.collectExpirience( )
					elif command.startswith(("/listbld", "/постройки")):
						cls.listOfBuilds( )
					elif command.startswith(("/listmil", "/войска")):
						cls.listOfMillitaryObj( )
					elif command.startswith(("/buybld", "/+постройка")):
						cls.buyBuild( )
					elif command.startswith(("/buymil", "/+армия")):
						cls.buyMilitaryObj( )
					elif command.startswith(("/transm", "/переводм")):
						cls.transaction( )
					elif command.startswith(("/rejt", "")):
						cls.transactionRejection( )
					# elif command.split(" ")[0] in ("/setrace", " "):
					# можно убирать в связи с готовой анкетной системой
					# cls.setRace( )
					elif command.startswith(("/st", "/раса")):
						cls.raceInformation( )
					elif command.startswith(("/goods", "/сделки")):
						cls.listOfGoods( )
					elif command.startswith(("/addgood", "/добавитьсделку")):
						cls.addGood( )
					elif command.startswith(("/buygood", "/+сделка")):
						cls.buyGood( )
					elif command.startswith(("/rjgood", "/-сделка")):
						cls.lotRejection( )
					elif command.startswith(("/rejg", "")):
						cls.rejectonLotForAdms( )
					elif command.startswith(("/prof", "/проф")):
						cls.getProfile( )
					elif command.startswith(("/races", "/расы")):
						cls.races( )
					elif command.startswith(("/nickname", "")):
						cls.changeNickForAdms( )
					# elif command.startswith(("/nick", "")):
					# можно убирать в связи с готовой анкетной системой
					# cls.changeNickname( )
					elif command.startswith("/getstats"):
						cls.getCount( )
					elif command.startswith("/getlot"):
						cls.getLot( )
					elif command.startswith("/gettrans"):
						cls.getTransaction( )
					elif command.startswith("/event"):
						cls.showEvent( )
					elif command.startswith(("/help", "/помощь")):
						cls.help( )
					elif command.startswith(("/transr", "/переводр")):
						cls.addResTransactions( )
					elif command.startswith(("/trnacc", "/+сделка")):
						cls.acceptPersonalTrans( )
					elif command.startswith(("/trnrej", "")):
						cls.personalTransRejection( )
					elif command.startswith(("/rjtrns", "")):
						cls.PersonalTransRejForAdms( )
					elif command.startswith(("/lsttrn", "")):
						cls.listOfPersonalTrans( )
					elif command.startswith(("/pid", "")):
						cls.setChat( )
					elif command.startswith("/delprof"):
						cls.deleteProfile( )
					elif command.startswith(("/setfort", "/форт")):
						cls.changeFortName( )
					elif command.startswith(("/chngfort", "/названиефрт")):
						cls.changeFortNameForAdms( )
					elif command.startswith("/verif"):
						cls.verificationConv( )
					elif command.startswith("/unverif"):
						cls.unverificationConv( )
					# elif command.startswith("/form"):
					# cls.attachForm( )
					elif command.startswith("/getform"):
						cls.getForm( )
					elif command.startswith(("/rjg", "/-лот")):
						cls.lotRejection( )
					elif command.startswith(("/maps", "/карта")):
						cls.getMap( )
					elif command.startswith(("/setmap", "")):
						cls.setMap( )
					elif command.startswith(("/acform", "")):
						cls.accessForm( )
					elif command.startswith(("/rjform", "")):
						cls.rejectionForm( )
					elif command.startswith(("/msgto", "")):
						cls.sendMessageToUser( )
					elif command.startswith(("/rb", "/removebld")):
						cls.removeBuild( )
					elif command.startswith(("/fortst", "/статафорта")):
						cls.getFortStats( )
					elif command.startswith(("/milst", "/статаармии")):
						cls.getMilitaryStats( )
					elif command.startswith(("/costs", "/цены")):
						cls.getCostOnRes( )
		
		except Exception:
			vk.messages.send(
					peer_id=2e9 + 4,
					random_id=random.randint(0, 10000000000),
					message=f"[ERROR]\n{traceback.format_exc( )}\n\nLAST_EVENT: {event}"
					)
			print(traceback.format_exc( ))
