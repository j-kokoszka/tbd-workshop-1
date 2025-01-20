import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Zakładamy, że masz 3 pliki logów:
log_files = ["tbd2b_dbt-run_exec1.txt", "tbd2b_dbt-run_exec2.txt", "tbd2b_dbt-run_exec5.txt"]

# 1. Struktura do przechowywania czasów: {plik: {numer_testu: [lista_czasów]}}
test_durations = defaultdict(lambda: defaultdict(list))

# 2. Wczytujemy plik CSV
with open("times.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        plik = row["plik"]                  # np. "log1.txt"
        numer_testu = int(row["numer_testu"])  
        # Czas w formacie "41.42s" -> float 41.42
        czas_str = row["czas_wykonania"].rstrip("s")  # usuń końcowe "s"
        czas_val = float(czas_str)
        
        # Odkładamy do słownika
        test_durations[plik][numer_testu].append(czas_val)

# 3. Zbierzmy wszystkie numery testów (ze wszystkich plików)
all_test_nums = set()
for plik_dict in test_durations.values():
    all_test_nums.update(plik_dict.keys())  # dodaj numery testów do zbioru

# Posortowana lista numerów testów (np. 1...43)
sorted_tests = sorted(all_test_nums)

# 4. Obliczmy średni czas wykonania dla każdej pary (plik, numer_testu)
#    Możesz też obliczyć sumę, max, min – w zależności od potrzeb.
averages = defaultdict(dict)  # {plik: {numer_testu: sredni_czas}}
for plik, test_dict in test_durations.items():
    for test_num, times in test_dict.items():
        avg_time = sum(times) / len(times)
        averages[plik][test_num] = avg_time

# 5. Przygotujmy dane do wykresu (zachowując kolejność plików)
#    Zakładam, że chcesz mieć kolejność: log1.txt, log2.txt, log3.txt (lewa->prawa)
ordered_logs = ["tbd2b_dbt-run_exec1.txt", "tbd2b_dbt-run_exec2.txt", "tbd2b_dbt-run_exec5.txt"]

# Dla każdego pliku stworzymy listę średnich czasów w kolejności testów sorted_tests
data_for_plot = []
for plik in ordered_logs:
    # Jeżeli brak wpisu w danym pliku dla testu, przyjmij 0 (lub None)
    values_for_plik = [averages[plik].get(t, 0) for t in sorted_tests]
    data_for_plot.append(values_for_plik)

# data_for_plot to np. [
#    [avg_test1_log1, avg_test2_log1, ..., avg_test43_log1],
#    [avg_test1_log2, avg_test2_log2, ..., avg_test43_log2],
#    [avg_test1_log3, avg_test2_log3, ..., avg_test43_log3]
# ]

# 6. Rysowanie grupowanego wykresu słupkowego
x = np.arange(len(sorted_tests))  # np.array z wartościami 0,1,2,...,42 (dla 43 testów)
bar_width = 0.25  # szerokość jednego słupka
offsets = [i * bar_width for i in range(len(ordered_logs))]  
# offsets = [0, 0.25, 0.50] -> przesunięcia słupków w ramach jednej grupy

plt.figure(figsize=(20, 6))  # Rozmiar wykresu (szerokość x wysokość w calach)

for i, plik in enumerate(ordered_logs):
    # data_for_plot[i] -> lista średnich czasów dla pliku i-tego
    plt.bar(x + offsets[i], data_for_plot[i], 
            width=bar_width, 
            label=plik)  # etykieta w legendzie = nazwa pliku

# Ustawiamy etykiety na osi X (pod słupkami) - zamiast 0,1,2,... chcemy np. 1,2,3,...43
plt.xticks(x + bar_width, sorted_tests) 
#        ^ pozycja etykiet  ^ co wypisać

plt.xlabel("Numer testu")
plt.ylabel("Średni czas wykonania (s)")
plt.title("Porównanie czasów wykonania dla 3 plików logów (wykres słupkowy grupowany)")
plt.legend()  # wyświetla legendę z etykietami (log1.txt, log2.txt, log3.txt)

plt.tight_layout()  # lepsze dopasowanie elementów wykresu

# 7. Pokazujemy wykres w oknie
plt.show()

# Jeżeli wolisz zapisać do pliku (zamiast / oprócz .show()):
# plt.savefig("grupowany_wykres_testy.png", dpi=150)

