# Diplom_3 - UI тесты для Stellar Burgers

## Описание
Автотесты для веб-приложения Stellar Burgers с использованием паттерна Page Object.

## Технологии
- Python 3.14
- pytest 8.3.3
- selenium 4.25.0
- allure-pytest 2.13.5

## Тестовые сценарии
- Переход по клику на «Конструктор»
- Переход по клику на «Лента заказов»
- Клик на ингредиент → открывается модальное окно
- Модальное окно закрывается кликом по крестику
- Счётчик ингредиента увеличивается
- Счётчик «Выполнено за всё время» увеличивается
- Счётчик «Выполнено за сегодня» увеличивается
- Номер заказа появляется в разделе «В работе»

## Запуск
```bash
pip install -r requirements.txt
pytest tests/ --browser=chrome --alluredir=allure_results -v
allure generate allure_results -o allure_report
allure open allure_report