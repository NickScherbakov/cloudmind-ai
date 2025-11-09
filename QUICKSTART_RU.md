# CloudMind AI - Быстрый старт

Это руководство поможет вам запустить CloudMind AI менее чем за 5 минут!

## 🚀 Установка в один клик

### Для тестирования и демонстрации

Самый быстрый способ попробовать CloudMind AI:

```bash
# Клонируйте репозиторий
git clone https://github.com/NickScherbakov/cloudmind-ai.git
cd cloudmind-ai

# Запустите интерактивную настройку
chmod +x setup.sh
./setup.sh
```

Выберите опцию **1** (Production mode) при запросе. API будет доступен по адресу:
- API: http://localhost:8000
- Интерактивная документация: http://localhost:8000/docs

### Для разработки

Если вы хотите внести вклад или изменить код:

```bash
# Клонируйте репозиторий
git clone https://github.com/NickScherbakov/cloudmind-ai.git
cd cloudmind-ai

# Запустите настройку и выберите опцию 2 (Development mode)
chmod +x setup.sh
./setup.sh
```

Или используйте Make:

```bash
make setup
make dev
```

Ваши изменения в каталоге `src/` будут автоматически перезагружаться.

## 📋 Требования

Вам нужны только:
- **Docker** (20.10+) - [Установить Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (2.0+) - Обычно включен в Docker Desktop

Это все! Все зависимости Python обрабатываются автоматически внутри контейнера.

## 🎯 Что дальше?

### 1. Настройте облачных провайдеров

Отредактируйте файл `.env` для добавления учетных данных облачных провайдеров:

```bash
# AWS
AWS_ENABLED=true
AWS_ACCESS_KEY_ID=ваш_ключ
AWS_SECRET_ACCESS_KEY=ваш_секрет
AWS_REGION=us-east-1

# Azure
AZURE_ENABLED=true
AZURE_SUBSCRIPTION_ID=ваш_id
# ... другие настройки Azure
```

Перезапустите сервис после редактирования:

```bash
docker compose restart
# или
make restart
```

### 2. Попробуйте API

Откройте браузер и перейдите на http://localhost:8000/docs для интерактивной документации API.

Попробуйте некоторые эндпоинты:
- `GET /` - Информация об API
- `GET /health` - Проверка работоспособности
- `GET /providers` - Список настроенных облачных провайдеров

### 3. Используйте CLI

```bash
# Внутри контейнера
docker compose exec cloudmind-api python cloudmind_cli.py --help

# Разовые команды
docker compose run --rm cloudmind-api python cloudmind_cli.py version
docker compose run --rm cloudmind-api python cloudmind_cli.py info
```

### 4. Запустите тесты

```bash
docker compose -f docker-compose.dev.yml run --rm cloudmind-test
# или
make test
```

## 🔧 Основные команды

| Команда | Описание |
|---------|----------|
| `./setup.sh` | Интерактивное меню настройки |
| `make help` | Показать все доступные команды |
| `make up` | Запустить в режиме production |
| `make dev` | Запустить в режиме разработки |
| `make test` | Запустить тесты |
| `make logs` | Просмотр логов |
| `make stop` | Остановить все сервисы |
| `make clean` | Удалить контейнеры и образы |

## 🆘 Устранение неполадок

### Порт 8000 уже используется

Отредактируйте `docker-compose.yml` и измените маппинг портов:

```yaml
ports:
  - "8001:8000"  # Использовать порт 8001 на вашей машине
```

### Изменения не применяются

Если вы изменили код и не видите изменений:

1. Убедитесь, что используете режим разработки: `make dev`
2. Проверьте, что файлы монтируются: `docker compose -f docker-compose.dev.yml config`
3. Перезапустите: `make restart`

### Не удается подключиться к Docker

Убедитесь, что Docker запущен:

```bash
docker ps
```

Если не работает, запустите Docker Desktop (macOS/Windows) или выполните `sudo systemctl start docker` (Linux).

### Нужна помощь?

- Смотрите [руководство по настройке Docker](docs/docker_setup.md) для подробной информации
- См. основной [README](../README.md) для документации API
- Откройте issue на GitHub

## 📚 Дополнительные ресурсы

- [Полная документация](../README.md)
- [Руководство по настройке Docker](docs/docker_setup.md)
- [Справочник API](docs/api_reference.md)
- [Руководство по началу работы](docs/getting_started.md)

## 💡 Советы для контрибуторов

1. Всегда используйте режим разработки при написании кода: `make dev`
2. Запускайте тесты перед коммитом: `make test`
3. Проверяйте логи в случае проблем: `make logs-dev`
4. Откройте shell в контейнере для отладки: `make shell`

Удачи в разработке! 🎉

---

**Для Windows пользователей:** Используйте `setup.bat` вместо `setup.sh`

**English version:** See [QUICKSTART.md](QUICKSTART.md)
