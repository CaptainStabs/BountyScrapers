from subprocess import call

with open("./tools/nums.txt", "r") as f:
    for line in f:
        call(f"dolt diff HPI multi-code-fix prices --summary --where=cms_certification_num='{line}'")
        
