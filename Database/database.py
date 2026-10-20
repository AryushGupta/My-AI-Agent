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

graph = db.select_graph("research_graph")

# Load the Excel file
df = pd.read_excel("./research_papers_graph_dataset.xlsx")


def create_paper_node(content: dict):
    query = """
        CREATE (p:Paper {
            id: $id,
            title: $title,
            institution: $institution,
            field: $field,
            subject: $subject,
            keywords: $keywords,
            year: $year,
            paper_url: $paper_url,
            references: $references
        })
        """

    graph.query(query, {
        "id": content["Paper_ID"],
        "title": content["Title"],
        "institution": content["Institution"],
        "field": content["Field"],
        "subject": content["Subject"],
        "keywords": content["Keywords"].split(';'),
        "year": int(content["Year"]),
        "paper_url": content["Paper_URL"],
        "references": str(content["References"])
    })

# as papers have multiple author names , we need to create a separate node for each if it doesn't exist


def author_name(content: dict):
    authors = content["Authors"].split(';')
    for author in authors:
        create_author_node(author)


def author_node_exists(author_name: str) -> bool:
    query = f"""
    MATCH (a:Author {{author: $author_name}})
    RETURN count(a) AS total
    """
    result = graph.query(query, {"author_name": author_name})
    return result.result_set[0][0] > 0


def create_author_node(author_name: str):
    if not author_node_exists(author_name=author_name):
        query = """
            CREATE (a:Author {
                author: $author
            })
            """
        graph.query(query, {
            "author": author_name
        })


# Iterate and print row by row
for index, row in df.iterrows():
    # Convert the row to a dictionary or list to print it cleanly
    create_paper_node(row.to_dict())
    print(f"Row {index}: {row.to_dict()}")
