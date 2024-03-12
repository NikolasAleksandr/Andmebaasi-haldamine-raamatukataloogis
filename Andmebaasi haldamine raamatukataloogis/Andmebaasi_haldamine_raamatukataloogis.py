import tkinter as tk
from tkinter import messagebox
from sqlite3 import *
from sqlite3 import Error
import os


def create_connection(path: str):
    """Ühendus andmebaasiga"""
    connection = None
    try:
        if not os.path.exists("database"):
            os.mkdir("database")
        connection = connect(os.path.join("database", path))
        print("Ühendus on edukalt tehtud")
    except Error as e:
        print(f"Tekkis viga: '{e}'")
    return connection


def create_tables(connection):
    """Määratle tabelite struktuur"""
    try:
        cursor = connection.cursor()
        # Tabel Autorid
        cursor.execute('''CREATE TABLE IF NOT EXISTS Autorid (
                            autor_id INTEGER PRIMARY KEY,
                            autor_nimi TEXT NOT NULL,
                            sünnikuupäev DATE
                        )''')

        # Tabel Žanrid
        cursor.execute('''CREATE TABLE IF NOT EXISTS Žanrid (
                            žanr_id INTEGER PRIMARY KEY,
                            žanri_nimi TEXT NOT NULL
                        )''')

        # Tabel Raamatud
        cursor.execute('''CREATE TABLE IF NOT EXISTS Raamatud (
                            raamat_id INTEGER PRIMARY KEY,
                            pealkiri TEXT NOT NULL,
                            väljaandmise_kuupäev DATE,
                            autor_id INTEGER,
                            žanr_id INTEGER,
                            FOREIGN KEY (autor_id) REFERENCES Autorid(autor_id),
                            FOREIGN KEY (žanr_id) REFERENCES Žanrid(žanr_id)
                        )''')

        connection.commit()
    except Error as e:
        print(f"Viga tabelite loomisel: {e}")

def insert_data(connection, table, data):
    """Sisesta andmed tabelisse"""
    try:
        cursor = connection.cursor()
        placeholders = ', '.join(['?'] * len(data))
        cursor.execute(f"INSERT INTO {table} VALUES ({placeholders})", data)
        connection.commit()
        print("Andmed on lisatud")
    except Error as e:
        print(f"Viga andmete lisamisel: {e}")

def fetch_data(connection, query):
    """Päring andmete kuvamiseks"""
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(f"Viga andmete pärimisel: {e}")

def update_data(connection, query):
    """Andmete muutmine"""
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Andmed on edukalt uuendatud")
    except Error as e:
        print(f"Viga andmete uuendamisel: {e}")

def delete_data(connection, query):
    """Andmete kustutamine"""
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Andmed on edukalt kustutatud")
    except Error as e:
        print(f"Viga andmete kustutamisel: {e}")

def drop_table(connection, table):
    """Tabeli kustutamine"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        connection.commit()
        print(f"Tabel '{table}' on edukalt kustutatud")
    except Error as e:
        print(f"Viga tabeli kustutamisel: {e}")

def display_data():
    """Kuva andmed"""
    rows = fetch_data(connection, "SELECT * FROM Raamatud")

    if rows:
        for row in rows:
            print(row)
    else:
        print("Andmeid ei leitud")

def add_data():
    """Lisa andmed"""
    insert_data(connection, "Raamatud", (None, "Uus raamat", "2024-03-13", 1, 2))

def close_connection():
    """Sulge andmebaasi ühendus"""
    if connection:
        connection.close()
        print("Ühendus on sulgetud"
              )
# Andmete lisamine 
    insert_data(connection, "Autorid", (None, "Jaan Kross", "1920-02-19"))
    insert_data(connection, "Autorid", (None, "Oskar Luts", "1887-01-07"))
    insert_data(connection, "Žanrid", (None, "Romantika"))
    insert_data(connection, "Raamatud", (None, "Kolme katku vahel", "1970-01-01", 1, 1))
    insert_data(connection, "Raamatud", (None, "Kevade", "1912-01-01", 2, 2))

    fetch_data(connection, "SELECT * FROM Autorid")
    fetch_data(connection, "SELECT * FROM Žanrid")
    fetch_data(connection, "SELECT * FROM Raamatud")
if __name__ == "__main__":
  
  
    database = "raamatukogu.db"
    connection = create_connection(database)
    create_tables(connection)

root = tk.Tk()
root.title("Raamatukogu andmehaldus")

display_button = tk.Button(root, text="Kuva andmed", command=display_data, bg="lightblue")
display_button.pack(pady=10)

add_button = tk.Button(root, text="Lisa uus raamat", command=add_data, bg="lightgreen")
add_button.pack(pady=10)

close_button = tk.Button(root, text="Sulge ühendus", command=close_connection, bg="salmon")
close_button.pack(pady=10)

root.mainloop()