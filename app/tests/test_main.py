from .test_app import client


def test_create_shift_tasks():
    response = client.post("/shift_task", json=[
        {
            "СтатусЗакрытия": False,
            "ПредставлениеЗаданияНаСмену": "Задание на смену 2345",
            "Линия": "Т2",
            "Смена": "1",
            "Бригада": "Бригада №4",
            "НомерПартии": 444544,
            "ДатаПартии": "2024-01-30",
            "Номенклатура": "Какая то номенклатура",
            "КодЕКН": "456678",
            "ИдентификаторРЦ": "A",
            "ДатаВремяНачалаСмены": "2024-01-30T20:00:00+05:00",
            "ДатаВремяОкончанияСмены": "2024-01-31T08:00:00+05:00"
        },
        {
            "СтатусЗакрытия": False,
            "ПредставлениеЗаданияНаСмену": "Задание на смену 2345",
            "Линия": "Т2",
            "Смена": "1",
            "Бригада": "Бригада №4",
            "НомерПартии": 55555,
            "ДатаПартии": "2024-01-30",
            "Номенклатура": "Какая то номенклатура",
            "КодЕКН": "456678",
            "ИдентификаторРЦ": "A",
            "ДатаВремяНачалаСмены": "2024-01-30T20:00:00+05:00",
            "ДатаВремяОкончанияСмены": "2024-01-31T08:00:00+05:00"
        },
    ])
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0].get('submission_task_shift') == "Задание на смену 2345"
    assert response.json()[0].get("closed_at") is None
    assert response.json()[0].get('batch_number') == 444544
    assert response.json()[1].get('submission_task_shift') == "Задание на смену 2345"
    assert response.json()[1].get("closed_at") is None
    assert response.json()[1].get('batch_number') == 55555


def test_create_products_unique_code():
    response = client.post(
        "/shift_task/create_products/",
        json=[
            {
                "УникальныйКодПродукта": "12gRV60MMsn1",
                "НомерПартии": 22222,
                "ДатаПартии": "2024-01-25"
            },
            {
                "УникальныйКодПродукта": "12gRV60MMsn2",
                "НомерПартии": 55555,
                "ДатаПартии": "2024-01-30"
            }
        ],
    )
    assert response.status_code == 200
    assert response.json() == []
