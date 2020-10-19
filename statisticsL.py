#Задание: Обработчик выборки 
#Выполнили: Шишков Л., Язданов Р., Аполлова А.

from openpyxl import load_workbook, Workbook
import statistics

class StatisticsL():                                #класс рачёта числовых характеристик
    def dlinaV(name):                               #метод расчёта длины выборки                         
        dlina = len(name)
        return('Длина выборки', dlina)
    def sredneeV(name):                             #метод расчёта среднего значения выборки       
        srednee = statistics.mean(name)
        return("Среднее значение выборки", srednee)
    def dispersiaV(name):                           #метод расчёта дисперсии выборки
        dispersia = statistics.variance(name)
        return("Дисперсия выборки", dispersia)
    def skoV(name):                                 #метод расчёта СКО выборки        
        sko = statistics.stdev(name)
        return("СКО выборки", sko)
    def modaV(name):                                 #метод расчёта моды выборки       
        try:                                        
            moda = statistics.mode(name)
        except:
            moda = "-"
        return("Мода выборки", moda)
    def medianaV(name):                             #метод расчёта медианы выборки        
        mediana = statistics.median(name)
        return("Медиана выборки", mediana)
    def sortV(name):                                #метод сортировки выборки
        sort = sorted(name)
        return("Отсортированная выборка", sort)
               
#ПРОВЕРКА
wb = load_workbook(str(input('Введите название файла ')))   #Открытие выборки
sheet = wb.get_sheet_by_name('Лист1')
temp = []
temp2 = []
for row in sheet.rows:
	if type(row[0].value)!=str:
		temp.append(float(row[0].value))
		temp2.append(float(row[1].value))

re = 1
while re<=8:
	re = int(input("""Действие:
	1. Длина выборки
	2. Среднее значение выборки
	3. Дисперсия выборки
	4. СКО выборки
    5. Мода выборки
    6. Медиана выборки
    7. Отсортированная выборка
	8. Выход
	Выбор: """))
	if re==1:
		A = StatisticsL.dlinaV(temp)
		print(A)
	if re==2:
		A = StatisticsL.sredneeV(temp)
		print(A)
	if re==3:
		A = StatisticsL.dispersiaV(temp)										
		print(A)
	if re==4:
		A = StatisticsL.skoV(temp)
		print(A)
	if re==5:
		A = StatisticsL.modaV(temp)
		print(A)       
	if re==6:
		A = StatisticsL.medianaV(temp)
		print(A) 
	if re==7:
		A = StatisticsL.sortV(temp)
		print(A)          

