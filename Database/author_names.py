import pandas as pd
import xlsxwriter , random , string

df = pd.read_excel("../Dataset/research_papers_data.xlsx")

author_details_workbook = xlsxwriter.Workbook('../Dataset/author_names.xlsx')
author_worksheet = author_details_workbook.add_worksheet()

CHARACTERS = string.ascii_letters + string.digits

# dictionary schema
# "author-institution" : {
#         "ID" : "-",
#         "name" : "-",
#         "institution" : "-",
#         "email_id" : "-"
#  }

authors_data = {} 

def add_author(data:dict):
    authors = data['Authors'].split(';')
    institution = data['Institution']

    for author in authors:
        key = f"{author}-{institution}"

        if key not in authors_data:
            authors_data.update({
                key: 
                    {
                    "ID": ''.join(random.choices(CHARACTERS, k=12)),
                    "name": author,
                    "institution": institution,
                    "email_id": f"{author.replace(' ','').lower()}.@gmail.com"
                    }
                })

for index, row in df.iterrows():
    add_author(row)

# creating the excel sheet
headers = ["ID","Author","Email","Institution"]

for col, header in enumerate(headers):
    author_worksheet.write(0, col , header)

for row, (key, value) in enumerate(authors_data.items(), start=1):
    author_worksheet.write(row,0,value["ID"])
    author_worksheet.write(row,1,value["name"])
    author_worksheet.write(row,2,value["email_id"])
    author_worksheet.write(row,3,value["institution"])

author_details_workbook.close()