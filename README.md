## Heliflex (Arduino + Raspberry)
#### Программа предназначена для контроля работы линии по производству шлангов. Аппаратная часть реализована с использованием Raspberry, Arduino Unо, инкрементального кругового энкодера и двух датчиков приближения. Микроконтроллер Arduino с помощью датчиков определяет скорость вращения двух барабанов с нитками, скорость намотки шланга и количество намотаного на бобину шланга. На Raspberry, на Pythonе реализован графический интерфейс пользователя и серверная часть. Взаимодействие Arduino и Raspberry организовано с использованием usb-порта. Программа сохраняет полученные от микроконтроллера и расчитанные значения в локальной базе данных MariaDB. Это позволяет получить доступ к текущим параметрам работы линии с удаленного компьютера.  
