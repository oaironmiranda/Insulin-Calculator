from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
from datetime import datetime
import mysql.connector



class MainApp(MDApp):
    def build(self):
        # I hide my informations just for safe reasons
        conn = mysql.connector.connect(
            host='b6uvkfjwjuqi6ckzxz5s-mysql.services.clever-cloud.com',
            database='b6uvkfjwjuqi6ckzxz5s',
            user='uczx3ztt4o1jmssx',
            password='J57IrbhnsqCGnReZdnHx',
            port='3306'
        )

        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists glic (
            dia text,
            hora text,
            glicemia integer);
            """)
        conn.commit()
        conn.close()

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_file('main.kv')

    def calc(self):
        if str(self.root.ids.num.text) == '':
            self.root.ids.label.text = "Try Again"
        else:
            a = int(self.root.ids.num.text)
            if a < 190:
                self.root.ids.label.text = "You don't need to Add more insuline"
                if a <= 85:
                    self.root.ids.label.text = "You need to fix your blood sugar"
            elif a >= 190:
                b = (a - 120) / 70
                self.root.ids.label.text = f'Add {round(b)}UI'

        conn = mysql.connector.connect(
            host='b6uvkfjwjuqi6ckzxz5s-mysql.services.clever-cloud.com',
            database='b6uvkfjwjuqi6ckzxz5s',
            user='uczx3ztt4o1jmssx',
            password='J57IrbhnsqCGnReZdnHx',
            port='3306'
        )

        data = datetime.strftime(datetime.today(), "%d/%m/%y")
        hora = datetime.strftime(datetime.now(), "%H:%M")

        # create a cursor
        c = conn.cursor()
        sql_command = "INSERT INTO glic (dia, hora, glicemia) VALUES (%s, %s, %s)"
        values = (f"{data}", f"{hora}", int(self.root.ids.num.text),)

        # Add a record
        c.execute(sql_command, values)

        # commit the changes
        conn.commit()

        # close or conection
        conn.close()

    def navigation_draw(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        elif self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"

    def on_start(self):
        conn = mysql.connector.connect(
            host='b6uvkfjwjuqi6ckzxz5s-mysql.services.clever-cloud.com',
            database='b6uvkfjwjuqi6ckzxz5s',
            user='uczx3ztt4o1jmssx',
            password='J57IrbhnsqCGnReZdnHx',
            port='3306'
        )
        c = conn.cursor()

        data = datetime.strftime(datetime.today(), "%d/%m/%y")

        sql_command = "SELECT  * FROM glic WHERE dia = %s ORDER BY id DESC"
        values = (f"{data}",)

        c.execute(sql_command, values)
        records = c.fetchall()

        for record in records:
            self.root.ids.container.add_widget(
                ThreeLineListItem(text=f"{record[3]}", secondary_text=f"{record[1]}", tertiary_text=f"{record[2]}")
            )

        conn.commit()
        conn.close()


MainApp().run()
