from kivy import Config
Config.set('graphics', 'minimum_width', '500')
Config.set('graphics', 'minimum_height', '175')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import Converter

Window.size = (500, 175)
Window.clearcolor = (242, 242, 242, 1)


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        # Creating main box, where functions are stored

        self.cols = 2
        self.row = 1


        # Creating all inside of first box
        # Creating First row

        self.main_box = GridLayout()
        self.main_box.cols = 1
        self.main_box.size_hint = (None, 1)
        self.main_box.row_force_default = True
        self.main_box.row_default_height = 30
        self.main_box.width = 250

        # Row 1
        self.row_1 = GridLayout(row_force_default=True, row_default_height=50)
        self.row_1.cols = 3
        self.row_1.rows = 1
        self.main_box.add_widget(self.row_1)

        # Row 2
        self.row_2 = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=50)

        self.row_2.add_widget(Label(text='Path: ', font_size=25, color=(0, 0, 0, 1)))

        # Row 2 for text and button

        self.row_2_additinoal = GridLayout(cols=2, rows=1, row_force_default=True, row_default_height=50, spacing=25)

        self.path = TextInput(multiline=False, size_hint=(None, None), width=300, height=40, font_size=25)
        self.path.bind(on_text_validate=self.Path_Submit_button)
        self.row_2_additinoal.add_widget(self.path)
        self.submit = Button(size_hint=(None, None), width=197, height=47, background_normal='apply.png', background_down='papply.png')
        self.submit.bind(on_press=self.Path_Submit_button)
        self.row_2_additinoal.add_widget(self.submit)
        self.row_2.add_widget(self.row_2_additinoal)
        self.main_box.add_widget(self.row_2)

        # Row 3
        self.row_3 = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=100)
        self.main_box.add_widget(self.row_3)

        # Row 4
        self.row_4 = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=50)

        self.row_4.add_widget(Label(text='Symbol: ', font_size=25, color=(0, 0, 0, 1)))

        # Row 4 for text and button

        self.row_4_additinoal = GridLayout(cols=2, rows=1, row_force_default=True, row_default_height=50, spacing=25)

        self.name_row_4 = TextInput(multiline=False, size_hint=(None, None), width=300, height=40, font_size=25)
        self.name_row_4.bind(on_text_validate=self.Submit_button)
        self.row_4_additinoal.add_widget(self.name_row_4)
        self.submit_row_4 = Button(size_hint=(None, None), width=198, height=47, background_normal='save.png', background_down='psave.png')
        self.submit_row_4.bind(on_press=self.Submit_button)
        self.row_4_additinoal.add_widget(self.submit_row_4)
        self.row_4.add_widget(self.row_4_additinoal)
        self.main_box.add_widget(self.row_4)

        # Row 5
        self.row_6 = GridLayout(cols=1, rows=1, row_force_default=True, row_default_height=100, width=500)
        self.main_box.add_widget(self.row_6)

        # Row 6
        self.row_5 = GridLayout(cols=5, rows=1, row_force_default=False, row_default_height=40, width=500, padding=25)

        # Setting default period for ATR calculation
        self.period = 1599778200

        # Adding all the toggle buttons and binding them functions with periods for calculating ATR

        self.submit_row_6 = ToggleButton(size_hint=(None, None), width=100, height=40, background_normal='img/c1.jpg', background_down='img/c1p.jpg', group='timeframe_toggler')
        self.submit_row_6.bind(on_press=self.first_toggle)

        self.row_5.add_widget(self.submit_row_6)

        self.submit_row_7 = ToggleButton(size_hint=(None, None), width=100, height=40, background_normal='img/c2.jpg', background_down='img/c2p.jpg', group='timeframe_toggler')
        self.submit_row_7.bind(on_press=self.second_toggle)

        self.row_5.add_widget(self.submit_row_7)

        self.submit_row_8 = ToggleButton(size_hint=(None, None), width=100, height=40, background_normal='img/c3.jpg', background_down='img/c3p.jpg', group='timeframe_toggler')
        self.submit_row_8.bind(on_press=self.third_toggle)

        self.row_5.add_widget(self.submit_row_8)

        self.submit_row_9 = ToggleButton(size_hint=(None, None), width=100, height=40, background_normal='img/c4.jpg', background_down='img/c4p.jpg', group='timeframe_toggler')
        self.submit_row_9.bind(on_press=self.fourth_toggle)

        self.row_5.add_widget(self.submit_row_9)

        # Row 5 for text and button
        self.main_box.add_widget(self.row_5)

        # Adding main box 1

        self.add_widget(self.main_box)

    def Path_Submit_button(self, instance):
        self.path_dir = self.path.text

    def Submit_button(self, instance):
        name = self.name_row_4.text
        if Converter.TableConverter(self.period).Table_maker(name,self.path_dir) == 'try again':
            self.name_row_4.text = ''
            PopupError().build()

        elif Converter.TableConverter(self.period).Table_maker(name,self.path_dir) == 'wrong path name':
            self.name_row_4.text = ''
            PopupError_1().build()


        else:
            Converter.TableConverter(self.period).Table_maker(name, self.path_dir)
            Converter.Pivot_Maker().Pivot_maker(name, self.path_dir)
            self.name_row_4.text = ''
    def first_toggle(self, instance):
        self.period = 1599778200

    def second_toggle(self, instance):
        self.period = 1594421400

    def third_toggle(self, instance):
        self.period = 1586386200

    def fourth_toggle(self, instance):
        self.period = 1570834200
class PopupError(App):
    def build(self):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text='No tables found!\n Please check if you typed ticker correclty and try again',
                             size_hint=(1, None), height=100, halign='center', valign='center'))
        popup = Popup(title='Error', title_size=(25),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(750, 300),
                      auto_dismiss=True)
        box.add_widget(Button(text='OK', on_press=popup.dismiss))
        popup.open()
class PopupError_1(App):
    def build(self):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text='Wrong path name!\n Please check if you added "/" in the end and try again',
                             size_hint=(1, None), height=100, halign='center', valign='center'))
        popup = Popup(title='Error', title_size=(25),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(750, 300),
                      auto_dismiss=True)
        box.add_widget(Button(text='OK', on_press=popup.dismiss))
        popup.open()

class PopupSuccess(App):
    def build(self):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text='Table was successfully converted!'))
        popup = Popup(title='Table converted', title_size=(30),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(750, 300),
                      auto_dismiss=True)
        box.add_widget(Button(text='OK', on_press=popup.dismiss))
        popup.open()



class ConverterApp(App):
    def build(self):
        return MyGrid()


if __name__ == '__main__':
    ConverterApp().run()