import csv # для работы с файлом
import math
import matplotlib.pyplot as plt # Для построения графика
import threading # Для создания новой нити исполнения

timeArray = [1,10,100,1000,10000,100000,110000,120000,2,20,200,2000,20000,3,30,300,3000,30000,4,40,400,4000,40000,5,50,500,5000,50000,60000,70000,80000,90000]
dotArray = [] # массив, в который будут записаны все точки
time = 0
threadPointers = []
for i in range(len(timeArray)):
    time += timeArray[i]
class DotClass: # класс точки, где time - календарное время, avr - среднее время обработки одного запроса, disp - дисперсия
    time = 0
    avr = 0
    disp = 0

# РАБОТА С ФАЙЛОМ:

with open('ms_bucket.csv') as csvfile:
    read = csv.reader(csvfile, delimiter = ',')
    next(read)
    for line in read:
        # функция работы со строкой файла
        def lineReader(line):
            a = DotClass()
            for i in range(len(line)):
                if i == 0:
                    a.time = int(line[0])
                if i > 1:
                    try:
                        a.avr += float(line[i])
                    except ValueError:
                        a.avr += 0.0
            try:
                a.avr = time/a.avr # серднее время выполнения
            except ZeroDivisionError:
                a.avr = 0
            for j in range(len(line)):
                if j > 1:
                    try:
                        a.disp += (timeArray[j-2]/float(line[j]) - a.avr)*(timeArray[j-2]/float(line[j]) - a.avr)
                    except ValueError:
                        a.disp += (a.avr)*(a.avr)
            a.disp = (1/(len(line)-2))*(a.disp) # дисперсия для i-ой точки
            dotArray.append(a)

        # В другой нити запускаю работу со строкой файла
        th = threading.Thread(target=lineReader, args=(line,))
        threadPointers.append(th)

        threadPointers[len(threadPointers) - 1].start()

# Жду завершения всех нитей
for j in range(len(threadPointers)):
    threadPointers[j].join()
    
    
# ПОСТРОЕНИЕ ГРАФИКА:

avr = [] # массив со средними значениями
dis = [] # массив с погрешностями
c_time = [] # массив календарного времени


for i in range(len(dotArray)):
    c_time.append(dotArray[i].time)
    avr.append(dotArray[i].avr)
    dis.append(dotArray[i].disp)
    
plt.figure()
plt.errorbar(c_time, avr, yerr=dis,xerr=None, ecolor='red')
plt.show()
