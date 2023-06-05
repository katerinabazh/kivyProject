import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('mainfile.kv')

class MyGridLayout(Widget):

    #name_list_input = ObjectProperty(None)
    #finished_text = ObjectProperty(None)
    
    prec_num = 0

    
    
    def press(self):
        need_of_number_multiplication = self.ids.multiplication.active
        GELECkeck = self.ids.GELEcheck.active
        name_list_input = self.ids.name_list_input.text
        prec = int(self.ids.prec_num.text)
        code_of_scenario = int(self.ids.code_of_scenario.text)
        count_of_numbers = int(self.ids.count_of_numbers.text)

        if name_list_input == '':
            outprint = name_list_input     #'Не введен входной параметр'
        else:
            name_list = self.cur_name_list(name_list_input)
            if not name_list_input :
                outprint = 'Список не создан'
            else:
                outprint = 'Данные имен созданы и находятся в\n D:\PyTHoN\kivygui\shablonizatorhelper\\test.txt'

                finished_code = ''
                save_list_names_for_diff = []

                if count_of_numbers == 0:
                    outprint = 'Ошибка: отсутствуют значения'
                #здесь должна быть запись о полном завершении подпрограммы
                elif count_of_numbers == 1:
                    test_number = '0'
                    test_plus_one = ''
                else:
                    test_number = 'test'
                    test_plus_one = '\VAR{test + 1}'

                for i in range(len(name_list)):
                    #возврат сокрашенного имени функции(без limits или exists)
                    name, exists_or_limits = self.return_names_from_name_list(name_list[i])
                    if exists_or_limits == 'l':
                        #если нужен другой prec
                        prec_number = self.check_prec(prec)
                        #Смотрим нужно ли прописывать строку домножения
                        string_number_multiplication = self.return_string_of_num_multiplication(need_of_number_multiplication)
                        #создание кода с 3мя строками: основное значение, диапазон и статус
                        value_string_name, text_limits_string_name, status_string_name, code = self.main_code(name, name_list[i], test_number, prec_number, string_number_multiplication, GELECkeck)
                        
                        if code_of_scenario == 1:
                            lable_definition = self.easy_code(test_plus_one, value_string_name, text_limits_string_name, status_string_name) + '\n'
                        elif code_of_scenario == 2:
                            save_list_names_for_diff.append(name_list[i])

                        elif len(save_list_names_for_diff) == 2:
                            didderence_string_name, compare_two_statuses_name, code_two_strings =  self.second_scenario_add_code(save_list_names_for_diff, test_number, string_number_multiplication)
                            #table = table_string_16test()
                            lable_definition = code_two_strings + '\n' + '\n'
                            save_list_names_for_diff.clear()
                        else:
                            lable_definition = ''


                        #lable_definition = define_columns(value_string_name, text_limits_string_name, status_string_name, code_of_scenario, test_number)
                        finished_code += code + lable_definition 

                    elif exists_or_limits == 'e':
                        term_string =  test_plus_one + ' & ---- & --- &  \VAR{h.add_background_color(' + name_list[i] + '[' + test_number +']' + ')} \\tabularnewline \hline'
                        finished_code += term_string + '\n'*2
                    else:
                        print('unknown name list')
                        break
                f = open(r'D:\PyTHoN\kivygui\shablonizatorhelper\test.txt', 'w')
                f.write(str( finished_code))
                f.close() 
            self.ids.finished_text.text =  f'{outprint}'
            
        #self.name_list_input.text = ''

    def cur_name_list(self, name_list_input):
        """
        Обрезка имен списка
        """
        name_list = []
        #символы, которые удалятся из списка
        deleting_objects = ['%%', 'set', '=', ' ', '\t', '\n']
        name_list = name_list_input.split('[]')
        #строка-удаление пустого элемента из списка
        name_list = list(filter(None, name_list))
        for i in range(len(name_list)):
            for j in range(len(deleting_objects)):
                name_list[i] =  name_list[i].replace(deleting_objects[j], '')
        
        return name_list
    
    def take_nums(self, name = 'diff_voltage_IAE1_and_AE1_limits', amount_nesessery_num = 1):
        """
        забирает все числа из имени 
        param: name - имя  в котором будет происходиться поиск
        param: amount_nesessery_num - количество чисел, что надо забрать из имени
        return: 2 первых числа
        """
        
        two_nums = []
        for s in name:
            if s.isdigit():
                two_nums.append(s)

        return two_nums
        
    def return_string_of_num_multiplication(self, need_of_number_multiplication = False):
        """
        Проверяет нужен ли перевод в в милли (мВ/мс/мА). При успехе веврнет строку, которая будет вставляться в код. Если домножение не нужно - вернет пустоту
        param: need_of_number_multiplication - bool значение, по которому определится необходимость(или ее отсутствие) в домолнительной строке в коде
        return: строка, которая будет вставляться для домножения

        """
        # проверим- если надо, то будем писать. При ненадобности перевода в милли - запишем ничего
        if need_of_number_multiplication:
            string_number_multiplication = ', number_multiplication = 1000'
        else:
            string_number_multiplication = ''
        return string_number_multiplication
     
    def check_prec(self, prec_num = 0): #нуждается в предусмотрении prec отрицательного
        """
        Функция check_prec - выбирает что будет вставляться в prec
        """
        if prec_num == 0:
            prec = ''
        else:
            prec = str(prec_num)
        return prec

    def first_column_entry(self, name = 'diff_voltage_IAE1_and_AE1_limits', scenario = 1, amount_of_num = 0):
        list_num = take_nums(name, amount_of_num)
        if scenario == 451:
            #строка теста 4 для табл5 
            text_str = 'Разница напряжений на ИАЭ' + list_num[0] + ' и АЭ' +  list_num[1] +' (мВ)'
        elif scenario == 450:
            text_str =  'Разница напряжений АБ' + list_num[0] +' и суммой по 4м выходам АЭ' + list_num[0] +' (мВ)'
        elif scenario == 1610:
            text_str = 'Разница напряжений на линии питания ДД и БУФ'
        return text_str

    def easy_code(self, test_plus_one = '', value_string_name = 'name', text_limits_string_name = 'text_limits_name', status_string_name = 'status_name'):
        #эт0 часть кода с генерацией строки вывода
        

        output = test_plus_one + ' & \VAR{' + value_string_name + '} & \VAR{' + text_limits_string_name + '} & \VAR{' + status_string_name + '} ' + '\\tabularnewline \hline'

        #text_str = first_column_entry(name_list[i], scenario, 1)

        #finished_code += value_string + '\n'  + text_limits_string + '\n' + status_string + '\n' + output + '\n' + '\n'
        return output

    def return_names_from_name_list(self, name):
        if not name: # при передаче пустого списка пропечатает ошибку
            print('Ошибка: передача пустого списка')
            return None
        else:
            if name.find('limits') != -1: #если нашел limits
                return name[:name.find('limits') - 1] +  name[ name.find('limits') + 6: ], 'l' #вырез этого слова
            elif name.find('exists') != -1:
                return name[:name.find('exists') - 1] +  name[ name.find('exists') + 6: ], 'e'

    def main_code(self, name, name_from_list, test_number, prec_number, string_number_multiplication, GELECkeck):
        """
        Функция создает основной код: 3 строки, которые будут вытаскивать значения из списка словарей в программе Latex
        param: name - имя, вырезанное из name_from_list в основной программе. На его основе строятся переменные
        param: name_from_list - имя списка программы LaTeX. В данной проге(не функции) - из списка с названиями списков LaTeX
        param: test_number - номер, по которому в конечном коде LaTeX будут отсчитываться элементы списка. Здесь, при 1 словаре в списке будет стоять 0, иначе - test (как будущий инкремент)
        param: prec_number - будущий номер округления. Указывается в самом начале программы и является входным значением для создания кода
        param:string_number_multiplication - будущий номер домножения(перевод в милли, например). Указывается в самом начале программы и является входным значением для создания кода

        return: 3 имени и конечныее 3 строки кода для LaTeX


        """
        finished_code = '\n'
        #Отсюда начинается основлная программа
        #имя основного значения
        value_string_name = name
        value_string = '%% set ' + value_string_name + ' = h.formatting_float_number(' + name_from_list + '[' + test_number +']' + "[0]['result'], precision = prec" + prec_number + string_number_multiplication +')'

        upper_bound = 'h.exist_result(h.exist_limits(' + name_from_list + '[' + test_number +']' + "[0], 'hi', prec" + prec_number + string_number_multiplication + '), precision = prec' + prec_number + ')'
        lower_bound = 'h.exist_result(h.exist_limits(' + name_from_list + '[' + test_number +']' + "[0], 'lo', prec" + prec_number + string_number_multiplication + '), precision = prec' + prec_number + ')'
        comp_sign = 'h.exist_result(h.exist_limits(' + name_from_list + '[' + test_number +']' + "[0], 'comp'))"

        # имя диапазона значений
        text_limits_string_name = 'text_limits_' + name

        if GELECkeck == True:
            text_limits_string =  '%% set ' + text_limits_string_name + ' = ' + lower_bound + ' + ' + comp_sign + ' + ' + upper_bound
        else:
            text_limits_string =  '%% set '+ text_limits_string_name + ' = ' + comp_sign + ' + ' + lower_bound

        # имя статуса
        status_string_name =  name + '_status'

        status_string =  '%% set ' + status_string_name + ' = h.add_background_color(h.exist_result(' + name_from_list + '[' + test_number +']' + "[0]['status']))"

        finished_code += value_string + '\n'  + text_limits_string + '\n' + status_string + '\n' + '\n' 
        return value_string_name, text_limits_string_name, status_string_name, finished_code

    #@title 
    def second_scenario_add_code(self, list_of_2_names, test_number = '0', string_number_multiplication = ''):
        """
        Функция second_scenario_add_code: возвращает 2 дополнительные строки
        """
        inner_list_of_names = []
        for name in list_of_2_names:
            inner_list_of_names.append(return_names_from_name_list(name))
        # строка с разницей результатов
        didderence_string_name = 'diff_' + inner_list_of_names[0] + '_and_' + inner_list_of_names[1]
        didderence_string = '%% set ' + didderence_string_name + ' =  h.formatting_float_number((' + list_of_2_names[0] + '[' + test_number + "][0]['result']|float - " + list_of_2_names[1] + '[' + test_number + "][0]['result']|float)|abs, precision = prec"+ prec_number + string_number_multiplication +')'
        # строка сравнения статусов
        compare_two_statuses_name = 'general_status_' + inner_list_of_names[0] + '_and_' + inner_list_of_names[1]
        compare_two_statuses = '%% if ' + list_of_2_names[0] + '[' + test_number + "][0]['status'] != ' ' or " + list_of_2_names[1] + '[' + test_number + "][0]['status'] != ' '" + '\n'
        compare_two_statuses += '%% set ' + compare_two_statuses_name + " = h.add_background_color(h.exist_result('Failed'))" + '\n'
        compare_two_statuses += '%% endif'

        finished_string = didderence_string + '\n' + compare_two_statuses
        return didderence_string_name, compare_two_statuses_name, finished_string




class ThiseApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    ThiseApp().run()
