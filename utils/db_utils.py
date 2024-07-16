import sqlite3
import uuid

def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ Create the documents table """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS documents (
        uuid text PRIMARY KEY,
        file_name text NOT NULL,
        has_embeddings boolean NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_document(conn, document):
    """ Insert a new document into the documents table """
    sql = ''' INSERT INTO documents(uuid, file_name, has_embeddings)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, document)
    conn.commit()
    return cur.lastrowid

def get_document_by_uuid(conn, uuid):
    """ Query document by uuid """
    cur = conn.cursor()
    cur.execute("SELECT * FROM documents WHERE uuid=?", (uuid,))
    rows = cur.fetchall()
    return rows

def get_all_documents(conn):
    """ Query all documents """
    cur = conn.cursor()
    cur.execute("SELECT * FROM documents")
    rows = cur.fetchall()
    return rows

def delete_all_documents(conn):
    """ Delete all entries in the documents table """
    sql = 'DELETE FROM documents'
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Example usage
if __name__ == '__main__':
    database = "documents.db"

    # Create a database connection
    conn = create_connection(database)
    with conn:
        # Create table
        create_table(conn)

        # Insert a document
        doc = (str(uuid.uuid4()), 'STAT TB Chapt 1.pdf', True)
        insert_document(conn, doc)

        # Query the document
        print(get_document_by_uuid(conn, doc[0]))

        # Query all documents
        print(get_all_documents(conn))
