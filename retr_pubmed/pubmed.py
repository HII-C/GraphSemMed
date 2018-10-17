import os
from ftplib import FTP
import xml.etree.ElementTree as ET

from util.db_util import DatabaseHandle
from util.mesh_util import MeshOfInterest

import getpass
import gzip


class PubMed:
    pubmed_db: DatabaseHandle = None
    pubmed_prog: int = None
    pmid_d: MeshOfInterest = MeshOfInterest()
    useful_articles = list()

    def __init__(self, db_param, pubmed_prog=1):
        self.pubmed_db = DatabaseHandle(**db_param)
        self.pubmed_prog = pubmed_prog
        with open("pubmed.prog", 'w+') as handle:
            handle.write(f'{self.pubmed_prog}\n')
        print(f"Pubmed progress set to {pubmed_prog}")

    def new_table(self, table_name, schema):
        exec_str = f"DROP TABLE IF EXISTS {table_name}"
        self.pubmed_db.cursor.execute(exec_str)
        exec_str = f"CREATE TABLE {table_name} {schema}"
        self.pubmed_db.cursor.execute(exec_str)
        self.pubmed_db.connection.commit()

    def file_from_ftp(self, thread_prog_num):
        server_name = 'ftp.ncbi.nlm.nih.gov'
        dir_ = '/pubmed/baseline/'
        mesh_ids = self.pmid_d.get_mesh_ids()

        file_num = str(thread_prog_num)
        while len(file_num) < 4:
            file_num = f'0{file_num}'

        filename = f'pubmed18n{file_num}.xml'

        ftp = FTP(server_name)
        ftp.login('anonymous', 'austinmichne@gmail.com')
        ftp.cwd(dir_)
        ftp.retrbinary(f'RETR {filename}.gz', open(filename, 'wb+').write)

        xml_file = gzip.open(filename).read()
        root = ET.fromstring(xml_file)

        for ele_ in root.iter('PubmedArticle'):
            useful_flag = False
            useful_ui = None
            useful_ui_list = list()
            for ui_ in ele_.iter('PublicationType'):
                if ui_.attrib['UI'] in mesh_ids:
                    useful_flag = True
                    useful_ui = ui_.attrib['UI']
                    break
            if useful_flag:
                for x in ele_.iter('PublicationType'):
                    useful_ui_list.append(x.attrib['UI'])
                for x in ele_.iter('PMID'):
                    pmid = x.text
                self.useful_articles.append(tuple([pmid, useful_ui]))
        os.remove(f'{filename}')

    def write_to_sql(self, table):
        exec_str = f"INSERT INTO {table} VALUES (%s,%s)"
        self.pubmed_db.cursor.executemany(exec_str, self.useful_articles)
        self.pubmed_db.connection.commit()
        self.useful_articles[:] = []
