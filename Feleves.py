import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog, Text, Toplevel, Scrollbar, Frame, Button


# Adatbeolvasás funkció
def adat_beolvasas():
    """
    Fájl kiválasztása egy párbeszédablakból és adat beolvasása.
    :return: Pandas DataFrame az adatokkal
    """
    root = Tk()
    root.withdraw()  # Elrejti a Tkinter ablakot
    fajl_nev = filedialog.askopenfilename(
        title="Válassz egy fájlt",
        filetypes=[("CSV fájlok", "*.csv"), ("Minden fájl", "*.*")]
    )
    if not fajl_nev:
        return None
    try:
        adatok = pd.read_csv(fajl_nev)
        return adatok
    except Exception as e:
        megjelenit_ablak("Hiba", f"Hiba történt az állomány beolvasása során: {e}")
        return None


# Megjelenítés ablakban
def megjelenit_ablak(cim, szoveg):
    """
    Szöveg megjelenítése egy új ablakban.
    :param cim: Ablak címe
    :param szoveg: Megjelenítendő szöveg
    """
    ablak = Toplevel()
    ablak.title(cim)

    frame = Frame(ablak)
    frame.pack(fill="both", expand=True)

    szovegdoboz = Text(frame, wrap="word", bg="white", fg="black")
    szovegdoboz.insert("1.0", szoveg)
    szovegdoboz.config(state="disabled")  # Olvasásra állítjuk
    szovegdoboz.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(frame, command=szovegdoboz.yview)
    scrollbar.pack(side="right", fill="y")
    szovegdoboz.config(yscrollcommand=scrollbar.set)

    Button(ablak, text="Bezárás", command=ablak.destroy).pack()


# Numerikus elemzés
def numerikus_elemzes(adatok):
    """
    Numerikus statisztikai számítások az adatokon, ablakban megjelenítve.
    """
    numerikus_adatok = adatok.select_dtypes(include=["number"])
    if not numerikus_adatok.empty:
        szoveg = "Numerikus adatok statisztikai összefoglalása:\n\n"
        szoveg += str(numerikus_adatok.describe())  # Alapvető statisztikák
        megjelenit_ablak("Numerikus Elemzés", szoveg)


# Szöveges adatok elemzése
def szoveges_elemzes(adatok):
    """
    Szöveges oszlopok elemzése, ablakban megjelenítve.
    """
    szoveges_adatok = adatok.select_dtypes(include=["object"])
    szoveg = ""
    for oszlop in szoveges_adatok.columns:
        szoveg += f"'{oszlop}' oszlop leggyakoribb értékei:\n"
        szoveg += str(szoveges_adatok[oszlop].value_counts().head(5)) + "\n\n"
    if szoveg:
        megjelenit_ablak("Szöveges Elemzés", szoveg)


# Dátum elemzés
def datum_elemzes(adatok):
    """
    Elemzés dátumos oszlopokra.
    """
    datum_adatok = adatok.select_dtypes(include=["datetime", "object"]).apply(pd.to_datetime, errors="coerce")
    for oszlop in datum_adatok.columns:
        if datum_adatok[oszlop].notna().any():
            szoveg = f"'{oszlop}' oszlop érvényes dátumtartománya:\n\n"
            szoveg += f"Minimum: {datum_adatok[oszlop].min()}\n"
            szoveg += f"Maximum: {datum_adatok[oszlop].max()}\n"
            megjelenit_ablak(f"Dátum Elemzés - {oszlop}", szoveg)


# Adatok vizualizációja
def adatok_vizualizacio(adatok):
    """
    Alapvető vizualizációk létrehozása az adatokból.
    """
    numerikus_adatok = adatok.select_dtypes(include=["number"])
    if not numerikus_adatok.empty:
        numerikus_adatok.hist(bins=20, figsize=(10, 6))
        plt.suptitle("Numerikus adatok hisztogramjai")
        plt.show()

    for oszlop in adatok.select_dtypes(include=["object"]).columns:
        if adatok[oszlop].nunique() < 20:  # Csak a kevés kategóriájú oszlopokat vizualizáljuk
            plt.figure(figsize=(10, 6))
            adatok[oszlop].value_counts().plot(kind="bar")
            plt.title(f"{oszlop} gyakorisága")
            plt.xlabel(oszlop)
            plt.ylabel("Előfordulások száma")
            plt.show()


# Fő program
if __name__ == "__main__":
    # Tkinter főablak
    root = Tk()
    root.withdraw()  # Elrejti a fő Tkinter ablakot

    adatok = adat_beolvasas()
    if adatok is not None:
        numerikus_elemzes(adatok)
        szoveges_elemzes(adatok)
        datum_elemzes(adatok)
        adatok_vizualizacio(adatok)
