import psycopg2

def delete_tables(cursor):
    cur.execute("""
                DROP TABLE ClientsInfo CASCADE;
                DROP TABLE ClientsPhoneNumbers CASCADE;
                """)
    return conn.commit()

def create_tables(cursor):
        cur.execute("""CREATE TABLE IF NOT EXISTS ClientsInfo(
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(40) NOT NULL,
                            last_name VARCHAR(40) NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL
                        );
                        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS ClientsPhoneNumbers(
                            id SERIAL PRIMARY KEY,
                            phone_number BIGINT,
                            client_id INTEGER NOT NULL REFERENCES ClientsInfo(id)
                            ON DELETE CASCADE
                    );
                    """)

        return conn.commit()

def add_client(cursor, name, last_name, email=None):
    cur.execute("""
            INSERT INTO ClientsInfo(name, last_name, email)
                VALUES(%s, %s, %s)
                RETURNING id, name, last_name, email;
            """, (name, last_name, email))
    return cur.fetchone()

def add_phone_number(cursor, phone_number, client_id):
    cur.execute("""
            INSERT INTO ClientsPhoneNumbers(phone_number, client_id)
                VALUES(%s, %s)
                RETURNING id, phone_number, client_id;
            """, (phone_number, client_id))
    return cur.fetchone()

def update_data(cursor, name, last_name, email, id):
    cur.execute("""
            UPDATE ClientsInfo SET name=%s, last_name=%s, email=%s WHERE id=%s
            RETURNING id, name, last_name, email;
            """, (name, last_name, email, id))
    return cur.fetchone()

def update_phone_number(cursor, phone_number, id):
    cur.execute("""
            UPDATE ClientsPhoneNumbers SET phone_number=%s WHERE id=%s
            RETURNING id, phone_number;
            """, (phone_number, id))
    return cur.fetchone()

def delete_phone_number(cursor, id):
    cur.execute("""
            DELETE FROM ClientsPhoneNumbers WHERE id=%s;
            """, (id,))
    return conn.commit()

def delete_client_info(cursor, id):
    cur.execute("""
            DELETE FROM ClientsInfo WHERE id=%s;
            """, (id,))
    return conn.commit()

def get_client_info(cursor, name=None, last_name=None, email=None, phone_number=None):
    cur.execute("""
            SELECT ci.name, ci.last_name, ci.email, cpn.phone_number FROM ClientsInfo ci
            LEFT JOIN ClientsPhoneNumbers cpn ON cpn.client_id = ci.id
            WHERE name=%s OR last_name=%s OR email=%s OR phone_number=%s;
            """, (name, last_name, email, phone_number))
    return cur.fetchone()

command = input("Что нужно сделать? Введите help для справки по программе: ")
if command == "help".lower():
    print("""
    Список команд:
    deletetable - удаляет таблицы БД
    create - создаёт таблицы БД
    addclient - добавляет информацию о клиенте в БД
    addnum - добавляет телефонный номер клиента в БД
    updatedata - обновляет имя, фамилию и имейл клиента в БД
    updatenum - обновляет телефонный номер клиента в БД
    deletenum - удаляет телефонный номер клиента в БД
    deleteclient - удаляет ВСЮ информацию о клиенте в БД
    getinfo - получение информации о клиенте в БД(Должен быть введён хотя бы один параметр)
    """)

with psycopg2.connect(database="PyDB", user="postgres", password="7942") as conn:
    with conn.cursor() as cur:
        if command == "deletetable".lower():
            delete_tables(cur)

        if command == "create".lower():
            create_tables(cur)

        elif command == "addclient".lower():
            name = str(input("Введите имя: "))
            last_name = str(input("Введите фамилию: "))
            email = str(input("Введите имейл: "))
            print(add_client(cur, name, last_name, email))

        elif command == "addnum".lower():
            phone_number = int(input("Введите телефонный номер: "))
            client_id = int(input("Введите id клиента: "))
            print(add_phone_number(cur, phone_number, client_id))

        elif command == "updatedata".lower():
            name = str(input("Введите имя: "))
            last_name = str(input("Введите фамилию: "))
            email = str(input("Введите имейл: "))
            id = int(input("Введите id клиента: "))
            print(update_data(cur, name, last_name, email, id))

        elif command == "updatenum".lower():
            phone_number = int(input("Введите телефонный номер: "))
            id = int(input("Введите id номера: "))
            print(update_phone_number(cur, phone_number, id))

        elif command == "deletenum".lower():
            id = int(input("Введите id номера: "))
            delete_phone_number(cur, id)

        elif command == "deleteclient".lower():
            id = int(input("Введите id клиента: "))
            delete_client_info(cur, id)

        elif command == "getinfo".lower():
            name = str(input("Введите имя(или пропустите): "))
            last_name = str(input("Введите фамилию(или пропустите): "))
            email = str(input("Введите имейл(или пропустите): "))
            phone_number = int(input("Введите телефонный номер(или введите '0' для пропуска): "))
            if phone_number == 0:
                phone_number = None
            print(get_client_info(cur, name, last_name, email, phone_number))