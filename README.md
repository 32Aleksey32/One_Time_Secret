# One_time_secret

### «Хранитель секретов».
Сервис для одноразовых секретов наподобие https://onetimesecret.com/.

### Описание проекта:
- Метод `/generate/` принимает секрет, кодовую фразу и отдаёт кодовую фразу и secret_key,
по которому этот секрет можно получить.
- Метод `/secrets/<secret_key>/` принимает кодовую фразу и отдаёт секрет.
- Возможность задавать время жизни для секретов (7 дней, 3 дня, 1 день, 1 час, 30 минут, 5 минут)
- Секреты и кодовые фразы не хранятся в базе в открытом виде.
- Просроченные секреты удаляются каждые сутки в полночь.

### Как работать с API:
- для создания секрета перейдите по адресу http://127.0.0.1/api/generate
- для прочтения секрета перейдите по адресу http://127.0.0.1/api/secrets/<secret_key>

### Установка:
- Клонируйте репозиторий
   ```
    https://github.com/32Aleksey32/One_time_secret
   ```
- Создайте файл .env в корне проекта с данными:
  ```
  DB_ENGINE=django.db.backends.postgresql
  DB_NAME=postgres
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  DB_HOST=db
  DB_PORT=5432
  ```
- Создайте и запустите контейнеры:
   ```
    docker-compose up
   ```
- Войдите в контейнер backend и введите команду:
   ```
    celery -A onetimesecret worker --beat
   ```

### Стек технологий использованный в проекте:
- Python
- Django
- Django Rest Framework
- Docker
- PostgreSQL
- Redis
- Celery