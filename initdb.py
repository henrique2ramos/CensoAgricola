import psycopg2
from psycopg2 import OperationalError

DATABASE_NAME = "censo_agricola"


def create_tables():
    try:
        print("Conectando ao banco de dados...")

        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user="censoagro",
            password="censoagro",
            host="localhost",
            port="5434"
        )

        cursor = conn.cursor()

        with open('schema.sql', 'r') as f:
            print("Criando tabelas...")
            cursor.execute(f.read())

        conn.commit()
        print("Tabelas criadas com sucesso!")

    except OperationalError as e:
        print(f"The connection failed: {e}")

        if hasattr(e, 'pgcode'):
            print(f"PostgreSQL error code: {e.pgcode}")

    except psycopg2.Error as e:
        print(f"A general database error occurred: {e}")

    finally:
        print("Fechando a conexão com o banco de dados...")
        conn.close()
        print("Conexão fechada.")

if __name__ == "__main__":
    create_tables()