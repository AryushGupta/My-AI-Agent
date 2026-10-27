import pandas as pd
from falkordb import FalkorDB
import math , random , string

# connect to the FalkorDB instance running in Docker
db = FalkorDB(host="localhost", port=6379)

# select a graph by name
graph = db.select_graph("research_graph")

# optional: delete the old graph so re-running the script doesn't create duplicates
try:
    graph.delete()
except Exception:
    pass

# global variable
graph = db.select_graph("research_graph")

# Load the Excel file
df = pd.read_excel("../Dataset/research_papers_data.xlsx")

CHARACTERS = string.ascii_letters + string.digits

def create_paper_node(data: dict):
    query = """
        CREATE (p:Paper {
            id: $id,
            title: $title,
            institution: $institution,
            keywords: $keywords,
            year: $year,
            paper_url: $paper_url,
            references: $references
        })
        """

    graph.query(query, {
        "id": data["Paper_ID"],
        "title": data["Title"],
        "institution": data["Institution"],
        "keywords": data["Keywords"].split(';'),
        "year": int(data["Year"]),
        "paper_url": data["Paper_URL"],
        "references": (lambda x: x.split(';') if pd.notna(x) else [])(data["References"])
    })
    year_node(data['Year'],data["Paper_ID"])
    author_name(data)
    create_institution_node(data['Institution'],data['Paper_ID'])
    create_field_node(data,data['Paper_ID'])

def author_name(data: dict):
    authors = data["Authors"].split(';')
    for author_name in authors:
        create_author_node(author_name.strip().casefold(),data['Institution'], data['Paper_ID'])


def create_author_node(author_name: str, institution_name: str, paper_id: str):
    # Check whether the author node exists
    query = """
        MATCH (a:Author {author: $author, institution: $institution})
        RETURN count(a) AS total
    """
    result = graph.query(query, {
        "author": author_name,
        "institution": institution_name
    })

    # Create the author node if it doesn't exist
    if result.result_set[0][0] == 0:
        query = """
            CREATE (a:Author {
                id: $id,
                author: $author,
                email: $email,
                institution: $institution
            })
        """
        graph.query(query, {
            "id": ''.join(random.choices(CHARACTERS, k=12)),
            "author": author_name,
            "email": f"{author_name.replace(' ', '').lower()}@gmail.com",
            "institution": institution_name
        })

    # Connect the author to the current paper, regardless of
    # whether the author node was newly created or already existed
    query = """
        MATCH (p:Paper {id: $paper_id})
        MATCH (a:Author {author: $author, institution: $institution})
        MERGE (p)-[:WRITTEN_BY]->(a)
    """
    graph.query(query, {
        "paper_id": paper_id,
        "author": author_name,
        "institution": institution_name
    })


def create_institution_node(institution_name: str, paper_id: str):

    # Check whether the institution node already exists
    query = """
        MATCH (i:Institution {institution: $institution})
        RETURN count(i) AS total
    """
    result = graph.query(query, {
        "institution": institution_name
    })

    # Create the institution node if it doesn't exist
    if result.result_set[0][0] == 0:
        query = """
            CREATE (i:Institution {
                institution: $institution
            })
        """
        graph.query(query, {
            "institution": institution_name
        })

    # Connect the institution to the current paper
    query = """
        MATCH (p:Paper {id: $paper_id})
        MATCH (i:Institution {institution: $institution})
        MERGE (p)-[:PUBLISHING_INSTITUTION]->(i)
    """
    graph.query(query, {
        "paper_id": paper_id,
        "institution": institution_name
    })


def create_field_node(data: dict, paper_id: str):

    # Check whether the Field node exists
    query = """
        MATCH (f:Field {field: $field, subject: $subject})
        RETURN count(f) AS total
    """
    result = graph.query(query, {
        "field": data["Field"],
        "subject": data["Subject"]
    })

    # Create the node if it doesn't exist
    if result.result_set[0][0] == 0:
        query = """
            CREATE (f:Field {
                field: $field,
                subject: $subject
            })
        """
        graph.query(query, {
            "field": data["Field"],
            "subject": data["Subject"]
        })

    # Connect the Paper node to the Field node
    query = """
        MATCH (p:Paper {id: $paper_id})
        MATCH (f:Field {field: $field, subject: $subject})
        MERGE (p)-[:BELONGS_TO]->(f)
    """
    graph.query(query, {
        "paper_id": paper_id,
        "field": data["Field"],
        "subject": data["Subject"]
    })


def year_node(year: int, paper_id: str):

    # Check whether the Year node exists
    query = """
        MATCH (y:Year {year: $year})
        RETURN count(y) AS total
    """
    result = graph.query(query, {
        "year": int(year)
    })

    # Create the node if it doesn't exist
    if result.result_set[0][0] == 0:
        query = """
            CREATE (y:Year {year: $year})
        """
        graph.query(query, {
            "year": int(year)
        })

    # Connect the Paper node to the Year node
    query = """
        MATCH (p:Paper {id: $paper_id})
        MATCH (y:Year {year: $year})
        MERGE (p)-[:PUBLISHED_IN_YEAR]->(y)
    """
    graph.query(query, {
        "paper_id": paper_id,
        "year": int(year)
    })

for index, row in df.iterrows():
    create_paper_node(row.to_dict())