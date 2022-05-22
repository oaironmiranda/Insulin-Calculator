from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
from datetime import datetime
import mysql.connector

class MainApp(MDApp):

	# database connection function
	def connector(self, command, value):
		conn = mysql.connector.connect(
			host='b6uvkfjwjuqi6ckzxz5s-mysql.services.clever-cloud.com',
			database='b6uvkfjwjuqi6ckzxz5s',
			user='uczx3ztt4o1jmssx',
			password='J57IrbhnsqCGnReZdnHx',
			port='3306')

		c = conn.cursor()
		c.execute(command, value)
		conn.commit()
		conn.close()

	# time function
	def time(self):
		data = datetime.strftime(datetime.today(), "%d/%m/%y")
		hora = datetime.strftime(datetime.now(), "%H:%M")

	# app builder function
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "DeepPurple"

		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "DeepPurple"

		return Builder.load_file('main.kv')

	# calculation function
	def calc(self):
		if str(self.root.ids.num.text) == '':
			self.root.ids.label.text = "TRY AGAIN"
		else:
			a = int(self.root.ids.num.text)
			if a < 190:
				self.root.ids.label.text = "YOU DON'T NEED TO FIX YOUR BLOOD SUGAR"
				if a <= 85:
					self.root.ids.label.text = "YOU NEED TO FIX YOUR BLOOD SUGAR"
			elif a >= 190:
				b = (a - 120) / 70
				self.root.ids.label.text = f"ADD {round(b)} UI"

		command = "INSERT INTO glic (dia, hora, glicemia) VALUES (%s, %s, %s)"
		value = (f"{self.time.data()}", f"{self.time.hora()}", int(self.root.ids.num.text),)

		self.connector(command, value)

		self.on_start()

	# database show function
	def on_start(self):
		command = "SELECT * FROM glic WHERE dia = %s ORDER BY id DESC"
		value = (f{self.time.data()})
		c = self.connector(command, value)

		records = c.fetchall()

		for record in records:
			self.root.ids.container.add_widget(
				ThreeLineListItem(text=f"{record[3]}", secondary_text=f"{record[1]}", tertiary_text=f"{record[2]}")
			)

MainApp().run()
