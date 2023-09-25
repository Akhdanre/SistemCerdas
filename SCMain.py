import pyfiglet
import time
import sys
from rich.console import Console
from rich.table import Table
from rich.live import Live
from pick import pick
from pynput.keyboard import Key, Controller

TEXT_SPEED = 0.07
REFRESH_RATE = 1

console = Console()
keyboard = Controller()


def print_slow(text, colorTxt="white"):
    """Print text slowly, one character at a time."""
    for letter in text:
        console.print(letter, style=colorTxt, end="")
        time.sleep(TEXT_SPEED)


def get_user_input(prompt):
    """Get user input and handle any exceptions."""
    try:
        return input(prompt)
    except KeyboardInterrupt:
        sys.exit(0)


def main():
    title = pyfiglet.figlet_format("Deteksi Penyakit Mata", width=200)
    print(title)

    print_slow("Masukkan namamu\n")
    name = get_user_input("Nama : ")
    print_slow(f"Hallo, {name}\n")

    table = Table(title="Daftar Gejala")
    table.add_column("Kode", justify="right", style="cyan", no_wrap=True)
    table.add_column("Nama Gejala", style="magenta")

    table2 = Table(title="Daftar Penyakit")
    table2.add_column("Kode", justify="right", style="cyan", no_wrap=True)
    table2.add_column("Nama Penyakit", style="magenta")

    list_penyakit = {
        "P01": "Miopia",
        "P02": "Hipermetropia",
        "P03": "Astigmatisma",
        "P04": "Presbiopi"
    }

    list_gejala = [
        ["G01", "Pandangan kabur saat melihat objek"],
        ["G02", "Sering menyipitkan mata"],
        ["G03", "Sakit kepala"],
        ["G04", "Mata lelah"],
        ["G05", "Sering menggosok mata"],
        ["G06", "Frekuensi mengedipkan mata yang berlebihan"],
        ["G07", "Melihat objek jauh terlihat jelas"],
        ["G08", "Melihat objek dekat terlihat buram"],
        ["G09", "Mengerlingkan mata untuk melihat objek jelas"],
        ["G10", "Kesulitan Membaca"],
        ["G11", "Mata terasa panas dan gatal"],
        ["G12", "Distorsi pengelihatan"],
        ["G13", "Pandangan samar"],
        ["G14", "Sulit melihat saat malam hari"],
        ["G15", "Mata sering tegang dan mudah lelah"],
        ["G16", "Sensitif pada sorotan cahaya"],
        ["G17", "Kesulitan membedakan warna yang mirip"],
        ["G18", "pengelihatan ganda"],
        ["G19", "membutuhkan penerangan lebih saat membaca"],
        ["G20", "Sulit membaca huruf berukuran kecil"]
    ]

    dataKeputusanPakar = {
        "G01": {"P01": 0.25,  "P02": 0, "P03": 0, "P04": 0.25},
        "G02": {"P01": 0,  "P02": 0, "P03": 0.25, "P04": 0.25},
        "G03": {"P01": 0.25,  "P02": 0.25, "P03": 0.25, "P04": 0.25},
        "G04": {"P01": 0.25,  "P02": 0, "P03": 0, "P04": 0},
        "G05": {"P01": 0.25,  "P02": 0, "P03": 0, "P04": 0},
        "G06": {"P01": 0.25,  "P02": 0, "P03": 0, "P04": 0},
        "G07": {"P01": 0,  "P02": 0.25, "P03": 0, "P04": 0},
        "G08": {"P01": 0,  "P02": 0.25, "P03": 0, "P04": 0},
        "G09": {"P01": 0,  "P02": 0.25, "P03": 0, "P04": 0},
        "G10": {"P01": 0,  "P02": 0.25, "P03": 0, "P04": 0},
        "G11": {"P01": 0,  "P02": 0.25, "P03": 0, "P04": 0},
        "G12": {"P01": 0,  "P02": 0, "P03": 0.25, "P04": 0},
        "G13": {"P01": 0,  "P02": 0, "P03": 0.25, "P04": 0},
        "G14": {"P01": 0,  "P02": 0, "P03": 0.25, "P04": 0},
        "G15": {"P01": 0,  "P02": 0, "P03": 0.25, "P04": 0},
        "G16": {"P01": 0,  "P02": 0, "P03": 0.25, "P04": 0},
        "G17": {"P01": 0,  "P02": 0, "P03": 0, "P04": 0.25},
        "G18": {"P01": 0,  "P02": 0, "P03": 0.25, "P04": 0},
        "G19": {"P01": 0,  "P02": 0, "P03": 0, "P04": 0.25},
        "G20": {"P01": 0,  "P02": 0, "P03": 0, "P04": 0.25},
    }
    with Live(table2, refresh_per_second=4):
        for rbys, val in list_penyakit.items():
            time.sleep(0.2)
            table2.add_row(rbys, val)

    command = get_user_input(
        "Lanjutkan memilih gejala yang anda alami dengan mengetik Yes : ")

    if command == "yes" or command == "Yes":
        title = "pilih gejala gejala yang kamu rasakan: "
        selected = pick([data[1] for data in list_gejala], title, multiselect=True,
                        min_selection_count=1)
        print_slow("gejala yang anda alami \n")
        for idx, item in enumerate(selected, start=1):
            print_slow(f"{idx}. {item[0]}\n")
    else:
        print_slow("Baiklah")
        # cm = get_user_input("yes/no")
        exit()

    hasilAkhirBayes = {}
    for k in range(4):
        prob_1 = f"P0{k+1}"
        totalBayes = []
        for i in selected:
            valueKode = i[1]+1
            dataKode = f"G{valueKode}" if valueKode > 9 else f'G0{valueKode}'
            dataPakar = dataKeputusanPakar[dataKode]
            if (dataPakar[prob_1]):
                result = dataPakar[prob_1] / \
                    (dataPakar["P01"] + dataPakar["P02"] +
                     dataPakar["P03"] + dataPakar["P04"])
                # print(f"P({prob_1} | {i}) = {result}")
                totalBayes.append(result)
        sumTotalBayes = sum(totalBayes)
        if (len(totalBayes) > 1):
            hasilAkhirBayes[prob_1] = sumTotalBayes
        # print(f"total bayes untuk {prob_1} = {sumTotalBayes} \n")

    nilaiHasilAkhirBayes = sum(hasilAkhirBayes.values())
    # print(f"hasil akhir bayes = {nilaiHasilAkhirBayes}")
    presentasePenyakit = {}
    for bys, val in hasilAkhirBayes.items():
        resultPrecentage = (val / nilaiHasilAkhirBayes) * 100
        # print(
        #     f"P({bys}) = {val} / {nilaiHasilAkhirBayes} x 100 = {resultPrecentage}")
        presentasePenyakit[bys] = resultPrecentage
    # print(presentasePenyakit)
    topKeyPercentage = max(presentasePenyakit, key=presentasePenyakit.get)
    print("\n")
    print("Berdasarkan Pernyataan anda")
    print_slow(
        f"Saudara {name}, anda terkena penyakit {list_penyakit[topKeyPercentage]} \npresentase {list_penyakit[topKeyPercentage]} sebesar {round(presentasePenyakit[topKeyPercentage])}%")
    print("\n")


if __name__ == "__main__":
    main()
