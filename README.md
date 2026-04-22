# 🏦 MTB Coins - Хакатон Проект

Веб-приложение с игровыми режимами, заработком и элементами геймификации.

## 🎯 Структура проекта

```
chachaton2.0/
├── backend/
│   ├── main.py           # FastAPI сервер
│   ├── models.py         # Модели данных
│   └── requirements.txt
├── frontend/
│   ├── app.py            # Streamlit главный файл
│   ├── pages/            # Отдельные страницы режимов
│   └── requirements.txt
└── README.md
```

## 🚀 Быстрый старт

### 1️⃣ Установка зависимостей

**Бэк:**
```bash
cd backend
pip install -r requirements.txt
```

**Фронт:**
```bash
cd frontend
pip install -r requirements.txt
```

### 2️⃣ Запуск

**Окно 1 - Бэк:**
```bash
cd backend
python main.py
```
Сервер доступен на `http://localhost:8000`

**Окно 2 - Фронт:**
```bash
cd frontend
streamlit run app.py
```
Приложение доступен на `http://localhost:8501`

## 📚 API Endpoints

### Пользователи
- `POST /user/register` - Регистрация
- `GET /user/{user_id}` - Данные пользователя

### Фарм
- `POST /farm/add-spending` - Добавить трату
- `GET /farm/buildings/{user_id}` - Получить здания

### Файт
- `POST /fight/create-round` - Создать раунд
- `POST /fight/record-tap` - Записать тап
- `GET /leaderboard` - Лидерборд

## 🎮 Режимы

1. **Лидерборд** - Топ игроков по МТ коинам
2. **Магазин** - Промокоды, услуги, кэш бэк
3. **Фарм** - Здания с пассивным доходом
4. **Файт** - Мини-игра с соперником

## 🛠️ Технологии

- **Backend:** FastAPI, Python
- **Frontend:** Streamlit, Python
- **Storage:** In-memory (готово для переноса на PostgreSQL)

## 📝 TODO

- [ ] Интеграция БД (PostgreSQL)
- [ ] Интерактивная карта в Farm режиме
- [ ] Game Loop для Fight режима
- [ ] Реальные промокоды в Shop
- [ ] Аутентификация
- [ ] Deploy (Docker)

---

**Статус:** 🔨 В разработке
