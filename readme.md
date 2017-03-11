## Weather

**Цель проекта** - определить есть ли взаимосвязь между погодой и головной болью а так же температурой тела.


Установка зависимостей
```bash
pip install -r requirements.txt
```

**on Desktop in ~/Weather**

build image
```bash
docker build -t service:1.0 -f Dockerfile.dev .
```

run image
```bash
docker run -d --net=host service:1.0 main/service.py
docker run -d --net=host service:1.0 main/web.py
```

build via docker-compose
```bash
docker-compose -f docker-compose.dev.yml build
```

run via docker-compose
```bash
docker-compose -f docker-compose.dev.yml up -d
```

Команда для остановки контейнера
```bash
docker kill -s 15 CONTAINER_ID
```

**on RPi in ~/Weather**

build image
```bash
docker build -t raspbian-service:1.0 -f Dockerfile .
```
run image
```bash
docker run -d --net=host --device /dev/gpiomem raspbian-service:1.0 main/service.py
docker run -d --net=host --device /dev/gpiomem raspbian-service:1.0 main/web.py
```

build via docker-compose
```bash
docker-compose -f docker-compose.yml build
```

run via docker-compose
```bash
docker-compose -f docker-compose.yml up -d
```