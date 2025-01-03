# insurance-project

Добрый день.

Сервис по расчету страховки товаров на основе типа груза и тарифа.
Тариф отправляется в формате json и имеет вид показанный ниже.

```json 
{
    "2020-06-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.04"
        },
        {
            "cargo_type": "Other",
            "rate": "0.01"
        }
    ],
    "2020-07-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.035"
        },
        {
            "cargo_type": "Other",
            "rate": "0.015"
        }
    ]
} 
```

Сервис сохраняет тарифы в PostgreSQL, а также имеет возможность работы с ними методами CRUD.
Ознакомиться со всеми методами можно по http://0.0.0.0:8000/docs

Что-бы поднять сервис скачайте репозиторий и запустите команду 
```docker compose up -d --build```
Эта команда запустит создание контейнеров и настройку бд с помощью миграций alembic, создание topics kafka.
Контейнеры: API, PostgresSQL, Kafka (zookeeper, ui)

Для расчета страховки отправьте запрос на адрес http://0.0.0.0:8000/api/v1/insurance/
Укажите: типа груза, дату, обьявленную стоимость. В результате вы получитите стоимость или исключение если в бд нет тарифа на данный товар.
Пример curl

```bash 
curl -X 'POST'
'http://0.0.0.0:8000/api/v1/insurance/?insurance_date=2020-07-01&cargo_type=Glass&declared_cost=110.50'
-H 'accept: application/json'
-d '' 
```

Настроено логирование изменений тарифов (добавление, изменение, удаление).
Логи отправляются в автоматически созданный топик kafka при создании контейнеров.
С информацией timestamp, user_id если передан, сообщение об операции с количеством добавленных тарифов, удаленным id тарифа и т.д.