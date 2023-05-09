from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivymd.app import MDApp
from math import factorial

Window.size = (400, 400)

class Container(GridLayout):
    func = None   # текущая функция
    func_flag = False # флаг нужен, чтобы ввод значений и операций не сваливались в кучу
    save = False # для смены операции в процессе вычисления
    num = 0 # текущий буфер

    def zeros(self):
        if self.func_flag == True:
            self.text_inp.text = ''
        if self.text_inp.text == '0':
            pass
        else:
            self.text_inp.text += '0'
        self.func_flag = False

    # Для ввода цифр (кроме нуля)
    def figures(self, number):
        if self.func_flag == True:
            self.text_inp.text = ''
        if self.text_inp.text == '0':
            self.text_inp.text = number
        else:
            self.text_inp.text += number
        self.func_flag = False

    def ones(self):
        self.figures('1')

    def twos(self):
        self.figures('2')

    def threes(self):
        self.figures('3')

    def fours(self):
        self.figures('4')

    def fives(self):
        self.figures('5')

    def sixs(self):
        self.figures('6')

    def sevens(self):
        self.figures('7')

    def eights(self):
        self.figures('8')

    def nines(self):
        self.figures('9')

    # Функцию для ввода точки тоже прописал отдельно
    def points(self):
        if self.func_flag == True:
            self.text_inp.text = ''
        if not self.text_inp.text:
            self.text_inp.text = '0.'
        elif '.' not in self.text_inp.text:
            self.text_inp.text += '.'
        self.func_flag = False

    # Для AC
    def clear(self):
        self.num = 0
        self.text_inp.text = ''
        self.func_flag = False
        self.func = None
        self.save = False

    # Коллекция применяемых функций вынес специально вниз, а не с остальными атрибутами класса,
    # т.к. удобнее смотреть рядом с методами
    functions = {'+': 'if not self.func_flag: self.num += float(self.text_inp.text)',
                 '-': 'if not self.func_flag: self.num -= float(self.text_inp.text)',
                 '*': 'if not self.func_flag: self.num *= float(self.text_inp.text)',
                 '/': '''if not self.func_flag: 
                             try: 
                                 self.num /= float(self.text_inp.text) 
                             except: 
                                 self.num = "Ошибка"''',
                 'pows': 'if not self.func_flag: self.num = self.num ** float(self.text_inp.text)',
                 'sqrs': 'if not self.func_flag: self.num = self.num ** (1 / float(self.text_inp.text))',
                 'facts': '''if not self.func_flag:
                                 try:
                                    if int(float(self.num)) == float(self.num):
                                        res = int(float(self.num))
                                        if res <= 20: 
                                            self.num = factorial(res)
                                        else:
                                            self.num = "Ошибка"
                                    else:
                                        self.num = "Ошибка"
                                 except:
                                    self.num = "Ошибка"''',
                 'pers': 'if not self.func_flag: self.num = self.num % float(self.text_inp.text)',
                 '=': 'self.text_inp.text = str(self.num)'}

    # Функция для вычисления промежуточных результатов при последовательных вычислениях
    def result(self):
        exec(self.functions.get(self.func, 'None'))
        exec(self.functions['='])
        self.func = None
        self.func_flag = True

    # Для итогового результата (нажатие кнопки '=')
    def res_fin(self):
        self.result()
        self.save = False

    # Каркас для операций (для всех, кроме факториала)
    def operation(self, zn):
        if self.func != zn:
            if not self.save:
                if self.text_inp.text:
                    self.num = float(self.text_inp.text)
                else:
                    self.text_inp.text = '0'
                self.save = True
            self.result()
            self.func = zn
        exec(self.functions.get(self.func, 'None'))
        exec(self.functions['='])
        self.func_flag = True

    def adds(self):
        self.operation('+')

    def subs(self):
        self.operation('-')

    def muls(self):
        self.operation('*')

    def divs(self):
        self.operation('/')

    def pows(self):
        self.operation('pows')

    def sqrs(self):
        self.operation('sqrs')

    def pers(self):
        self.operation('pers')

# Факториал (ограничил его аргументом не более 20)
    def facts(self):
        if self.func != 'facts':
            if not self.save:
                if self.text_inp.text:
                    self.num = float(self.text_inp.text)
                else:
                    self.num = '0'
                self.save = True
            exec(self.functions.get(self.func, 'None'))
            exec(self.functions['='])
        self.func_flag = False
        self.num = self.text_inp.text
        self.func = 'facts'
        exec(self.functions.get(self.func, 'None'))
        exec(self.functions['='])
        self.func_flag = True


class Calculate(MDApp):
    def __init__(self, **kwargs):
        self.title = 'Калькуляторище'
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        return Container()

if __name__ == '__main__':
    Calculate().run()


