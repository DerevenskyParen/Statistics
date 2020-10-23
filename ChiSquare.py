# Диденко, Швецова, Беляев
import math
import numpy as np
import csv
import scipy.stats as sps


class ChiSquareTest:
    def __init__(self, data):
        self.data = np.sort(np.array(data))

    def Check(self):
        if len(self.data) < 50:
            print('Проверка невозможна, слишком маленький размер выборки.')

    def Count(self):
        self.n = len(self.data)
        self.max = self.data[len(self.data) - 1]
        self.min = self.data[0]
        self.m = self.data.mean()  # мат ожидание
        self.sig = self.data.std()  # средне.квадарат.отклонение
        # расчет данных для создания интервалов
        self.d = self.max - self.min
        self.interval = round(1 + 3.22 * math.log(len(self.data)))
        self.step = self.d / self.interval

    def Test(self):
        # подсчет распределения СВ по итервалам
        self.bins = np.array(self.min)
        for i in np.arange(self.min + self.step, self.max, self.step):
            self.bins = np.append(self.bins, i)
        self.data, self.bins = np.histogram(self.data, bins=self.bins)

        # наблюдаемые значения
        self.f_ob = list(self.data)

        # вероятности попадания СВ в интервалы
        self.f_ex = np.array(sps.norm.cdf((self.bins[1] - self.m) / self.sig) - 0.5) - (sps.norm.cdf((self.bins[0] - self.m) / self.sig) - 0.5)
        for i in range(1, len(self.bins) - 1):
            self.f_ex = np.append(self.f_ex,
                             (sps.norm.cdf((self.bins[i + 1] - self.m) / self.sig) - 0.5) - (sps.norm.cdf((self.bins[i] - self.m) / self.sig) - 0.5))
        # ожидаемые значения
        self.f_ex = list([i * self.n for i in self.f_ex])

        # расчет критерия
        self.stats, self.p_value = sps.chisquare(self.f_ob, self.f_ex, ddof=len(self.bins) - 3)
    
    def Output(self):
        if self.p_value < 0.05:
            print('Гипотеза о соответствии нормальному закону распределения верна.')
        else:
            print('Гипотеза о соответствии нормальному закону распределения не может быть принята.')

testchi = ChiSquareTest(data)
testchi.Check()
testchi.Count()
testchi.Test()
testchi.Output()
