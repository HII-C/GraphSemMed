from util.db_util import *


class DerivedGraphSemMed:
    def __init__(self):
        self.handles = PmidKnowledgeHandles()

    def create_pmid_filter(self, pubmed, semmed, tbl):
        pubmed_source_str = f'pubmed.{pubmed}'
        semmed_source_str = f'semmed.{semmed}'
        derived_tbl_str = f'derived.{tbl}'
        pmid = 'pmid'
        create_str = '''(PMID VARCHAR(12), PUBTYPE VARCHAR(12), PREDICATION_ID UNSIGNED INT NOT NULL, SENTENCE_ID UNSIGNED INT NOT NULL,
        PREDICATE VARCHAR(50), SUBJECT_CUI VARCHAR(255), SUBJECT_NAME VARCHAR(999), SUBJECT_SEMTYPE VARCHAR(50), 
        SUBJECT_NOVELTY TINYINT UNSIGNED, OBJECT_CUI VARCHAR(255), OBJECT_NAME VARCHAR(999), OBJECT_SEMTYPE VARCHAR(50), 
        OBJECT_NOVELTY TINYINT UNSIGNED'''
        exec_str = f'''CREATE TABLE 
                            {derived_tbl_str}{create_str} 
                        FROM 
                            {pubmed_source_str}
                        INNER JOIN
                            {semmed_source_str}
                        ON
                            {pubmed_source_str}.{pmid} = {semmed_source_str}.{pmid}'''
        self.handles.pubmed.cursor.execute(exec_str)
        self.handles.pubmed.connection.commit()


if __name__ == '__main__':
    usr = 'greenes2018'
    pw = getpass()
    pubmed_db = 'pubmed'
    pubmed_host = 'db01.healthcreek.org'
    semmed_db = 'semmed'
    semmed_host = 'db01.healthcreek.org'
    der_db = 'derived'
    der_host = 'db01.healthcreek.org'

    dg_sem = DerivedGraphSemMed()
    dg_sem.handles.pubmed = DatabaseHandle(usr, pw, pubmed_db, pubmed_host)
    dg_sem.handles.semmed = DatabaseHandle(usr, pw, semmed_db, semmed_host)
    dg_sem.handles.derived = DatabaseHandle(usr, pw, der_db, der_host)

    dg_sem.create_pmid_filter('pmid_filter', 'PREDICATION', 'PMID_FILTER')

