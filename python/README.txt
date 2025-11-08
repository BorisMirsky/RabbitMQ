Завести виртуальное окружение. 
Запустить сервер Fast API завести: 'uvicorn main:app --reload'      зачем это тут?

Запуск idle из под виртуального окружения 
- завести в окружение
- в терминале 'python -m idlelib.idle'    





1. Вручную через GUI
https://babok-school.ru/blog/rabbitmq-for-analyst/
HelloWorld/



2. Код
https://babok-school.ru/blog/how-to-write-producer-and-consumer-for-rabbitmq-in-colab/
Sensors/
Делал по гайду, у Обменника не создались Features (в след-м пункте создались).



3. Неправильно заданные параметры  => обработка, запись в (1) ok-file  (2) error-file 
https://babok-school.ru/blog/alternative-exchanges-and-queues-in-rabbitmq/
ProcessErrors/
3.1 В гайде по ссылке ошибка - нет привязки.
3.2 Пишет только ошибки - в консоль и в error-file.
        Error: TextIOWrapper.write() takes no keyword arguments, 
            Value: {'producer_publish_time': '11/07/2025 18:08:52', 
            'content': 'ВСЕ НОРМАЛЬНО, произошло событие номер 416'}
    Но это не ошибка
3.3 Пишет всё двоичном виде.



