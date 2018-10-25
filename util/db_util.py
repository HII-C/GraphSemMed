import MySQLdb as sql
import MySQLdb.connections as conns
from getpass import getpass
from dataclasses import dataclass

from neo4j import GraphDatabase


class DatabaseHandle:
    connection: conns.Connection = None
    cursor: conns.cursors.Cursor = None
    user: str = None
    host: str = None
    db: str = None

    def __init__(self, user, password, db, host):
        self.connection = sql.connect(
            user=user, password=password, db=db, host=host)
        self.cursor = self.connection.cursor()
        self.user = user
        self.host = host
        self.db = db


@dataclass
class PmidKnowledgeHandles:
    pubmed: DatabaseHandle
    semmed: DatabaseHandle
    derived: DatabaseHandle


class NeoHandle:
    driver = None
    session = None
    host: str = None
    user: str = None

    def __init__(self, host, user, password):
        bolt_url = f'bolt://{host}'
        self.driver = GraphDatabase.driver(bolt_url, auth=(user, password))
        self.host = host
        self.user = user
