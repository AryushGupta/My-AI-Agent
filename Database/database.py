import pandas as pd
from falkordb import FalkorDB

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
df = pd.read_excel("./Dataset/research_papers_data.xlsx")


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
        "references": str(data["References"])
    })

# as papers have multiple author names , we need to create a separate node for each author if it doesn't exist

def author_name(data: dict):
    authors = data["Authors"].split(';')
    for author in authors:
        create_author_node(author)


def create_author_node(data: str):
    # check if node exist or not
    query = f"""
    MATCH (a:Author {{author: $author}})
    RETURN count(a) AS total
    """
    result = graph.query(query, {"author": data})
    if result.result_set[0][0] > 0:
        print(f"{data} node exist")
    else:
        query = """
            CREATE (a:Author {
                author: $author
            })
            """
        graph.query(query, {
            "author": data
        })
        print(f"{data} author node created")


def create_institution_node(data: str):
    # check if node already exist or not
    query = f"""
    MATCH (i:Institution {{institution: $institution}})
    RETURN count(i) AS total
    """
    result = graph.query(query, {"institution": data})
    if result.result_set[0][0] > 0:
        print(f"{data} node exist")
    else:
        query = """
            CREATE (i:Institution {
                institution: $institution
            })
            """
        graph.query(query, {
            "institution": data
        })
        print(f"{data} node created.")

def create_field_node(data:dict):
    # check if node already exist or not
    print(data['Field'] , data['Subject'])
    query = f"""
    MATCH (f:field {{field: $field, subject: $subject}})
    RETURN count(f) AS total
    """
    result = graph.query(query, {"field": data["Field"],
                                "subject" : data["Subject"]})
    if result.result_set[0][0] > 0:
        print(f"{data} node exist")
    else:
        query = """
            CREATE (f:Field {
                field: $field
            })
            """
        graph.query(query, {
            "field": data['Field'],
            "subject" : data['Subject']
        })
        print(f"{data} node created.")

def create_references_node(data:dict):
    return

# Iterate and print row by row
for index, row in df.iterrows():
    # Convert the row to a dictionary or list to print it cleanly
    # create_paper_node(row.to_dict())
    # print(f"Row {index}: {row.to_dict()}")
    create_field_node(row.to_dict())
    break
