import pytest
import mysql.connector


@pytest.fixture
def db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tadeasvlcek1",
        database="task_manager_test"
    )
    yield conn
    conn.commit()
    conn.close()


@pytest.fixture
def setup_tasks_table(db):
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS tasks")

    cursor.execute("""
        CREATE TABLE tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM('nezahájeno','probíhá','hotovo') NOT NULL DEFAULT 'nezahájeno',
            datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()
    cursor.close()

from upgraded_task_manager import pridat_ukol
import builtins


def test_pridat_ukol_ok(db, setup_tasks_table, monkeypatch):
    inputs = iter(["Testovací úkol", "Popis úkolu"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    pridat_ukol(test=True)

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE nazev='Testovací úkol'")
    result = cursor.fetchone()

    assert result is not None
    assert result["popis"] == "Popis úkolu"

def test_pridat_ukol_invalid_empty_fields(db, setup_tasks_table, monkeypatch):
    inputs = iter(["", ""])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    pridat_ukol(test=True)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    assert cursor.fetchone() is None

from upgraded_task_manager import aktualizovat_ukol
import builtins


def test_aktualizovat_ukol_ok(db, setup_tasks_table, monkeypatch):

    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (nazev, popis) VALUES ('A', 'B')")
    db.commit()

    cursor.execute("SELECT id FROM tasks WHERE nazev='A'")
    task_id = cursor.fetchone()[0]

    inputs = iter([str(task_id), "2"])  # 2 = hotovo
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    aktualizovat_ukol(test=True)

    cursor.execute("SELECT stav FROM tasks WHERE id=%s", (task_id,))
    stav = cursor.fetchone()[0]

    assert stav is not None


def test_aktualizovat_ukol_invalid_id(db, setup_tasks_table, monkeypatch):

    inputs = iter(["999", "1"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    aktualizovat_ukol(test=True)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    assert cursor.fetchall() == []

from upgraded_task_manager import odstranit_ukol
import builtins


def test_odstranit_ukol_ok(db, setup_tasks_table, monkeypatch):

    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (nazev, popis) VALUES ('Smazat', 'Popis')")
    db.commit()

    cursor.execute("SELECT id FROM tasks WHERE nazev='Smazat'")
    task_id = cursor.fetchone()[0]

    inputs = iter([str(task_id)])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    odstranit_ukol(test=True)

    cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
    assert cursor.fetchone() is not None


def test_odstranit_ukol_invalid_id(db, setup_tasks_table, monkeypatch):

    inputs = iter(["999"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    odstranit_ukol(test=True)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    assert cursor.fetchall() == []