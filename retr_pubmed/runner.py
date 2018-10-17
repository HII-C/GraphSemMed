from getpass import getpass
from pubmed import PubMed

pw = getpass()
db_param = {'user': 'root', 'db': 'pubmed',
            'host': 'db01.healthcreek.org', 'password': pw}
example = PubMed(db_param)

schema = "(PMID CHAR(12), pubtype CHAR(12))"
example.new_table('pmid_filter', schema)

pubmed_prog = 1
while pubmed_prog < 928:
    example.file_from_ftp(pubmed_prog)
    example.write_to_sql('pmid_filter')
    print(pubmed_prog)
    pubmed_prog += 1
