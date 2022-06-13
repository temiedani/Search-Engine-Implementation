def get_documents():
    with open ('CISI.ALL', 'r') as f:
        lines = ""
        for l in f.readlines():
            lines += "\n" + l.strip() if l.startswith(".") else " " + l.strip()
    lines = lines.lstrip("\n").split("\n")
    #n = 5
    #for l in lines[:n]:
     #   print(l)
    doc_set = {}
    doc_id = ""
    doc_text = ""
    for l in lines:
        if l.startswith(".I"):
            doc_id = l.split(" ")[1].strip()
        elif l.startswith(".X"):
            doc_set[doc_id] = doc_text.lstrip(" ")
            doc_id = ""
            doc_text = ""
        else:
            doc_text += l.strip()[3:] + " " # The first 3 characters of a line can be ignored.
    # print(f"Number of documents = {len(doc_set)}" + ".\n")
    # print(doc_set["3"])
    return doc_set, doc_id, doc_text


def get_query():
    with open('CISI.QRY') as f:
        lines = ""
        for l in f.readlines():
            lines += "\n" + l.strip() if l.startswith(".") else " " + l.strip()
        lines = lines.lstrip("\n").split("\n")
    qry_set = {}
    qry_id = ""
    for l in lines:
        if l.startswith(".I"):
            qry_id = l.split(" ")[1].strip()
        elif l.startswith(".W"):
            qry_set[qry_id] = l.strip()[3:]
            qry_id = ""
    # Print something to see the dictionary structure, etc.
    # print(f"Number of queries = {len(qry_set)}" + ".\n")
    # print(qry_set["3"])
    return qry_set, qry_id

def get_ground_truth():
    rel_set = {}
    with open('CISI.REL') as f:
        for l in f.readlines():
            qry_id = l.lstrip(" ").strip("\n").split("\t")[0].split(" ")[0]
            doc_id = l.lstrip(" ").strip("\n").split("\t")[0].split(" ")[-1]
            if qry_id in rel_set:
                rel_set[qry_id].append(doc_id)
            else:
                rel_set[qry_id] = []
                rel_set[qry_id].append(doc_id)
            # if qry_id == "7":
            #     print(l.strip("\n"))

    # Print something to see the dictionary structure, etc.
    # print(f"\nNumber of mappings = {len(rel_set)}" + ".\n")
    # print(rel_set["7"]) # note that the dictionary indexes are strings, not numbers.
    return rel_set
