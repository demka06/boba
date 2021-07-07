import datetime
import random
from datetime import datetime
from PIL import Image, ImageGrab, ImageFont, ImageDraw
import vk_api
import pymorphy2
import pymysql
from pytz import timezone
import os


class Main(object):
	def __init__(self, vk, event, vk_session):
		self.vk = vk
		self.event = event
		self.user_id = event.object.message["from_id"]
		self.peer_id = event.object.message["peer_id"]
		self.command = event.obj.message["text"].lower( )
		self.txt = event.obj.message["text"]
		self.vk_session = vk_session
		self.adms_chat = 2000000001
		self.user = str(os.environ.get("SQL-USER"))
		self.passw = str(os.environ.get("SQL-PASS"))
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		curs.execute("SELECT user_id FROM users WHERE role = 'adm'")
		self.adms = []
		for i in curs.fetchall( ):
			self.adms.append(i[0])
	
	def registrationConv(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		res = curs.execute("SELECT peer_id FROM conversations WHERE peer_id = %s", (self.peer_id,))
		if res == 0:
			chat = self.vk.messages.getConversationsById(peer_ids=self.peer_id)['items'][0]["chat_settings"]
			user_count = chat["members_count"]
			admin_id = chat["owner_id"]
			curs.execute(
					"INSERT INTO conversations (peer_id,user_count,admin_id) VALUES (%s,%s,%s)",
					(self.peer_id, user_count, admin_id)
					)
			conn.commit( )
		else:
			pass
	
	def registrarionUser(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		res = curs.execute("SELECT user_id FROM users WHERE user_id = %s", (self.user_id,))
		if res == 0:
			user = self.vk.users.get(user_ids=self.user_id)
			user_name = f"{user[0]['first_name']} {user[0]['last_name']}"
			curs.execute(
					"INSERT INTO users(user_id,peer_id,anders,nickname,food) VALUES (%s,%s,%s,%s,%s)",
					(self.user_id, self.peer_id, 0, user_name, 10)
					)
			conn.commit( )
		else:
			pass
	
	def addResourse(self):
		if self.user_id in self.adms:
			res_cost = self.txt.split("\n")[2]
			res_count = self.txt.split("\n")[3]
			res_name = self.txt.split("\n")[1]
			if res_cost.isdigit( ) and res_count.isdigit( ):
				conn = pymysql.connect(
						host="remotemysql.com",
						user=self.user,
						password=self.passw,
						db='IMR5jUaWZE'
						)
				curs = conn.cursor( )
				res = curs.execute("SELECT * FROM resourses WHERE name = %s", (res_name,))
				if res == 0:
					curs.execute(
							"INSERT INTO resourses (name, count, cost) VALUES (%s, %s, %s)",
							(res_name, res_count, res_cost)
							)
					conn.commit( )
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Ресурс успешно добавлен в базу данных."
							)
				else:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Данный ресурс уже есть в базе данных."
							)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Один из аргументов указан неверно."
						)
	
	def addMilitary(self):
		if self.user_id in self.adms:
			mil_name = self.txt.split("\n")[1]
			mil_cost = self.txt.split("\n")[2]
			mil_count = self.txt.split("\n")[3]
			mil_expn = self.txt.split("\n")[4]
			if mil_cost.isdigit( ) and mil_count.isdigit( ) and mil_expn.isdigit( ):
				conn = pymysql.connect(
						host="remotemysql.com",
						user=self.user,
						password=self.passw,
						db='IMR5jUaWZE'
						)
				curs = conn.cursor( )
				mil_check = curs.execute("SELECT * FROM military WHERE name = %s", (mil_name,))
				if mil_check == 0:
					curs.execute(
							"INSERT INTO military (name, expn, count, cost) VALUES (%s, %s, %s, %s)",
							(mil_name, mil_expn, mil_count, mil_cost)
							)
					conn.commit( )
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Вид войска успешно добавлен в базу данных."
							)
				else:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Данный вид войска уже есть в базе данных."
							)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Один из аргументов указан неверно."
						)
	
	def addBuild(self):
		if self.user_id in self.adms:
			name = self.txt.split("\n")[1]
			cost = self.txt.split("\n")[2]
			prof = self.txt.split("\n")[3]
			res_id = self.txt.split("\n")[4]
			if cost.isdigit( ) and res_id.isdigit( ) and prof.isdigit( ):
				conn = pymysql.connect(
						host="remotemysql.com",
						user=self.user,
						password=self.passw,
						db='IMR5jUaWZE'
						)
				curs = conn.cursor( )
				build_check = curs.execute("SELECT * FROM builds WHERE name = %s", (name,))
				if build_check == 0:
					res_check = curs.execute("SELECT * FROM resourses WHERE res_id = %s", (res_id,))
					if res_check == 0:
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message="В базе данных не существует указанного ID ресурса."
								)
					else:
						curs.execute(
								"INSERT INTO builds (name, cost, profit, res_id) VALUES (%s, %s, %s, %s)",
								(name, cost, prof, res_id)
								)
						conn.commit( )
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message="Постройка успешно добавлена в базу данных."
								)
				else:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Данная постройка уже есть в базе данных."
							)
			
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Один из аргументов указан неверно."
						)
	
	def collectResourses(self):
		now_utc = datetime.now(timezone('UTC'))
		time = now_utc.astimezone(timezone('Europe/Moscow'))
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		now = int(time.timestamp( ))
		curs.execute("SELECT last_res_coll FROM users WHERE user_id = %s", (self.user_id,))
		resp = int(curs.fetchone( )[0])
		a = now - resp
		if resp == 0 or a >= 86400:
			curs.execute(
					"SELECT mine, vlg, farm, city, tmpl, altr, swml FROM users WHERE user_id = %s", (self.user_id,)
					)
			data = curs.fetchone( )
			curs.execute("SELECT build_id FROM builds ORDER BY build_id DESC")
			count = curs.fetchone( )[0] - 1
			curs.execute("SELECT profit FROM builds")
			prof = curs.fetchall( )
			res = []
			for i in range(count + 1):
				mine = data[i] * prof[i][0]
				res.append(mine)
			curs.execute(
					f"UPDATE users SET steel = {res[0]}, anders = {res[1] + res[3]}, food = {res[2]}, w_cris = {res[4]}, b_cris = {res[5]}, wood = {res[6]}, last_res_coll = {now} WHERE user_id = %s",
					(self.user_id,)
					)
			conn.commit( )
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message=f"Ресурсы собраны!\nДерево: {res[6]}\nМеталлы: {res[0]}\nПродовольствие: {res[2]}\nКристаллы Тьмы: {res[4]}\nКристаллы Света:{res[5]}\nАндеры: {res[1] + res[3]}"
					)
		else:
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message="Вы уже собирали ресурсы."
					)
	
	def collectExpirience(self):
		now_utc = datetime.now(timezone('UTC'))
		time = now_utc.astimezone(timezone('Europe/Moscow'))
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		now = int(time.timestamp( ))
		curs.execute("SELECT last_exp_coll FROM users WHERE user_id = %s", (self.user_id,))
		resp = int(curs.fetchone( )[0])
		a = now - resp
		if resp == 0 or a >= 259200:
			curs.execute(
					"SELECT inf, arch, clvr, plds, mag, ctpl, bllsts FROM users WHERE user_id = %s", (self.user_id,)
					)
			data = curs.fetchone( )
			mil = 0
			for i in data:
				mil = i + mil
			res = mil * 0.1
			curs.execute(f"UPDATE users SET exp = exp + {res}, last_exp_coll = {now} WHERE user_id = {self.user_id}")
			conn.commit( )
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message=f"Вы получили {round(res, 4)} ед. опыта."
					)
		else:
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message="Вы уже собирали опыт."
					)
	
	def listOfMillitaryObj(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		
		curs.execute("SELECT anders FROM users WHERE user_id = %s", (self.user_id,))
		builds = curs.fetchone( )
		stats_pic = Image.open("military.png")
		stats_pic_draw = ImageDraw.Draw(stats_pic)
		font = ImageFont.truetype("Aqum.ttf", size=23)
		stats_pic_draw.text(xy=(365, 180), text=str(builds[0]), fill="black", font=font)
		
		stats_pic.save('mil.png')
		
		vk_upload = vk_api.VkUpload(self.vk_session)
		photo = vk_upload.photo_messages(photos="mil.png", peer_id=self.peer_id)
		photo = f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}'
		self.vk.messages.send(
				peer_id=self.peer_id, random_id=random.randint(0, 10000000000), attachment=photo
				)
	
	def listOfBuilds(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		
		curs.execute("SELECT anders FROM users WHERE user_id = %s", (self.user_id,))
		builds = curs.fetchone( )
		stats_pic = Image.open("builds.png")
		stats_pic_draw = ImageDraw.Draw(stats_pic)
		font = ImageFont.truetype("Aqum.ttf", size=23)
		stats_pic_draw.text(xy=(365, 180), text=str(builds[0]), fill="black", font=font)
		
		stats_pic.save('build.png')
		
		vk_upload = vk_api.VkUpload(self.vk_session)
		photo = vk_upload.photo_messages(photos="build.png", peer_id=self.peer_id)
		photo = f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}'
		self.vk.messages.send(
				peer_id=self.peer_id, random_id=random.randint(0, 10000000000), attachment=photo
				)
	
	def buyMillitaryObj(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		curs.execute("SELECT anders FROM users WHERE user_id = %s", (self.user_id,))
		user_profile = curs.fetchone( )
		mil_id = self.command.split(" ")[1]
		if mil_id.isdigit( ):
			curs.execute("SELECT cost, count, bd_name, name FROM military WHERE mil_id = %s", (mil_id,))
			mil = curs.fetchone( )
			if mil is not None:
				if user_profile[0] >= mil[0]:
					curs.execute(
							f"UPDATE users SET {mil[2]} = {mil[2]} + {mil[1]}, anders = anders - {mil[0]} WHERE user_id = {self.user_id}"
							)
					conn.commit( )
					morph = pymorphy2.MorphAnalyzer( )
					mil_name = morph.parse(mil[3])[0]
					mil_name = mil_name.inflect({'gent'}).word.capitalize( )
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message=f"Поздравляем!\nВы приобрели {mil[1]} {mil_name}!"
							)
				else:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message=f"Вам нужно еще {mil[0] - user_profile[0]} ед. Андеров."
							)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Боевой единицы с таким ID не существует."
						)
		
		else:
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message="Вы неверно указали ID здания."
					)
	
	def buyBuild(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		curs.execute("SELECT steel, wood, food, w_cris, b_cris FROM users WHERE user_id = %s", (self.user_id,))
		user_profile = curs.fetchone( )
		build_id = self.command.split(" ")[1]
		if build_id.isdigit( ):
			curs.execute(
					"SELECT food, steel, wood, b_cris, w_cris, build_name, name FROM builds WHERE build_id = %s",
					(build_id,)
					)
			build = curs.fetchone( )
			if build is None:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Здания с таким ID не существует."
						)
			else:
				if user_profile[2] >= build[0]:
					if user_profile[0] >= build[1]:
						if user_profile[1] >= build[2]:
							if user_profile[3] >= build[4]:
								if user_profile[4] >= build[3]:
									curs.execute(
											f"UPDATE users SET {build[5]} = {build[5]} + 1, wood = wood - {build[2]}, steel = steel - {build[2]}, food = food - {build[0]}, b_cris = b_cris - {build[3]}, w_cris = w_cris - {build[4]} WHERE user_id = {self.user_id}"
											)
									conn.commit( )
									morph = pymorphy2.MorphAnalyzer( )
									build_name = morph.parse(build[6])[0]
									build_name = build_name.inflect({'gent'}).word.capitalize( )
									self.vk.messages.send(
											peer_id=self.peer_id,
											random_id=random.randint(0, 10000000000),
											message=f"Поздравляем вас с покупкой {build_name}!"
											)
								else:
									self.vk.messages.send(
											peer_id=self.peer_id,
											random_id=random.randint(0, 10000000000),
											message=f"У вас не хватает {build[4] - user_profile[3]} ед. Кристалов Тьмы."
											)
							else:
								self.vk.messages.send(
										peer_id=self.peer_id,
										random_id=random.randint(0, 10000000000),
										message=f"У вас не хватает {build[4] - user_profile[3]} ед. Кристалов Cвета."
										)
						else:
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"У вас не хватает {build[2] - user_profile[1]} ед. Дерева."
									)
					else:
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message=f"У вас не хватает {build[1] - user_profile[0]} ед. Металлов."
								)
				else:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message=f"У вас не хватает {build[0] - user_profile[2]} ед. Еды."
							)
		else:
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message="Вы неверно указали ID здания."
					)
	
	def transaction(self):
		# /trans [кол во] [адресат]
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		
		val = self.command.split(" ")[1]
		if val.isdigit( ):
			curs.execute("SELECT anders FROM users WHERE user_id = %s", (self.user_id,))
			if curs.fetchone( )[0] >= int(val):
				if self.command.split(" ")[2].startswith("[id"):
					try:
						to_user = self.command.split(" ")[2].split("|")[0].repladce("[id", "")
						curs.execute("SELECT user_id FROM users WHERE user_id = %s", (to_user,))
						if curs.fetchone( ) is None:
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"[id{to_user}|Этот пальзователь] не зарегистрирован в базе данных бота."
									)
						else:
							now_utc = datetime.now(timezone('UTC'))
							time = str(now_utc.astimezone(timezone('Europe/Moscow'))).split(".")[0]
							curs.execute(f"UPDATE users SET anders = anders + {val} WHERE user_id = {to_user}")
							conn.commit( )
							curs.execute(f"UPDATE users SET anders = anders - {val} WHERE user_id = {self.user_id}")
							conn.commit( )
							curs.execute(
									f"INSERT INTO transactions (from_user, to_user, datetime, summ) VALUES (%s, %s, %s, %s)",
									(self.user_id, to_user, time, val)
									)
							conn.commit( )
							curs.execute("SELECT trans_id FROM transactions ORDER BY trans_id DESC LIMIT 1")
							last_post = curs.fetchone( )[0]
							self.vk.messages.send(
									peer_id=self.adms_chat,
									random_id=random.randint(0, 10000000000),
									message=f"Перевод:\n FROM: @id{self.user_id}\nTO: @id{to_user}\n SUMM: {val}\nTRANS_ID: {last_post}"
									)
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"[id{to_user}|Вам] пришло {val} Андеров от @id{self.user_id}"
									)
					except Exception as err:
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message=f"Произошла ошибка. Возможно данная ссылка не ведет на страницу пользователя\n{err}"
								)
				
				elif self.command.split(" ")[2].startswith("https://vk.com/"):
					try:
						to_user = self.vk.users.get(user_ids=self.command.split(" ")[2].split("/")[3])[0]['id']
						curs.execute("SELECT user_id FROM users WHERE user_id = %s", (to_user,))
						if curs.fetchone( ) is None:
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"[id{to_user}|Этот пальзователь] не зарегистрирован в базе данных бота."
									)
						else:
							now_utc = datetime.now(timezone('UTC'))
							time = str(now_utc.astimezone(timezone('Europe/Moscow'))).split(".")[0]
							curs.execute(f"UPDATE users SET anders = anders + {val} WHERE user_id = {to_user}")
							conn.commit( )
							curs.execute(f"UPDATE users SET anders = anders - {val} WHERE user_id = {self.user_id}")
							conn.commit( )
							curs.execute(
									f"INSERT INTO transactions (from_user, to_user, datetime, summ) VALUES (%s, %s, %s, %s)",
									(self.user_id, to_user, time, val)
									)
							conn.commit( )
							curs.execute("SELECT trans_id FROM transactions ORDER BY trans_id DESC LIMIT 1")
							last_post = curs.fetchone( )[0]
							self.vk.messages.send(
									peer_id=self.adms_chat,
									random_id=random.randint(0, 10000000000),
									message=f"Перевод:\n FROM: @id{self.user_id}\nTO: @id{to_user}\n SUMM: {val}\nTRANS_ID: {last_post}"
									)
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"[id{to_user}|Вам] пришло {val} Андеров от @id{self.user_id}"
									)
					except Exception as err:
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message=f"Произошла ошибка. Данная ссылка не ведет на страницу пользователя\n{err}"
								)
				elif self.command.split(" ")[2].startswith("vk.com/"):
					try:
						to_user = self.vk.users.get(user_ids=self.command.split(" ")[2].split("/")[1])[0]['id']
						curs.execute("SELECT user_id FROM users WHERE user_id = %s", (to_user,))
						if curs.fetchone( ) is None:
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"[id{to_user}|Этот пальзователь] не зарегистрирован в базе данных бота."
									)
						else:
							now_utc = datetime.now(timezone('UTC'))
							time = str(now_utc.astimezone(timezone('Europe/Moscow'))).split(".")[0]
							curs.execute(f"UPDATE users SET anders = anders + {val} WHERE user_id = {to_user}")
							conn.commit( )
							curs.execute(f"UPDATE users SET anders = anders - {val} WHERE user_id = {self.user_id}")
							conn.commit( )
							curs.execute(
									f"INSERT INTO transactions (from_user, to_user, datetime, summ) VALUES (%s, %s, %s, %s)",
									(self.user_id, to_user, time, val)
									)
							conn.commit( )
							curs.execute("SELECT trans_id FROM transactions ORDER BY trans_id DESC LIMIT 1")
							last_post = curs.fetchone( )[0]
							self.vk.messages.send(
									peer_id=self.adms_chat,
									random_id=random.randint(0, 10000000000),
									message=f"Перевод:\n FROM: @id{self.user_id}\nTO: @id{to_user}\n SUMM: {val}\nTRANS_ID: {last_post}"
									)
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"[id{to_user}|Вам] пришло {val} Андеров от @id{self.user_id}"
									)
					except Exception as err:
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message=f"Произошла ошибка. Данная ссылка не ведет на страницу пользователя\n{err}"
								)
				
				elif self.event.object["reply_message"] is not None:
					if self.event.object["reply_message"]["from_id"] > 0:
						to_user = self.event.object["reply_message"]["from_id"]
						curs.execute("SELECT user_id FROM users WHERE user_id = %s", (to_user,))
						if curs.fetchone( ) is None:
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"[id{to_user}|Этот пальзователь] не зарегистрирован в базе данных бота."
									)
						else:
							now_utc = datetime.now(timezone('UTC'))
							time = str(now_utc.astimezone(timezone('Europe/Moscow'))).split(".")[0]
							curs.execute(f"UPDATE users SET anders = anders + {val} WHERE user_id = {to_user}")
							conn.commit( )
							curs.execute(f"UPDATE users SET anders = anders - {val} WHERE user_id = {self.user_id}")
							conn.commit( )
							curs.execute(
									f"INSERT INTO transactions (from_user, to_user, datetime, summ) VALUES (%s, %s, %s, %s)",
									(self.user_id, to_user, time, val)
									)
							conn.commit( )
							curs.execute("SELECT trans_id FROM transactions ORDER BY trans_id DESC LIMIT 1")
							last_post = curs.fetchone( )[0]
							self.vk.messages.send(
									peer_id=self.adms_chat,
									random_id=random.randint(0, 10000000000),
									message=f"Перевод:\n FROM: @id{self.user_id}\nTO: @id{to_user}\n SUMM: {val}\nTRANS_ID: {last_post}"
									)
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message=f"[id{to_user}|Вам] пришло {val} Андеров от @id{self.user_id}"
									)
					else:
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message=f"[club{str(self.event.object['reply_message']['from_id']).replace('-', '')}|Эта страница] не является страницей пользователя."
								)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="У вас недостаточно средств."
						)
		else:
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message="Вы неверно указали сумму перевода."
					)
	
	def transactionRejection(self):
		if self.user_id in self.adms:
			conn = pymysql.connect(
					host="remotemysql.com",
					user=self.user,
					password=self.passw,
					db='IMR5jUaWZE'
					)
			curs = conn.cursor( )
			
			trans_id = self.command.split(" ")[1]
			
			if trans_id.isdigit( ):
				curs.execute('SELECT * FROM transactions WHERE trans_id = %s', (trans_id,))
				trans_info = curs.fetchone( )
				if trans_info is None:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Транзакции с таким ID не существует."
							)
				else:
					curs.execute(f"UPDATE users SET anders = anders - {trans_info[3]} WHERE user_id = {trans_info[2]}")
					conn.commit( )
					curs.execute(f"UPDATE users SET anders = anders + {trans_info[3]} WHERE user_id = {trans_info[1]}")
					conn.commit( )
					curs.execute(f"UPDATE users SET access = 0 WHERE trans_id = {trans_id}")
					conn.commit( )
					
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message=f"Транзанкция #{trans_id} отменена."
							)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="ID транзакции должно состоять только из цифр."
						)
	
	def raceInformation(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		
		stats_pic = Image.open("interfeys_dlya_bota_V2.png")
		stats_pic_draw = ImageDraw.Draw(stats_pic)
		font = ImageFont.truetype("Aqum.ttf", size=20)
		
		if len(self.command.split(" ")) <= 2:
			curs.execute(f"SELECT race_id FROM users WHERE user_id = {self.user_id}")
			race_id = curs.fetchall( )
			curs.execute(
					"SELECT SUM(anders), SUM(food), SUM(steel), SUM(wood), SUM(w_cris), SUM(b_cris), SUM(exp) FROM users WHERE race_id = %s",
					(race_id,)
					)
			race_inv = curs.fetchone( )
			
			curs.execute(
					"SELECT SUM(inf),SUM(mag),SUM(arch),SUM(ctpl),SUM(bllsts),SUM(clvr),SUM(plds) FROM users WHERE race_id = %s",
					(race_id,)
					)
			mil_inv = curs.fetchone( )
			
			curs.execute(
					"SELECT SUM(farm),SUM(swml),SUM(mine),SUM(vlg),SUM(city),SUM(tmpl),SUM(altr) FROM users WHERE race_id = %s",
					(race_id,)
					)
			bld_inv = curs.fetchone( )
			curs.execute(
					"SELECT name FROM races WHERE race_id = %s",
					(race_id,)
					)
			stats_pic_draw.text(
					xy=(245, 71), text=curs.fetchone( )[0], fill="white", font=ImageFont.truetype("Aqum.ttf", size=35)
					)
			
			stats_pic_draw.text(xy=(207, 419), text=str(mil_inv[0]), fill="black", font=font)
			stats_pic_draw.text(xy=(207, 518), text=str(mil_inv[2]), fill="black", font=font)
			stats_pic_draw.text(xy=(207, 617), text=str(mil_inv[5]), fill="black", font=font)
			stats_pic_draw.text(xy=(207, 716), text=str(mil_inv[6]), fill="black", font=font)
			stats_pic_draw.text(xy=(207, 814), text=str(mil_inv[1]), fill="black", font=font)
			stats_pic_draw.text(xy=(207, 912), text=str(mil_inv[3]), fill="black", font=font)
			stats_pic_draw.text(xy=(207, 1011), text=str(mil_inv[4]), fill="black", font=font)
			
			stats_pic_draw.text(
					xy=(357, 174), text=str(round(race_inv[6], 3)), fill="white",
					font=ImageFont.truetype("Aqum.ttf", size=25)
					)
			stats_pic_draw.text(
					xy=(835, 174), text=str(race_inv[1]), fill="white", font=ImageFont.truetype("Aqum.ttf", size=25)
					)
			
			stats_pic_draw.text(xy=(631, 419), text=str(race_inv[1]), fill="black", font=font)
			stats_pic_draw.text(xy=(631, 518), text=str(race_inv[3]), fill="black", font=font)
			stats_pic_draw.text(xy=(631, 617), text=str(race_inv[2]), fill="black", font=font)
			stats_pic_draw.text(xy=(631, 716), text=str(race_inv[4]), fill="black", font=font)
			stats_pic_draw.text(xy=(631, 814), text=str(race_inv[5]), fill="black", font=font)
			
			stats_pic_draw.text(xy=(1055, 419), text=str(bld_inv[0]), fill="black", font=font)
			stats_pic_draw.text(xy=(1055, 518), text=str(bld_inv[1]), fill="black", font=font)
			stats_pic_draw.text(xy=(1055, 617), text=str(bld_inv[2]), fill="black", font=font)
			stats_pic_draw.text(xy=(1055, 716), text=str(bld_inv[3]), fill="black", font=font)
			stats_pic_draw.text(xy=(1055, 814), text=str(bld_inv[4]), fill="black", font=font)
			stats_pic_draw.text(xy=(1055, 912), text=str(bld_inv[5]), fill="black", font=font)
			stats_pic_draw.text(xy=(1055, 1011), text=str(bld_inv[6]), fill="black", font=font)
			
			stats_pic.save('stats.png')
			
			vk_upload = vk_api.VkUpload(self.vk_session)
			photo = vk_upload.photo_messages(photos="stats.png", peer_id=self.peer_id)
			photo = f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}'
			self.vk.messages.send(peer_id=self.peer_id, random_id=random.randint(0, 10000000000), attachment=photo)
		else:
			print(4)
			race = self.command.split(" ")[1]
			if race.isdigit( ):
				curs.execute(
						"SELECT SUM(anders), SUM(food), SUM(steel), SUM(wood), SUM(w_cris), SUM(b_cris), SUM(exp) FROM users WHERE race_id = %s",
						(race,)
						)
				race_inv = curs.fetchone( )
				
				curs.execute(
						"SELECT SUM(inf),SUM(mag),SUM(arch),SUM(ctpl),SUM(bllsts),SUM(clvr),SUM(plds) FROM users WHERE race_id = %s",
						(race,)
						)
				mil_inv = curs.fetchone( )
				
				curs.execute(
						"SELECT SUM(farm),SUM(swml),SUM(mine),SUM(vlg),SUM(city),SUM(tmpl),SUM(altr) FROM users WHERE race_id = %s",
						(race,)
						)
				bld_inv = curs.fetchone( )
				curs.execute(
						"SELECT name FROM races WHERE race_id = %s",
						(race,)
						)
				stats_pic_draw.text(
						xy=(245, 71), text=curs.fetchone( )[0], fill="white",
						font=ImageFont.truetype("Aqum.ttf", size=35)
						)
				
				stats_pic_draw.text(xy=(207, 419), text=str(mil_inv[0]), fill="black", font=font)
				stats_pic_draw.text(xy=(207, 518), text=str(mil_inv[2]), fill="black", font=font)
				stats_pic_draw.text(xy=(207, 617), text=str(mil_inv[5]), fill="black", font=font)
				stats_pic_draw.text(xy=(207, 716), text=str(mil_inv[6]), fill="black", font=font)
				stats_pic_draw.text(xy=(207, 814), text=str(mil_inv[1]), fill="black", font=font)
				stats_pic_draw.text(xy=(207, 912), text=str(mil_inv[3]), fill="black", font=font)
				stats_pic_draw.text(xy=(207, 1011), text=str(mil_inv[4]), fill="black", font=font)
				
				stats_pic_draw.text(
						xy=(357, 174), text=str(round(race_inv[6], 3)), fill="white",
						font=ImageFont.truetype("Aqum.ttf", size=25)
						)
				stats_pic_draw.text(
						xy=(835, 174), text=str(race_inv[1]), fill="white",
						font=ImageFont.truetype("Aqum.ttf", size=25)
						)
				
				stats_pic_draw.text(xy=(631, 419), text=str(race_inv[1]), fill="black", font=font)
				stats_pic_draw.text(xy=(631, 518), text=str(race_inv[3]), fill="black", font=font)
				stats_pic_draw.text(xy=(631, 617), text=str(race_inv[2]), fill="black", font=font)
				stats_pic_draw.text(xy=(631, 716), text=str(race_inv[4]), fill="black", font=font)
				stats_pic_draw.text(xy=(631, 814), text=str(race_inv[5]), fill="black", font=font)
				
				stats_pic_draw.text(xy=(1055, 419), text=str(bld_inv[0]), fill="black", font=font)
				stats_pic_draw.text(xy=(1055, 518), text=str(bld_inv[1]), fill="black", font=font)
				stats_pic_draw.text(xy=(1055, 617), text=str(bld_inv[2]), fill="black", font=font)
				stats_pic_draw.text(xy=(1055, 716), text=str(bld_inv[3]), fill="black", font=font)
				stats_pic_draw.text(xy=(1055, 814), text=str(bld_inv[4]), fill="black", font=font)
				stats_pic_draw.text(xy=(1055, 912), text=str(bld_inv[5]), fill="black", font=font)
				stats_pic_draw.text(xy=(1055, 1011), text=str(bld_inv[6]), fill="black", font=font)
				
				stats_pic.save('stats.png')
				
				vk_upload = vk_api.VkUpload(self.vk_session)
				photo = vk_upload.photo_messages(photos="stats.png", peer_id=self.peer_id)
				photo = f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}'
				self.vk.messages.send(
						peer_id=self.peer_id, random_id=random.randint(0, 10000000000), attachment=photo
						)
			else:
				curs.execute("SELECT race_id FROM reces WHERE low_name = %s", (race,))
				race_id = curs.fetchone( )
				if race_id is None:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Расы с таким названием не существует."
							)
				else:
					curs.execute(f"SELECT race_id FROM users WHERE user_id = {self.user_id}")
					race_id = curs.fetchall( )
					curs.execute(
							"SELECT SUM(anders), SUM(food), SUM(steel), SUM(wood), SUM(w_cris), SUM(b_cris), SUM(exp) FROM users WHERE race_id = %s",
							(race_id,)
							)
					race_inv = curs.fetchone( )
					
					curs.execute(
							"SELECT SUM(inf),SUM(mag),SUM(arch),SUM(ctpl),SUM(bllsts),SUM(clvr),SUM(plds) FROM users WHERE race_id = %s",
							(race_id,)
							)
					mil_inv = curs.fetchone( )
					
					curs.execute(
							"SELECT SUM(farm),SUM(swml),SUM(mine),SUM(vlg),SUM(city),SUM(tmpl),SUM(altr) FROM users WHERE race_id = %s",
							(race_id,)
							)
					bld_inv = curs.fetchone( )
					curs.execute(
							"SELECT name FROM races WHERE race_id = %s",
							(race_id,)
							)
					stats_pic_draw.text(
							xy=(245, 71), text=curs.fetchone( )[0], fill="white",
							font=ImageFont.truetype("Aqum.ttf", size=35)
							)
					
					stats_pic_draw.text(xy=(207, 419), text=str(mil_inv[0]), fill="black", font=font)
					stats_pic_draw.text(xy=(207, 518), text=str(mil_inv[2]), fill="black", font=font)
					stats_pic_draw.text(xy=(207, 617), text=str(mil_inv[5]), fill="black", font=font)
					stats_pic_draw.text(xy=(207, 716), text=str(mil_inv[6]), fill="black", font=font)
					stats_pic_draw.text(xy=(207, 814), text=str(mil_inv[1]), fill="black", font=font)
					stats_pic_draw.text(xy=(207, 912), text=str(mil_inv[3]), fill="black", font=font)
					stats_pic_draw.text(xy=(207, 1011), text=str(mil_inv[4]), fill="black", font=font)
					
					stats_pic_draw.text(
							xy=(357, 174), text=str(round(race_inv[6], 3)), fill="white",
							font=ImageFont.truetype("Aqum.ttf", size=25)
							)
					stats_pic_draw.text(
							xy=(835, 174), text=str(race_inv[1]), fill="white",
							font=ImageFont.truetype("Aqum.ttf", size=25)
							)
					
					stats_pic_draw.text(xy=(631, 419), text=str(race_inv[1]), fill="black", font=font)
					stats_pic_draw.text(xy=(631, 518), text=str(race_inv[3]), fill="black", font=font)
					stats_pic_draw.text(xy=(631, 617), text=str(race_inv[2]), fill="black", font=font)
					stats_pic_draw.text(xy=(631, 716), text=str(race_inv[4]), fill="black", font=font)
					stats_pic_draw.text(xy=(631, 814), text=str(race_inv[5]), fill="black", font=font)
					
					stats_pic_draw.text(xy=(1055, 419), text=str(bld_inv[0]), fill="black", font=font)
					stats_pic_draw.text(xy=(1055, 518), text=str(bld_inv[1]), fill="black", font=font)
					stats_pic_draw.text(xy=(1055, 617), text=str(bld_inv[2]), fill="black", font=font)
					stats_pic_draw.text(xy=(1055, 716), text=str(bld_inv[3]), fill="black", font=font)
					stats_pic_draw.text(xy=(1055, 814), text=str(bld_inv[4]), fill="black", font=font)
					stats_pic_draw.text(xy=(1055, 912), text=str(bld_inv[5]), fill="black", font=font)
					stats_pic_draw.text(xy=(1055, 1011), text=str(bld_inv[6]), fill="black", font=font)
					
					stats_pic.save('stats.png')
					
					vk_upload = vk_api.VkUpload(self.vk_session)
					photo = vk_upload.photo_messages(photos="stats.png", peer_id=self.peer_id)
					photo = f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}'
					self.vk.messages.send(
							peer_id=self.peer_id, random_id=random.randint(0, 10000000000), attachment=photo
							)
	
	def setRace(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		if self.user_id in self.adms:
			user = self.command.split(" ")[1].split("|")[0]
			race = self.command.split(" ")[2]
			if race.isdigit( ):
				curs.execute("SELECT race_id FROM races WHERE race_id = %s", (race,))
				if curs.fetchone( ) is None:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Расы с таким ID не существует."
							)
				else:
					if user.startswith("[id"):
						user = user.replace("[id", "")
						curs.execute("SELECT user_id FROM users WHERE user_id = %s", (user,))
						if curs.fetchone( ) is None:
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message="Данный пользователь не зарегистрирован в базе данных."
									)
						else:
							curs.execute("UPDATE users SET race_id = %s WHERE user_id = %s", (race, user))
							conn.commit( )
							self.vk.messages.send(
									peer_id=self.peer_id,
									random_id=random.randint(0, 10000000000),
									message="Вы изменили расу пользователю."
									)
					else:
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message="Гиперссылка должна вести на страницу человека."
								)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="ID расы должно состоять только из цифр."
						)
		else:
			curs.execute(f"SELECT race_id FROM users WHERE user_id = {self.user_id}")
			if curs.fetchone( )[0] == 0:
				race = self.command.split(" ")[0]
				if race.isdigit( ):
					curs.execute("SELECT race_id FROM races ORDER BY race_id DESC LIMIT 1")
					maxi = curs.fetchone( )[0]
					if maxi >= int(race) >= 1:
						curs.execute(f"UPDATE users SET race_id = {race} WHERE user_id = {self.user_id}")
						conn.commit( )
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message="Раса успешно установлена."
								)
				else:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="ID расы должно состоять только из цифр."
							)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Вы уже выбрали свою расу. Чтобы ее изменить - обратитесь к администрации."
						)
	
	def changeNickname(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		name = self.txt.split(" ", 1)[1]
		if len(name) >= 12:
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message="Ваш ник слишком длинный."
					)
		else:
			curs.execute("SELECT user_id FROM users WHERE nick_name = %s", (name,))
			if curs.fetchone( ) is None:
				curs.execute("UPDATE users SET nickname = %s WHERE user_id = %s", (name, self.user_id))
				conn.commit( )
				# нужно переложить ответственность за ник на пользователя
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Ник успешно изменен."
						)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Этот ник уже кем-то занят."
						)
	
	def listOfGoods(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		curs.execute("SELECT lot_id, from_user, res_id, count, cost FROM market WHERE purch = 0")
		goods = curs.fetchall( )
		a = ""
		for i in goods:
			curs.execute(f"SELECT name FROM resourses WHERE res_id = {i[2]}")
			a += f"ID: {i[0]}\nПродавец: @id{i[1]}\nСтоимость: {i[4]} ед. Андеров\nРесурс: {curs.fetchone( )[0]}\nКол-во: {i[3]}\n\n"
		self.vk.messages.send(
				peer_id=self.peer_id,
				random_id=random.randint(0, 10000000000),
				message=f"Список лотов:\n{a}ЧТОБЫ КУПИТЬ ЛОТ НАПИШИТЕ '/buy [ID лота]' (без кавычек)"
				)
	
	def buyGood(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		now_utc = datetime.now(timezone('UTC'))
		time = now_utc.astimezone(timezone('Europe/Moscow'))
		lot_id = self.command.split(" ")[1]
		if lot_id.isdigit( ):
			curs.execute("SELECT count, res_id, cost, from_user FROM market WHERE lot_id = %s", (lot_id,))
			lot = curs.fetchone( )
			if lot[3] == self.user_id:
				if lot is None:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message="Лота с таким ID не существует."
							)
				else:
					curs.execute("SELECT anders FROM users WHERE user_id = %s", (self.user_id,))
					money = curs.fetchone( )[0]
					if money >= lot[2]:
						curs.execute("SELECT bd_name, name FROM resourses WHERE res_id = %s", (lot[1],))
						res_name = curs.fetchone( )
						curs.execute(
								f"UPDATE users SET anders = anders - {lot[2]}, {res_name[0]} = {res_name[0]} + {lot[0]} WHERE user_id = {self.user_id}"
								)
						conn.commit( )
						curs.execute(
								f"UPDATE users SET anders = anders + {lot[2]}, {res_name[0]} = {res_name[0]} - {lot[0]} WHERE user_id = {lot[3]}"
								)
						conn.commit( )
						curs.execute(f"UPDATE market SET purch_time = %s, to_user = {self.user_id}, purch = 1", (time,))
						conn.commit( )
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message=f"Вы купили {lot[0]} ед. {res_name[1]}!\n\n[id{lot[3]}|Лот #{lot_id}] продан!"
								)
					
					else:
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message="У вас недостаточно Андеров."
								)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Нельзя купить свой же лот."
						)
		else:
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message="ID лота должно состоять только из цифр."
					)
	
	def addGood(self):
		"""
		/addgood
		[ресурс]
		[кол-во]
		[стоимость за ед.]
		"""
		res_name = self.command.split("\n")[1].capitalize( ).strip( )
		res_count = self.command.split("\n")[2].strip( )
		res_cost = self.command.split("\n")[3].strip( )
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		now_utc = datetime.now(timezone('UTC'))
		time = now_utc.astimezone(timezone('Europe/Moscow'))
		curs.execute("SELECT cost, res_id, bd_name FROM resourses WHERE name = %s", (res_name,))
		res = curs.fetchone( )
		if res is None:
			self.vk.messages.send(
					peer_id=self.peer_id,
					random_id=random.randint(0, 10000000000),
					message="Ресурса с таким названием не существует."
					)
		else:
			if res_cost.isdigit( ) and res_count.isdigit( ):
				curs.execute(f"SELECT {res[2]} FROM users WHERE user_id = {self.user_id}")
				if curs.fetchone( )[0] >= int(res_count):
					if res[0] >= int(res_cost):
						cost = int(res_cost) * int(res_count)
						curs.execute(
								"INSERT INTO market (from_user, cost, res_id, count, time) VALUE (%s,%s,%s,%s,%s)",
								(self.user_id, cost, res[1], res_count, time)
								)
						conn.commit( )
						curs.execute("SELECT lot_id FROM market ORDER BY lot_id DESC LIMIT 1")
						lot = curs.fetchone( )[0]
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message=f"Лот #{lot} выставлен на продажу!"
								)
					else:
						morph = pymorphy2.MorphAnalyzer( )
						res_name = morph.parse(res_name[3])[0]
						res_name = res_name.inflect({'gent'})
						self.vk.messages.send(
								peer_id=self.peer_id,
								random_id=random.randint(0, 10000000000),
								message=f"Минимальная цена за 1 ед. {res_name}: {res[0]}."
								)
				else:
					morph = pymorphy2.MorphAnalyzer( )
					res_name = morph.parse(res_name[3])[0]
					res_name = res_name.inflect({'gent'})
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message=f"У вас недостаточно {res_name}."
							)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="Аргументы указаны неверно. Проверьте, чтоб стоимость и количество были указаны числами."
						)
	
	def rejectonLot(self):
		"""
		/rejlot [lot_id]
		"""
		if self.user_id in self.adms:
			lot_id = self.command.split(" ")[1]
			conn = pymysql.connect(
					host="remotemysql.com",
					user=self.user,
					password=self.passw,
					db='IMR5jUaWZE'
					)
			curs = conn.cursor( )
			if lot_id.isdigit( ):
				curs.execute(
						"SELECT to_user, from_user, cost, res_id, count, purch FROM market WHERE lot_id = %s", (lot_id,)
						)
				lot = curs.fetchone( )
				if lot[5] == 1:
					curs.execute(f"SELECT bd_name FROM resourses WHERE res_id = {lot[3]}")
					res_name = curs.fetchone( )[0]
					curs.execute(
							f"UPDATE users SET anders = anders + {lot[2]}, {res_name} = {res_name} - {lot[4]} WHERE user_id = {lot[0]}"
							)
					conn.commit( )
					curs.execute(
							f"UPDATE users SET anders = anders - {lot[2]}, {res_name} = {res_name} + {lot[4]} WHERE user_id = {lot[1]}"
							)
					conn.commit( )
					curs.execute(f"UPDATE market SET access = 0 WHERE lot_id = {lot_id}")
					conn.commit( )
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message=f"Лот {lot_id} заблокирован."
							)
				else:
					self.vk.messages.send(
							peer_id=self.peer_id,
							random_id=random.randint(0, 10000000000),
							message=f"Лот {lot_id} еще не продан."
							)
			else:
				self.vk.messages.send(
						peer_id=self.peer_id,
						random_id=random.randint(0, 10000000000),
						message="ID лота должно состоять только из цифр."
						)
	
	def getProfile(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		curs.execute("SELECT race_id, exp, anders, nickname FROM users WHERE user_id = %s", (self.user_id,))
		prof = curs.fetchone( )
		curs.execute("SELECT name, photo_link FROM races WHERE race_id = %s", (prof[0],))
		race = curs.fetchone( )
		
		stats_pic = Image.open("profile.png")
		stats_pic_draw = ImageDraw.Draw(stats_pic)
		font = ImageFont.truetype("Aqum.ttf", size=20)
		
		stats_pic_draw.text(xy=(199, 45), text=race[0], fill="black", font=ImageFont.truetype("Aqum.ttf", size=25))
		stats_pic_draw.text(xy=(278, 128), text=str(prof[2]), fill="black", font=font)
		stats_pic_draw.text(xy=(294, 214), text=str(prof[2]), fill="black", font=font)
		stats_pic_draw.text(xy=(106, 403), text=prof[3].split(" ")[0], fill="black", font=font)
		stats_pic_draw.text(xy=(106, 544), text=prof[3].split(" ")[1], fill="black", font=font)
		stats_pic_draw.text(xy=(106, 685), text=str(self.user_id), fill="black", font=font)
		
		stats_pic.save('prof.png')
		
		vk_upload = vk_api.VkUpload(self.vk_session)
		photo = vk_upload.photo_messages(photos="prof.png", peer_id=self.peer_id)
		photo = f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}'
		self.vk.messages.send(
				peer_id=self.peer_id, random_id=random.randint(0, 10000000000), attachment=photo
				)
	
	def races(self):
		conn = pymysql.connect(
				host="remotemysql.com",
				user=self.user,
				password=self.passw,
				db='IMR5jUaWZE'
				)
		curs = conn.cursor( )
		curs.execute("SELECT name, adm, race_id FROM races")
		
		a = "\n\n"
		txt = a.join(f"ID: {i[2]}\nНазвание: {i[0]}\nАдмин: {i[1]}" for i in curs.fetchall( ))
		self.vk.messages.send(
				peer_id=self.peer_id,
				random_id=random.randint(0, 10000000000),
				message=txt
				)
	def addAdmin(self):
		pass
