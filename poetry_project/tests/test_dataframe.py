from plt_temp import create_dataframe
import pandas as pd


def test_create_dataframe():
    # Исходные данные специально расположены не по порядку
    hours = [
        "2026-10-20T14:00",
        "2026-10-20T12:00",
        "2026-10-20T13:00"
    ]
    temps = [15.0, 10.0, 12.5]

    df = create_dataframe(hours, temps)

    # 1. Проверка названий столбцов
    assert list(df.columns) == ["time", "temperature_c"]

    # 2. Проверка количества строк
    assert len(df) == 3

    # 3. Проверка сортировки по времени
    assert df["time"].is_monotonic_increasing

    # 4. Проверка соответствия температур времени
    assert df["time"].tolist() == list(pd.to_datetime([
        "2026-10-20T12:00",
        "2026-10-20T13:00",
        "2026-10-20T14:00"
    ]))

    assert df["temperature_c"].tolist() == [10.0, 12.5, 15.0]
