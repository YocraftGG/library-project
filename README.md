# Library Project

מערכת לניהול ספרים וחברי ספרייה עם FastAPI, MySql ו-OOP.
המערכת תאשפר להוסיף למחוק לשנות ולצפות בסטטיסטיקות של ספרים וחברי ספרייה

## הקוד ליצירת docker עם MySql

docker run --name mysql-library \
    -e MYSQL_ROOT_PASSWORD=root \
    -e MYSQL_DATABASE=library_db \
    -p 3306:3306 \
    -d mysql:8

## מבנה התיקיות

library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db\_connection.py  
│   │   ├── book\_db.py  
│   │   └── member\_db.py  
│   ├── routes/  
│   │   ├── book\_routes.py  
│   │   ├── member\_routes.py  
│   │   └── report\_routes.py  
│   └── logs/  
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore

## טבלת ספרים

| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `title` | כותרת הספר, עמודה לא ריקה, מקסימום 50 תווים |
| `author` | שם המחבר, עמודה לא ריקה, מקסימום 50 תווים |
| `genre` | **ערכי `genre` מותרים:**  Fiction | Non-Fiction | Science | History | Other — מומש כעמודת ENUM במסד הנתונים, כל ערך אחר מחזיר שגיאה, עמודה לא ריקה |
| `is_available` | האם הספר זמין להשאלה — FALSE מסמן הושאל עמודה לא ריקה |
| `borrowed_by_member_id` | מזהה החבר שמחזיק את הספר — NULL אם זמין |

## טבלת חברי ספרייה

| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `name` | שם החבר, עמודה לא ריקה, מקסימום 50 תווים |
| `email` | כתובת מייל — ייחודית, עמודה לא ריקה |
| `is_active` | האם החבר פעיל — FALSE לא יכול להשאיל עמודה לא ריקה |
| `total_borrows` | מונה סה"כ השאלות — עולה ב-1 בכל השאלה עמודה לא ריקה |

## חוקי מערכת

| חוק | נושא | הכלל |
| ----: | ----: | ----: |
| 1 | יצירת ספר | המשתמש שולח title/author/genre — המערכת מוסיפה `is_available=True`, `borrowed_by=NULL` |
| 2 | genre | חייב להיות Fiction / Non-Fiction / Science / History / Other — כל ערך אחר מחזיר שגיאה יש לוודא הן בהוספה (POST) והן בעדכון (PATCH) |
| 3 | יצירת חבר | המשתמש שולח name/email — המערכת מוסיפה `is_active=True`, `total_borrows=0` |
| 4 | email | חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה |
| 5 | חבר לא פעיל | אם `is_active=False` — אי אפשר להשאיל ספר |
| 6 | ספר לא זמין | אי אפשר להשאיל ספר שכבר מושאל (`is_available=False`) |
| 7 | מקסימום ספרים | חבר לא יכול להחזיק יותר מ-3 ספרים בו-זמנית |
| 8 | החזרת ספר | ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו |

## נקודות קצה

### Books

| Method | Endpoint | תיאור |
| :---- | :---- | :---- |
| `POST` | `/books` | יצירת ספר |
| `GET` | `/books` | כל הספרים |
| `GET` | `/books/{id}` | ספר לפי ID |
| `PATCH` | `/books/{id}` | עדכון ספר |
| `PATCH` | `/books/{id}/borrow/{member_id}` | השאלת ספר לחבר |
| `PATCH` | `/books/{id}/return/{member_id}` | החזרת ספר מחבר |

### Members

| Method | Endpoint | תיאור |
| :---- | :---- | ----: |
| `POST` | `/members` | יצירת חבר |
| `GET` | `/members` | כל החברים |
| `GET` | `/members/{id}` | חבר לפי ID |
| `PATCH` | `/members/{id}` | עדכון חבר |
| `PATCH` | `/members/{id}/deactivate` | השבתת חבר |
| `PATCH` | `/members/{id}/activate` | הפעלת חבר |

### Reports

| Method | Endpoint | תיאור |
| :---- | :---- | ----- |
| `GET` | `/reports/summary` | דוח כללי |
| `GET` | `/reports/books-by-genre` | ספרים לפי ז'אנר |
| `GET` | `/reports/top-member` | החבר הכי פעיל |

## זרימת המערכת

Request --> FastAPI --> OOP --> MySQL --> Responce

## הוראות הרצה

### פתיחת `venv`
```bash
python -m venv venv
```

```bash
venv\Sctipts\activate
```

### התקנת `requirements`

```bash
pip install -r requirements.txt
```

### התחלת ה-`container`

```bash
docker start mysql-library
```

### הרצת השרת

```bash
python main.py
```

### פתיחת Swagger

```text
127.0.0.1:8000/docs
```