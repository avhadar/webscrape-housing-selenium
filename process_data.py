sources = {} # source: startpage
sources["detoatepentrutoti"] = [ "https://www.detoatepentrutoti.ro/cautare?domeniu=Imobiliare&categoria=Imobile&rubrica=&tranzactie=1&judet=31&localitate=&sortare_data=desc&keyword=cuvant+cheie&filtru=aplicat&startPage=", "realestate.csv", "realestate-clean.csv"]

# test files
# infile = open("realestate-short-allpages.csv", "r", encoding = "utf8")
# outfile = open("realestate-short-clean.csv", "w", encoding = "utf8")

infile = open("realestate.csv", "r", encoding = "utf8") # raw data
outfile = open("realestate-clean.csv", "w", encoding = "utf8") # clean data

header_fields = ["Link", "Price", "Ad_date", "Zona", "Amplasare", "Suprafata", "Etaj", "Confort", "Bai", "Balcoane", "Optiuni"]

output_data = {}
count = 0

print("Reading input file...")

for line in infile:
    # print(line)
    fields = line.strip().split("|") # column separator is "|"
    # print(fields)
    
    output_data[count] = { "Link": fields[0], "Ad_date": fields[2] }
    
    # get price - from fields[1]
    start_pos_price = fields[1].find("Pret: ")
    end_idx1_price = fields[1].find(" pret total")
    end_idx2_price = fields[1].find(" / buc.")
    # the last tag might not be available -> check if found
    if end_idx1_price != -1:
        end_pos_price = end_idx1_price
    elif end_idx2_price != -1:
        end_pos_price = end_idx2_price
    else:
        end_pos_price = -1
    # get price data
    if end_pos_price != -1:
        price = fields[1][(start_pos_price+6) : end_pos_price]
    else:
        price = fields[1][(start_pos_price+6) : ]
    # print(price)
    output_data[count]["Price"] = price
    
    # get details - from fields[3]
    details = fields[3].split("·")
    # print(details)
    details = [elem.strip().split(": ") for elem in details if elem != '']
    # print(details)
    
    others = []
    for detail in details:
        if len(detail) == 2:
            key = detail[0]
            if key in header_fields:
                output_data[count][key] = detail[1]
            else:
                print("Key unknown: " + key)
        else:
            others.append(detail[0])
    
    output_data[count]["Other"] = "-".join(others)
    count += 1

infile.close()
print("Finished processing input file")

# print(output_data)

print("Generating output file...")
# write clean data to file
# write header
header_fields.append("Other")
# print(header_fields)
header = ";".join(header_fields)
outfile.write(header + "\n")
# write line entries
for elem in output_data:
    print("processing element " + str(elem))
    # print(output_data[elem])
    # Note the syntax: (x if  cond else y for x in listx) - vs - (x for x in listx if cond)
    line = ";".join(output_data[elem][tag] if tag in output_data[elem] else '' for tag in header_fields) 
    # column separator is ";"
    # print(line)
    outfile.write(line + "\n")
# close output file
outfile.close()
print("Processing finished")

