
SHINY_DIR = "data/shiny"
message = "Spotkales shiny Falsafafinks!"

with open(SHINY_DIR, "r") as file:
    while True:
        val = file.readline()

                    
        val = val.strip()
        print(val)           
        if not val or val == " ":
            print("booho")
            break
        elif val in message and val != " ":
            print("found exclusice pokemon: |", val, "| ")
            break            




