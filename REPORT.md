# Отчёт по практической работе № 2

**Тема:** Управление зависимостями Python: `venv + pip` и Poetry.

## 1. Версии Python, Poetry и операционная система

| Параметр | Значение |
|---|---|
| Операционная система | Windows (`win32` по выводу pytest) |
| Python | 3.12.5 |
| Poetry | 2.5.1 |

Команды проверки и результаты:

```cmd
poetry --version
```
```text
Poetry (version 2.5.1)
```

```cmd
poetry run python -m pytest tests/ -v
```
```text
platform win32 -- Python 3.12.5, pytest-9.1.1, pluggy-1.7.0
```

## 2. Пути к интерпретаторам обеих частей

**`pip_project`** — путь после создания `.venv`:

```text
C:\Users\Admin\Desktop\практика_2 mlops\pip_project\.venv\Scripts\python.exe
```

**`poetry_project`** — путь подтверждён выводом pytest:

```text
C:\Users\Admin\Desktop\практика_2 mlops\poetry_project\.venv\Scripts\python.exe
```

Проверка Poetry:

```cmd
poetry env info --executable
```

## 3. Прямые зависимости и их назначение

| Пакет | Назначение |
|---|---|
| `requests` | HTTP-запрос к Open-Meteo, проверка ответа и ограничение времени ожидания |
| `pandas` | Создание `DataFrame`, сортировка по времени, экспорт CSV |
| `matplotlib` | Построение графика и сохранение `temperature_24h.png` |

В Poetry также созданы дополнительные группы: **`test`** — `pytest` (автоматические тесты), **`dev`** — `ruff` (проверка и форматирование кода). Эти инструменты не относятся к основным зависимостям скрипта.

## 4. Примеры транзитивных зависимостей

| Прямой пакет | Транзитивная зависимость | Для чего используется |
|---|---|---|
| `requests` | `urllib3` | HTTP-соединения |
| `pandas` | `numpy` | Операции с массивами и числовыми данными |
| `matplotlib` | `contourpy` | Построение контуров |

Примеры можно проверить через `poetry show --tree`. `numpy` не объявляется прямой зависимостью скрипта, поскольку `plt_temp.py` не импортирует его самостоятельно.

## 5. Восстановление окружения `pip_project`

Список пакетов с точными версиями сохраняется в `requirements.txt`. После удаления только `.venv` окружение создаётся заново, а зависимости восстанавливаются без индивидуальной установки:

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python plt_temp.py
```

**Результат:** Зависимости восстановлены через requirements.txt, скрипт успешно выполнился. 

## 6. Результат проверки групп Poetry

Проверка выполняется последовательной синхронизацией окружения:

| Команда | Выбранные группы | `pytest` | `ruff` | `plt_temp.py` |
|---|---|---|---|---|
| `poetry sync --only main` | `main` | Нет | Нет | Может запускаться при доступном API |
| `poetry sync --only test` | `test`, без `main` | Да | Нет | Не запускается без основных зависимостей |
| `poetry sync --with test,dev` | `main`, `test`, `dev` | Да | Да | Может запускаться при доступном API |

**Объяснение:** `--only` выбирает исключительно перечисленные группы, а `--with` добавляет указанные необязательные группы к основным. `poetry sync` удаляет пакеты, не соответствующие выбранному составу. Таблица показывает ожидаемое поведение на основе конфигурации; отдельных терминальных выводов для первых двух режимов не предоставлено. Полное окружение подтверждено успешным запуском теста и скрипта (раздел 8).

## 7. Результат точечного обновления зависимости

Для прямой зависимости `requests` изменено ограничение в `pyproject.toml`:

```toml
"requests (>=2.32,<3.0)"
```

Команда и результат:

```cmd
poetry update requests
```
```text
Updating dependencies
Resolving dependencies... (0.2s)
No dependencies to install or update
Writing lock file
```

**Итог:** ограничение прямой зависимости задано как `>=2.32,<3.0`. Poetry не потребовалось устанавливать или обновлять версии пакетов; соответственно, по результату команды обновление установленной версии `requests` и её транзитивных зависимостей не подтверждается. При этом `poetry.lock` был повторно записан.

Проверка изменений:

```cmd
git diff -- pyproject.toml poetry.lock
```
```
diff --git a/poetry.lock b/poetry.lock
index a381215..3218511 100644
--- a/poetry.lock
+++ b/poetry.lock
@@ -1109,4 +1109,4 @@ zstd = ["backports-zstd (>=1.0.0) ; python_version < \"3.14\""]
 [metadata]
 lock-version = "2.1"
 python-versions = ">=3.12,<3.13"
-content-hash = "cc389dfc4950c160cb577ffa586c2f77a9758271e503bdb8a160b2dae686a13a"
+content-hash = "ac87496ac12cec8b6fc770d731030d1bb699ab5ff1276b712ceab11e07618a4f"

```
**Итог:** Изменение только content-hash, когда конфигурация зависимостей изменилась, а их разрешённые версии остались прежними.

## 8. Результат чистого восстановления Poetry-проекта

Экспорт зависимостей, включая группы `test` и `dev`:

```cmd
poetry export -f requirements.txt --with test,dev --output requirements.txt
```

Для чистого восстановления удаляется только `poetry_project\.venv`, после чего используются файлы `pyproject.toml` и `poetry.lock`:

```cmd
poetry env use "C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe"
poetry sync --with test,dev
```

**Проверка тестов:**

```cmd
poetry run python -m pytest tests/ -v
```
```text
tests/test_dataframe.py::test_create_dataframe PASSED [100%]
1 passed in 1.15s
```

Тест использует локальные списки и без сетевого запроса проверяет названия столбцов, число строк, сортировку времени и соответствие температур временным меткам.

**Проверка скрипта:**

```cmd
poetry run python plt_temp.py
```
```text
Сохранено в temperature_24h.csv
Сохранено в temperature_24h.png
```

**Проверка числа строк CSV:**

```cmd
poetry run python -c "import pandas as pd; print(len(pd.read_csv('temperature_24h.csv')))"
```
```text
24
```

Таким образом, тест прошёл, оба файла были сформированы, а CSV содержит 24 строки данных. Предоставленный вывод подтверждает рабочее окружение после выполнения этапов восстановления, но не содержит отдельного журнала удаления `.venv` и повторной установки зависимостей.

## 9. Сравнение `venv + pip` и Poetry

| Критерий | `venv + pip` | Poetry |
|---|---|---|
| Изоляция | `.venv` создаётся стандартным модулем `venv` | `.venv` создаётся и управляется Poetry |
| Прямые зависимости | Задаются вручную; `pip freeze` выводит все установленные пакеты | Явно описаны в `pyproject.toml` |
| Фиксация версий | `requirements.txt`, сформированный `pip freeze`, содержит точные версии прямых и транзитивных пакетов | `poetry.lock` фиксирует разрешённые версии зависимостей |
| Восстановление | `pip install -r requirements.txt` | `poetry sync` по `pyproject.toml` и `poetry.lock` |
| Группы зависимостей | При необходимости организуются отдельными файлами или командами | Встроенные группы `main`, `test`, `dev` |

**Вывод:** в подходе `venv + pip` воспроизводимость состава Python-пакетов обеспечивает `requirements.txt` с точными версиями. В Poetry — согласованные `pyproject.toml` (прямые зависимости и ограничения) и `poetry.lock` (разрешённые версии всех зависимостей). В обоих случаях для воспроизводимости важно также использовать совместимую версию Python и учитывать операционную систему.
