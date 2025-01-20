import re
import glob

# Wzorzec (Regex) do wyciągnięcia:
# (godzina) (numer_testu) of (coś) OK created sql table model (nazwa_tabeli) [OK in (czas)]
pattern = re.compile(
    r'^(\d{2}:\d{2}:\d{2})\s+(\d+)\s+of\s+\d+\s+OK\s+created\s+sql\s+table\s+model\s+([^\s]+).*?\[OK in ([\d.]+s)\]'
)

# Jeśli trzy logi masz w osobnych plikach np. log1.txt, log2.txt, log3.txt,
# możesz je czytać pojedynczo lub użyć wzorca "log*.txt" i w pętli przechodzić po wszystkich
files = ["tbd2b_dbt-run_exec1.txt", "tbd2b_dbt-run_exec2.txt", "tbd2b_dbt-run_exec5.txt"]

# Możesz też użyć glob, jeśli pliki są nazwane np. log1.txt, log2.txt itd.:
# files = glob.glob("log*.txt")

# Wypisujemy nagłówek CSV
print("plik,numer_testu,nazwa_tabeli,czas_wykonania")

for f_name in files:
    with open(f_name, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            match = pattern.search(line)
            if match:
                # match.group(1) -> czas (HH:MM:SS) z loga, jeśli potrzebujesz
                test_number = match.group(2)
                table_name = match.group(3)
                duration = match.group(4)
                
                # Możemy też wyciągnąć sam numer logu (f_name), by wiedzieć, z którego logu
                # pochodzi wpis.
                print(f"{f_name},{test_number},{table_name},{duration}")

