import mysql.connector
from mysql.connector import Error


def pripojeni_db(test=False):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tadeasvlcek1",
            database="task_manager_test" if test else "task_manager"
        )
        return connection
    except Error as e:
        print(f"Chyba při připojení k MySQL: {e}")
        return None


def vytvoreni_tabulky(test=False):
    conn = pripojeni_db(test)
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('nezahájeno', 'probíhá', 'hotovo') NOT NULL DEFAULT 'nezahájeno',
                datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Error as e:
        print(f"Chyba při vytváření tabulky: {e}")
    finally:
        cursor.close()
        conn.close()


def pridat_ukol(test=False):
    conn = pripojeni_db(test)
    if conn is None:
        return

    nazev = input("Zadej název úkolu: ").strip()
    popis = input("Zadej popis úkolu: ").strip()

    if not nazev or not popis:
        print("Úkol musí mít název i popis!")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        conn.commit()
        print("Úkol byl přidán ✓")
    except Error as e:
        print(f"Chyba při přidávání úkolu: {e}")
    finally:
        cursor.close()
        conn.close()


def zobrazit_ukoly(test=False):
    conn = pripojeni_db(test)
    if conn is None:
        return

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks ORDER BY id")
        ukoly = cursor.fetchall()

        if not ukoly:
            print("Žádné úkoly nenalezeny.")
            return

        for u in ukoly:
            print(f"{u['id']}: {u['nazev']} ({u['stav']}) – {u['popis']}")

    except Error as e:
        print(f"Chyba při načítání úkolů: {e}")
    finally:
        cursor.close()
        conn.close()


def aktualizovat_ukol(test=False):
    conn = pripojeni_db(test)
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM tasks")
        ids = [row[0] for row in cursor.fetchall()]

        if not ids:
            print("Žádné úkoly k aktualizaci.")
            return

        id_ukolu = input("Zadej ID úkolu k aktualizaci: ").strip()

        if not id_ukolu.isdigit() or int(id_ukolu) not in ids:
            print("Neplatné ID!")
            return

        print("1 - nezahájeno\n2 - probíhá\n3 - hotovo")
        volba = input("Vyber nový stav: ").strip()

        stavy = {"1": "nezahájeno", "2": "probíhá", "3": "hotovo"}

        if volba not in stavy:
            print("Neplatná volba stavu!")
            return

        cursor.execute("UPDATE tasks SET stav=%s WHERE id=%s", (stavy[volba], id_ukolu))
        conn.commit()

        print("Úkol aktualizován ✓")

    except Error as e:
        print(f"Chyba při aktualizaci: {e}")
    finally:
        cursor.close()
        conn.close()


def odstranit_ukol(test=False):
    conn = pripojeni_db(test)
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM tasks")
        ids = [row[0] for row in cursor.fetchall()]

        if not ids:
            print("Žádné úkoly k odstranění.")
            return

        id_ukolu = input("Zadej ID úkolu k odstranění: ").strip()

        if not id_ukolu.isdigit() or int(id_ukolu) not in ids:
            print("Neplatné ID!")
            return

        cursor.execute("DELETE FROM tasks WHERE id=%s", (id_ukolu,))
        conn.commit()

        print("Úkol byl odstraněn ✓")

    except Error as e:
        print(f"Chyba při odstraňování: {e}")
    finally:
        cursor.close()
        conn.close()


def hlavni_menu():
    vytvoreni_tabulky()
    while True:
        print("\n--- Hlavní menu ---")
        print("1 - Přidat úkol")
        print("2 - Zobrazit úkoly")
        print("3 - Aktualizovat úkol")
        print("4 - Odstranit úkol")
        print("5 - Konec")

        volba = input("Vyber možnost: ").strip()

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            aktualizovat_ukol()
        elif volba == "4":
            odstranit_ukol()
        elif volba == "5":
            print("Ukončuji program...")
            break
        else:
            print("Neplatná volba.")



if __name__ == "__main__":
    hlavni_menu()