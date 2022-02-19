
with open("extracted_sql.sql", "r") as f:
    with open("cleaned_sql2.sql", "a", newline="") as output:
        for line in f.readlines():
            if "page = 'P: " in line:
                output.write(line.replace("page = 'P: ", "page = '"))
            elif "page = 'P:" in line:
                output.write(line.replace("page = 'P:", "page = '"))

            elif ":'" in line:
                output.write(line.replace(":'", "'"))

            elif "page = 'P" in line:
                output.write(line.replace("page = 'P", "page = '"))

            elif "book = ';" in line:
                output.write(line.replace("book = ';", "book = '"))
            elif "book = '; " in line:
                output.write(line.replace("book = '; ", "book = '"))

            elif "book = ':" in line:
                output.write(line.replace("book = ':", "book = '"))
            elif "book = ': " in line:
                output.write(line.replace("book = ': ", "book = '"))

            elif "book = ''" in line:
                output.write(line.replace("book = ''", "book = NULL"))
            elif "page = ''" in line:
                output.write(line.replace("page = ''", "page = NULL"))

            elif "book = 'LIBER" in line:
                output.write(line.replace("book = 'LIBER", "book ='"))
