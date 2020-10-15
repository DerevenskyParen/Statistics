"""
	Модуль гистограммы
	Выполнено студентами ПИ-Б19-1 Быков Данила и Кашин Никита
"""
#Импорты необходимых библиотек
#from random import randrange - использовалось для создания импровизированной выборки
import math
import seaborn as sns
import matplotlib.pyplot as plt


class Histogram:
	"""Графическое отображение:
	- Графика плотности распределения
	- Гистограммы
	"""
	#Конструктор
	def __init__(self, table):
		self.table = table
	#Метод отрисовки графиков
	def DrawGraphs(self):
		"""Вычисление количества интервалов"""
		intervalCount = round(1 + 3.22 * math.log(len(self.table)))

		"""Создание гистограммы"""
		plt.subplot(1,2,1)
		n, bins, patches = plt.hist(self.table, intervalCount, facecolor='red', alpha=0.5, edgecolor='black')
		plt.title("Гистограмма")
		plt.ylabel("Количество значений")
		plt.xlabel("Значения")
		"""Создание графика плотности"""
		plt.subplot(1,2,2)
		sns.distplot(self.table, hist=True, kde=True, bins=intervalCount, color='darkblue', hist_kws={'edgecolor':'black'}, kde_kws={'linewidth':4})
		plt.title("График плотности")
		plt.ylabel("Частота")
		plt.xlabel("Значения")
		"""Отображение графиков"""
		plt.show()
		pass
