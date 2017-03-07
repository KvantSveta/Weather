## Weather

**Цель проекта** - определить есть ли взаимосвязь между погодой и головной болью а так же температурой тела.


Установка зависимостей
```bash
pip install -r requirements.txt
```

on Desktop in ~/Weather

build
```bash
docker build -t service:1.0 -f dockerfiles/service/Dockerfile .
```

run
```bash
docker run -d --net=host service:1.0 main/service.py
docker run -d --net=host service:1.0 main/web.py
```

run via docker-compose
```bash
docker-compose up -d
```

Команда для остановки контейнера
```bash
docker kill -s 15 CONTAINER_ID
```

on RPi in ~/Weather

build
```bash
docker build -t raspbian-service:1.0 -f dockerfiles/raspbian-service/Dockerfile .
```
run
```bash
docker run -d --net=host --device /dev/gpiomem raspbian-service:1.0 main/service.py
docker run -d --net=host --device /dev/gpiomem raspbian-service:1.0 main/web.py
```