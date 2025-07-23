# Diplom_3
# Проект автоматизации тестирования Stellar Burgers

## Описание
Этот проект содержит автоматизированные UI-тесты для веб-приложения Stellar Burgers. Тесты написаны с использованием Pytest и Selenium WebDriver. Для генерации отчетов используется Allure.

## Структура проекта
- locators/ — файлы с локаторами для страниц
- pages/ — классы страниц с методами взаимодействия
- tests/ — тестовые сценарии и конфигурация тестового окружения
- urls.py — файл с основными URL для тестов
- .gitignore — настройки исключений для Git
- requirements.txt — список зависимостей проекта
- README.md — этот файл

## Установка и подготовка
1. Клонируйте репозиторий:
git clone <URL_репозитория>
cd <папка_проекта>

2. Создайте и активируйте виртуальное окружение:
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
.venv\Scripts\activate        # Windows

3. Установите зависимости:
pip install -r requirements.txt

## Запуск тестов
Для запуска всех тестов с генерацией результатов для Allure используйте команду:
pytest tests/ --alluredir=allure-results

## Просмотр отчёта Allure
1. Сгенерируйте HTML-отчёт из результатов:
allure serve allure-results

или, если установлен allure командой:
allure generate allure-results -o allure-report --clean

2. Откройте отчет локально:
allure open allure-report

## Особенности
Тесты запускаются параллельно в браузерах Chrome и Firefox (настройка в conftest.py).
Для авторизации создаётся временный пользователь через API и удаляется после теста.
Используется Page Object Model для поддержки и расширения тестов.
Все основные шаги тестов аннотированы шагами Allure для удобного анализа.
