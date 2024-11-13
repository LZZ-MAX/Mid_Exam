import sqlite3
import json

# db config
conn = sqlite3.connect('movies.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def create_table():
    """
    Create the movies table if it does not exist.
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL CHECK(rating >= 1.0 AND rating <= 10.0)
        )
    ''')


def main():
    """
    Main function to run the movie management system.
    """
    create_table()

    while True:
        print('\n-----電影管理系統-----')
        print('1. 匯入電影資料檔')
        print('2. 查詢電影')
        print('3. 新增電影')
        print('4. 修改電影')
        print('5. 刪除電影')
        print('6. 匯出電影')
        print('7. 離開系統')
        print('-' * 24)

        try:
            choice = int(input('請選擇操作選項（1-7）：'))

            match choice:
                case 1:
                    movie_input()
                case 2:
                    check_movie()
                case 3:
                    add_movie()
                case 4:
                    modify_movie()
                case 5:
                    delete_movie()
                case 6:
                    movie_output()
                case 7:
                    print("離開系統")
                    break
        except ValueError:
            print('請輸入數字1-7')


def movie_input():
    """
    Import movie data from a JSON file and insert it into the database.
    """
    try:
        with open('movies.json', 'r', encoding='utf-8') as file:
            movies = json.load(file)

        for movie in movies:
            cursor.execute('''
                INSERT INTO movies (title, director, genre, year, rating)
                VALUES (?, ?, ?, ?, ?)
            ''', (movie['title'], movie['director'], movie['genre'], movie['year'], movie['rating']))

        conn.commit()
        print('電影已匯入')
    except FileNotFoundError:
        print('找不到檔案...')


def check_movie():
    """
    Check and display movie data from the database.
    """
    cursor.execute('SELECT * FROM movies')
    all_records = cursor.fetchall()
    if not all_records:
        print('目前無電影資料')
        return

    choice = input('查詢全部電影嗎？（y/n）:').strip().lower()
    if choice == 'y':
        print('電影列表：')
        print(f'{"電影名稱":<15}{chr(12288)*2}{"導演":<20}{chr(12288)}{"類型":<10}{chr(12288)}{"上映年份":<10}{chr(12288)}{"評分":<10}')
        print('-' * 72)
        for row in all_records:
            print(f'{row["title"]:<15}{chr(12288)*2}{row["director"]:<15}{chr(12288)}{row["genre"]:<11}{chr(12288)}{row["year"]:<15}{chr(12288)}{row["rating"]:<10}')
    elif choice == 'n':
        print('請輸入電影名稱：')
        title = input()
        cursor.execute('SELECT * FROM movies WHERE title like ?', (f'%{title}%',))
        movie = cursor.fetchone()
        if movie:
            print(f'{"電影名稱":<15}{chr(12288)*2}{"導演":<20}{chr(12288)}{"類型":<10}{chr(12288)}{"上映年份":<10}{chr(12288)}{"評分":<10}')
            print('-' * 72)
            print(f'{movie["title"]:15}{chr(12288)*2}{movie["director"]:<15}{chr(12288)}{movie["genre"]:<11}{chr(12288)}{movie["year"]:<15}{chr(12288)}{movie["rating"]:<10}')
        else:
            print('找不到電影')


def modify_movie():
    """
    Modify movie data in the database.
    """
    try:
        print('請輸入要修改的電影名稱：')
        title = input()

        cursor.execute('SELECT * FROM movies WHERE title like ?', (f'%{title}%',))
        movie = cursor.fetchone()

        if movie:
            print(f'{"電影名稱":<15}{chr(12288)*2}{"導演":<20}{chr(12288)}{"類型":<10}{chr(12288)}{"上映年份":<10}{chr(12288)}{"評分":<10}')
            print('-' * 72)
            print(f'{movie["title"]:15}{chr(12288)*2}{movie["director"]:<15}{chr(12288)}{movie["genre"]:<11}{chr(12288)}{movie["year"]:<15}{chr(12288)}{movie["rating"]:<10}')

            name = input('請輸入新的電影名稱（若不修改直接按Enter）：') or movie['title']
            director = input('請輸入新的導演（若不修改直接按Enter）：') or movie['director']
            genre = input('請輸入新的類型（若不修改直接按Enter）：') or movie['genre']
            year = input('請輸入新的年份（若不修改直接按Enter）：') or movie['year']
            rating = input('請輸入新的評分（1.0 - 10.0）（若不修改直接按Enter）：') or movie['rating']
            cursor.execute('''
                UPDATE movies
                SET title = ?,
                    director = ?,
                    genre = ?,
                    year = ?,
                    rating = ?
                WHERE title = ?
            ''', (name, director, genre, year, rating, title))
            conn.commit()
            print('電影資料已更新')
        else:
            print('找不到此電影')

    except sqlite3.DatabaseError as e:
        print(f'錯誤： {e}')


def delete_movie():
    """
    Delete movie data from the database.
    """
    choice = input('刪除全部的的電影嗎（y/n）：').strip().lower()
    if choice == 'y':
        cursor.execute('DELETE FROM movies')
        conn.commit()
        print('全部電影已刪除')
        return

    elif choice == 'n':
        print('請輸入要刪除的電影名稱：')
        title = input()
        cursor.execute('SELECT * FROM movies WHERE title like ?', (f'%{title}%',))
        movie = cursor.fetchone()
        if movie:
            print(f'{"電影名稱":<15}{chr(12288)*2}{"導演":<20}{chr(12288)}{"類型":<10}{chr(12288)}{"上映年份":<10}{chr(12288)}{"評分":<10}')
            print('-' * 72)
            print(f'{movie["title"]:15}{chr(12288)*2}{movie["director"]:<15}{chr(12288)}{movie["genre"]:<11}{chr(12288)}{movie["year"]:<15}{chr(12288)}{movie["rating"]:<10}')
            choice = input('是否要刪除（y/n）:').strip().lower()
            if choice == 'y':
                cursor.execute('DELETE FROM movies WHERE title like ?', (f'%{title}%',))
                conn.commit()
                print('電影已刪除')
            else:
                print('取消刪除')
        else:
            print('找不到電影')


def movie_output():
    """
    Export movie data from the database to a JSON file.
    """
    cursor.execute('SELECT * FROM movies')
    all_records = cursor.fetchall()
    if not all_records:
        print('目前無電影資料')
        return

    with open('exported.json', 'w', encoding='utf-8') as file:
        json.dump([dict(row) for row in all_records], file, ensure_ascii=False, indent=4)
        print('電影已匯出')