import matplotlib.pyplot as plt
import numpy as np
from random import random, randint


def readData(file):
    Data = []
    with open(file, 'r') as f:
        Keys = list(map(str, f.readline().rstrip().split(',')))
        while True:
            Input = f.readline().rstrip()
            if Input == '':
                break
            line = list(map(str, Input.split(',')))
            for i in range(len(line)):
                if line[i].isdigit():
                    line[i] = float(line[i])
            dct = {Keys[i]: line[i] for i in range(len(Keys))}
            Data.append(dct)
    return Data, Keys
            

def chooseCategory(Data, categories = None, condition = lambda: True):
    if categories is None:
        categories = Keys
    Array = [[] for i in range(len(categories))]
    for line in Data:
        if condition(line):
            if categories is not None:
                for i in range(len(categories)):
                    Array[i].append(line[categories[i]])
            else:
                Array.append(line)
    return Array


def visCountry(countryName, active = False):
    A = chooseCategory(Data, categories = ['Confirmed', 'Recovered', 'Deaths'],
                       condition = lambda line: (line['Country/Region'] == countryName
                                                 and line['Province/State'] == ''))
    B = [A[0][i] - A[1][i] - A[2][i] for i in range(len(A[0]))]

    if active:
        plt.plot(B, color='blue', antialiased=True)

    plt.plot(A[0], color='red', antialiased=True)
    plt.plot(A[1], color='green', antialiased=True)
    plt.plot(A[2], color='black', antialiased=True)

    plt.show()


def getColor(i):
    GoodColors = [(0.7, 0, 0), (0, 0.7, 0), (0, 0, 0.7), (0.2, 0.2, 0.2),
                  (0.7, 0.7, 0), (0, 0.7, 0.7)]
    for j in range(i):
        if len(GoodColors) > 0:
            yield GoodColors.pop(randint(0, len(GoodColors) - 1))
        else:
            yield (random(), random(), random())


def Smoothing(A, rate):
    Res = []
    Q = []
    for val in A:
        Q.append(val)
        if len(Q) > rate:
            Q.pop(0)
        Res.append(int(sum(Q) / len(Q)))
    return Res

    
def compareCountries(countries, parameters, perDay = False,
                     smooth = False, smoothRate = 7):
    '''
    example:
    compareCountries(['Germany', 'Italy', 'France', 'Spain'],
                     ['Confirmed','Recovered','Deaths', 'Active'])
    '''
    differ = 3
    IllColorRange = [(i / 255, 0, 0) for i in range(255, 255 // 2, -(255 // 2) //
                                              len(countries) + 1)]
    RecColorRange = [(0, i / 255, 0) for i in range(255, 255 // 2, -(255 // 2) //
                                              len(countries) + 1)]
    ActColorRange = [(0, 0, i / 255) for i in range(255, 255 // 2, -(255 // 2) //
                                              len(countries) + 1)]
    DieColorRange = [(i / 255, i / 255, i / 255)
                     for i in range(0, 255 // 2, (255 // 2) //
                                    len(countries) + 1)]
    ColorGen = getColor(len(countries) * len(parameters))
    Colors = [i for i in ColorGen]
    for country in countries:
        for parameter in parameters:
            req = [parameter]
            if parameter == 'Active':
                req = ['Confirmed', 'Recovered', 'Deaths']
            A = chooseCategory(Data, categories = req,
                       condition = lambda line: (line['Country/Region'] == country
                                                 and line['Province/State'] == ''))

            if parameter == 'Active':
                A = [[A[0][i] - A[1][i] - A[2][i] for i in range(len(A[0]))]]
            if len(parameters) == 1:
                color = Colors.pop()
            elif parameter == 'Confirmed':
                color = IllColorRange.pop(0)
            elif parameter == 'Recovered':
                color = RecColorRange.pop(0)
            elif parameter == 'Deaths':
                color = DieColorRange.pop(0)
            elif parameter == 'Active':
                color = ActColorRange.pop(0)
            else:
                color = Colors.pop()
                
            text = country + ' ' + parameter
            if perDay:
                A[0] = np.diff(A[0])

            if smooth:
                A[0] = Smoothing(A[0], smoothRate)
                
            plt.plot(A[0], color=color, antialiased=True, label = text)
    plt.grid()       
    plt.legend()
    plt.show()



if __name__ == '__main__':
    Data, Keys = readData(r'covid.txt')
    compareCountries(['Russia', 'Brazil'],
                     ['Active'], perDay = False, smooth = False)

