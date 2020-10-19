#выполнили модуль:Бабкин Гусаков Емельянов 
#Расчет коэффициентов парной линейной регрессии

# coding: utf-8

# In[3]:


import numpy as np 
import matplotlib.pyplot as plt

def estimate_coefficients(x, y): 
    # размер набора данных ИЛИ количество наблюдений / точек
    n = np.size(x) 
  
    # среднее значение x и y
	# Поскольку мы используем numpy, достаточно просто вызвать mean для numpy
    mean_x, mean_y = np.mean(x), np.mean(y) 
  
    # вычисление перекрестного отклонения и отклонения около x 
    SS_xy = np.sum(y*x - n*mean_y*mean_x) 
    SS_xx = np.sum(x*x - n*mean_x*mean_x) 
  
    # вычисление коэффициентов регрессии
    b_1 = SS_xy / SS_xx 
    b_0 = mean_y - b_1*mean_x 
  
    return(b_0, b_1)

    # x, y - расположение точек на графике

def plot_regression_line(x, y, b): 
    # нанесение точек в соответствии с набором данных на график
    plt.scatter(x, y, color = "m",marker = "o", s = 30) 

    # предсказанный вектор ответа
    y_pred = b[0] + b[1]*x 
  
    # построение линии регрессии
    plt.plot(x, y_pred, color = "g")
  
    # размещение меток для осей x и y
    plt.xlabel('argument') 
    plt.ylabel('function') 
  
    # функция для отображения построенного графика
    plt.show()
    

    


def main(): 
    # Наборы данных, которые мы создаем 
    x = np.array([ 1,   2,   3,   4,   5,   6,   7,   8,    9,   10]) 
    y = np.array([300, 350, 500, 700, 800, 850, 900, 900, 1000, 1200]) 
  
    # оценочные коэффициенты 
    b = estimate_coefficients(x, y) 
    print("Estimated coefficients:\nb_0 = {} \nb_1 = {}".format(b[0], b[1])) 
  
    # построение линии регрессии 
    plot_regression_line(x, y, b)

    
if __name__ == "__main__": 
    main()

