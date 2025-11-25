import mysql.connector
from mysql.connector import Error



def pripojeni_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tadeasvlcek1",
            database="task_manager"
        )
        if connection.is_connected():
            print("Připojeno k MySQL ✓")
            return connection
    except Error as e:
        print(f"Chyba při připojení k MySQL: {e}")
        return None

def pridat_ukol():
    conn = pripojeni_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("USE task_manager")

    nazev = input("Zadejte název úkolu: ").strip()
    popis = input("Zadejte popis úkolu: ").strip()

    if nazev == "" or popis == "":
        print("Název i popis jsou povinné.")
        return

    sql = "INSERT INTO tasks (nazev, popis) VALUES (%s, %s)"
    cursor.execute(sql, (nazev, popis))
    conn.commit()

    print("Úkol byl úspěšně přidán ✓")

    cursor.close()
    conn.close()

def zobrazit_ukoly():
    conn = pripojeni_db()
    if conn is None:
        return
    cursor = conn.cursor(dictionary=True)
    cursor.execute("USE task_manager")

    print("\nZvolte filtr:")
    print("1 Vše")
    print("2 Pouze Nezahájeno")
    print("3 Pouze Probíhá")
    print("4 Pouze Hotovo")

    volba = input("Vyber: ")

    if volba == "1":
        cursor.execute("SELECT * FROM tasks")
    elif volba == "2":
        cursor.execute("SELECT * FROM tasks WHERE stav = 'nezahájeno'")
    elif volba == "3":
        cursor.execute("SELECT * FROM tasks WHERE stav = 'probíhá'")
    elif volba == "4":
        cursor.execute("SELECT * FROM tasks WHERE stav = 'hotovo'")
    else:
        print("Neplatná volba")
        return

    ukoly = cursor.fetchall()

    if not ukoly:
        print("Žádné úkoly nenalezeny.")
    else:
        print("\n--- Seznam úkolů ---")
        for u in ukoly:
            print(f"{u['id']} | {u['nazev']} | {u['stav']} | {u['datum_vytvoreni']}")
            print(f"Popis: {u['popis']}")
            print("------------------------")

    cursor.close()
    conn.close()

def aktualizovat_ukol():
    conn = pripojeni_db()
    if conn is None:
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("USE task_manager")

    cursor.execute("SELECT id, nazev, stav FROM tasks")
    ukoly = cursor.fetchall()

    if not ukoly:
        print("Žádné úkoly nejsou v databázi.")
        return

    print("\n--- Úkoly ---")
    valid_ids = [] 

    for u in ukoly:
        print(f"{u['id']} – {u['nazev']} (stav: {u['stav']})")
        valid_ids.append(u['id'])

    
    while True:
        try:
            id_ukolu = int(input("Zadejte ID úkolu pro změnu stavu: "))
            if id_ukolu in valid_ids:
                break
            else:
                print("Toto ID není v seznamu úkolů. Zkuste znovu.")
        except:
            print("ID musí být číslo.")

    print("\nNový stav:")
    print("1 – Probíhá")
    print("2 – Hotovo")
    print("3 – Nezahájeno")

    volba = input("Vyber: ")

    if volba == "1":
        novy = "probíhá"
    elif volba == "2":
        novy = "hotovo"
    elif volba == "3":
        novy = "nezahájeno"
    else:
        print("Neplatná volba")
        return

    sql = "UPDATE tasks SET stav = %s WHERE id = %s"
    cursor.execute(sql, (novy, id_ukolu))
    conn.commit()

    print("Stav úkolu byl změněn ✓")

    cursor.close()
    conn.close()



def odstranit_ukol():
    conn = pripojeni_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("USE task_manager")

    try:
        id_ukolu = int(input("Zadejte ID úkolu pro odstranění: "))
    except:
        print("ID musí být číslo.")
        return

    cursor.execute("DELETE FROM tasks WHERE id = %s", (id_ukolu,))
    conn.commit()

    if cursor.rowcount == 0:
        print("Úkol s tímto ID nebyl nalezen.")
    else:
        print("Úkol byl odstraněn ✓")

    cursor.close()
    conn.close()



def hlavni_menu():
   
    while True:
        print("\n--- Hlavní menu ---")
        print("1 - Přidat úkol")
        print("2 - Zobrazit úkoly")
        print("3 - Aktualizovat úkol")
        print("4 - Odstranit úkol")
        print("5 - Konec")

        volba = input("Vyber možnost: ")

        if volba == "1":
            pridat_ukol()

        elif volba == "2":
            zobrazit_ukoly()

        elif volba == "3":
            aktualizovat_ukol()

        elif volba == "4":
            odstranit_ukol()

        elif volba == "5":
            print("Program ukončen.")
            break

        else:
            print("Neplatná volba. Zkuste to znovu.")


hlavni_menu()
