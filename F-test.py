import numpy

class readtestF:
   #класс принимает (название_файла.txt, степнь свободы выборки(по умолчанию = 1))
    
    def __init__(self, name = None, freedom = 1):
        self.name = name
        self.file = open(self.name)
        self.readen = self.file.readlines()
        self.freedom = freedom
        for i in range(len(self.readen)):
            self.readen[i] = self.readen[i].rstrip()
            self.readen[i] = self.readen[i].split(',')
            self.readen[i] = '.'.join(self.readen[i])
            self.readen[i] = float(self.readen[i])
    
    def Dispersion(self):
        # Метод вычисляет дисперсию выборки
        return numpy.var(self.readen, ddof = self.freedom)

class Ftest:
    # Класс принимает список из двух элементов
    def __init__(self, dispersions = None):
        self.dispersions = dispersions
    
    def ReturnF(self):
        #Метод считает экспериментальную величину Фишера(относительная).
        if self.dispersions[0] > self.dispersions[1]:
            return self.dispersions[0]/self.dispersions[1]
        else:
            return self.dispersions[1]/self.dispersions[0]

#Например можно вычислить критерий Фишера так:
file1 = readtestF('Vyborka1.txt').Dispersion()
file2 = readtestF('Vyborka2.txt').Dispersion() 
#file1 и file2 содержат дисперсии каждой выборки
print(file1)
print(file2)
#убедились, что это так. Наши переменные содержат некоторое число(Дисперсию выборки)
List = [file1, file2]
result = Ftest(List)
print(result.ReturnF())





