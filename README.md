Это итоговый проект семестра 1 курса DLS.
Модель позаимствована у СБЕР АИ https://github.com/ai-forever/Real-ESRGAN
они не возражают, но за пследствия ответственности не несут


Бот асинхронный, реализован в 3 сущностях, не считая модели: 
- поллер [main.py](main.py), реализован на aiogram, слушает телеграм и, если получает картинку - сохраняет ее в  папку, при этом добавляет к имени файла chat_id и message_id. 
- улучшатель [resolutor.py](resolutor.py) - время от времени просматривает папку и если находит в ней картинки - отправляет их модели, удаляя из папки. Модель сохраняет новый файл в папку с исходящими изображениями.
- отправитель [sender.py](sender.py) - просматривает папку исходящих картинок и из имени определяет чат и пользователя и высылает их получателю.   
