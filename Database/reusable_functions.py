# def node_exists(label: str, node_id: str) -> bool:
#     query = f"""
#     MATCH (n:{label} {{id: $node_id}})
#     RETURN count(n) AS total
#     """
#     result = graph.query(query, {"node_id": node_id})
#     return result.result_set[0][0] > 0


# def create_node(content: dict):
#     query = """
#     CREATE (p:Paper {
#         id: $id,
#         title: $title,
#         authors: $authors,
#         institution: $institution,
#         field: $field,
#         subject: $subject,
#         keywords: $keywords,
#         year: $year,
#         paper_url: $paper_url,
#         references: $references
#     })
#     """

#     graph.query(query, {
#         "id": content["Paper_ID"],
#         "title": content["Title"],
#         "authors": content["Authors"].split(';'),
#         "institution": content["Institution"],
#         "field": content["Field"],
#         "subject": content["Subject"],
#         "keywords": content["Keywords"].split(';'),
#         "year": int(content["Year"]),
#         "paper_url": content["Paper_URL"],
#         "references": str(content["References"])
#     })

#     print("Node created successfully!")
