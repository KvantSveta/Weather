## Weather

**Цель проекта** - определить есть ли взаимосвязь между погодой и головной болью а так же температурой тела.


Установка зависимостей
```bash
pip install -r requirements.txt
```

on Desktop in ~/Weather
```bash
docker run -d --net=host -v /home/jd/Coding/Weather/:/home -w /home service:1.0 service.py
docker run -d --net=host -v /home/jd/Coding/Weather/:/home -w /home service:1.0 web.py
```

Команда для остановки контейнера
```bash
docker kill -s 15 CONTAINER_ID
```

on RPi in ~/Weather
```bash
docker run -d --net=host --device /dev/gpiomem -v /home/jd/Weather/:/home -w /home raspbian-service:1.0 main/service.py
docker run -d --net=host --device /dev/gpiomem -v /home/jd/Weather/:/home -w /home raspbian-service:1.0 main/web.py
```
