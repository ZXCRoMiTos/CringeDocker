import time
import redis
from flask import Flask
import pymysql
import psycopg2
import random


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
            
            
def get_name():
    names = ['Oliver', 'Jack', 'Harry', 'Jacob', 'Charley', 'Agnes', 'Adelaida', 'Ida', 'Iris']
    return random.choice(names)


def get_password():
    return random.randint(100000000, 1000000000)
    
    
def get_email():
    random_part = ['best', 'moscow', 'top', 'dpr', 'heavy', 'ugly', 'high', 'cringe', 'test']
    email_part = ['@gmail.com', '@mail.ru', '@yandex.ru', '@yahoo.com', '@hotmail.com']
    first_part = get_name()
    first_part = first_part[:len(first_part)//2].lower()
    second_part = get_name()
    second_part = second_part[len(second_part)//2:]
    return first_part + second_part + random.choice(random_part) + random.choice(email_part)
    
    
def get_nickname():
    nicknames = ['Oxonomy', 'BeardDemon', 'Succotash', 'Altometer', 'HereSheIs', 'GrownMan', 'Mountbatten', 'Promenader']
    first_part = random.choice(nicknames)
    first_part = first_part[:len(first_part)//2]
    second_part = random.choice(nicknames)
    second_part = second_part[len(second_part)//2:] 
    return first_part + second_part


@app.route('/')
def start_page():
    return '<img src="data:image/jpeg;base64,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"><br> \
                <a href="/redis">Redis</a><br><a href="/mysql">Mysql</a><br><a href="/postgres">Postgres</a>'


@app.route('/redis')
def redis():
    count = get_hit_count()
    return 'Hello World Docker! I have been seen {} times.\n'.format(count)
    

@app.route('/mysql')
def mysql():

    connection = pymysql.connect(host='mysql',
                             user='user',
                             password='test',
                             database='myDb',
                             cursorclass=pymysql.cursors.DictCursor)
                             
    try:
                             
        with connection.cursor() as cursor:
            try:
                create_table_query = "CREATE TABLE `users`(id int AUTO_INCREMENT," \
                                     " name varchar(32)," \
                                     " password varchar(32)," \
                                     " email varchar(32), PRIMARY KEY (id));"
                cursor.execute(create_table_query)
            except:
                pass
                
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO `users` (name, password, email) VALUE ('{get_name()}', '{get_password()}', '{get_email()}');"
            cursor.execute(insert_query)
            connection.commit()
            
        with connection.cursor() as cursor:
            select_all_rows = "SELECT * FROM `users`"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            if len(rows) <= 20:
                result = ''
                for row in rows:
                    tr = '<tr>'
                    tr += '<td style="padding: 10px;">' + str(row.get('id')) + '</td>'
                    tr += '<td style="padding: 10px;">' + str(row.get('name')) + '</td>'
                    tr += '<td style="padding: 10px;">' + str(row.get('password')) + '</td>'
                    tr += '<td style="padding: 10px;">' + str(row.get('email')) + '</td>'
                    tr += '</tr>'
                    result += tr
                return f"<h2>MYSQL Database:<h2><h3>Для добавления записи обновите страничку<h3><hr><table style='border: 1px solid;'><tr><td style='padding: 10px;'>ID</td> \
                            <td style='padding: 10px;'>NAME</td><td style='padding: 10px;'>PASSWORD</td><td style='padding: 10px;'>EMAIL</td></tr>{result}</table>"
            else:
                delete_query = "DELETE FROM `users`;"
                cursor.execute(delete_query)
                connection.commit()
                return '<h1>Каждые 20 записей таблица очищается :)<h1>'
    finally:
        connection.close()


@app.route('/postgres')    
def postgres():
    connection = psycopg2.connect(
                    host="postgres",
                    database="habrdb",
                    user="habrpguser",
                    password="pgpwd4habr")
    connection.autocommit = True
    
    try:
    
        with connection.cursor() as cursor:
            try:
                create_table_query = """CREATE TABLE users(
                                        id serial PRIMARY KEY,
                                        first_name varchar(32) NOT NULL,
                                        nick_name varchar(32) NOT NULL);"""
                cursor.execute(create_table_query)
            except:
                pass
        
        with connection.cursor() as cursor:
            insert_query =  f"INSERT INTO users (first_name, nick_name) VALUES('{get_name()}', '{get_nickname()}');"
            cursor.execute(insert_query)
        
        with connection.cursor() as cursor:
            select_all_rows = "SELECT * FROM users"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            if len(rows) <= 20:
                result = ''
                for row in rows:
                    tr = '<tr>'
                    tr += '<td style="padding: 10px;">' + str(row[0]) + '</td>'
                    tr += '<td style="padding: 10px;">' + str(row[1]) + '</td>'
                    tr += '<td style="padding: 10px;">' + str(row[2]) + '</td>'
                    tr += '</tr>'
                    result += tr
                return f"<h2>POSTGRESQL Database:<h2><h3>Для добавления записи обновите страничку<h3><hr><table style='border: 1px solid;'><tr><td style='padding: 10px;'>ID</td> \
                            <td style='padding: 10px;'>FIRST NAME</td><td style='padding: 10px;'>NICK NAME</td>{result}</table>"
            else:
                delete_query = "DELETE FROM users;"
                cursor.execute(delete_query)
                return '<h1>Каждые 20 записей таблица очищается :)<h1>'
    finally:
        connection.close()
    