import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Toplevel, Text, Scrollbar, Frame, Button


# Load and clean data dynamically
def adat_beolvasas():
    """
    Fájl kiválasztása egy párbeszédablakból és adat beolvasása CSV vagy Excel fájlformátumból.
    :return: Pandas DataFrame az adatokkal
    """
    root = Tk()
    root.withdraw()
    fajl_nev = filedialog.askopenfilename(
        title="Válassz egy fájlt",
        filetypes=[("Minden adatfájl", "*.csv;*.xlsx;*.xls"), ("CSV fájlok", "*.csv"), ("Excel fájlok", "*.xlsx;*.xls")]
    )
    if not fajl_nev:
        return None

    try:
        # Determine file type and load data
        if fajl_nev.endswith(".csv"):
            # Load CSV and infer header row
            adat = pd.read_csv(fajl_nev, header=None)
        elif fajl_nev.endswith((".xls", ".xlsx")):
            # Check for Excel dependencies
            try:
                adat = pd.read_excel(fajl_nev, header=None, engine="openpyxl" if fajl_nev.endswith(".xlsx") else "xlrd")
            except ImportError as e:
                megjelenit_ablak("Hiba", f"A szükséges könyvtárak hiányoznak: {e}")
                return None
        else:
            raise ValueError("Nem támogatott fájlformátum!")

        # Infer header row and drop irrelevant rows
        header_row = adat.apply(lambda row: row.notna().sum(), axis=1).idxmax()
        adat.columns = adat.iloc[header_row].fillna("").astype(str).str.strip()
        adat = adat.iloc[header_row + 1:].reset_index(drop=True)

        # Convert numeric columns
        for col in adat.columns:
            adat[col] = pd.to_numeric(adat[col], errors="ignore")

        return adat

    except Exception as e:
        megjelenit_ablak("Hiba", f"Hiba történt az állomány beolvasása során: {e}")
        return None


    except Exception as e:
        megjelenit_ablak("Hiba", f"Hiba történt az állomány beolvasása során: {e}")
        return None


# Display results in a tkinter window
def megjelenit_ablak(cim, szoveg):
    ablak = Toplevel()
    ablak.title(cim)

    frame = Frame(ablak)
    frame.pack(fill="both", expand=True)

    szovegdoboz = Text(frame, wrap="word", bg="white", fg="black")
    szovegdoboz.insert("1.0", szoveg)
    szovegdoboz.config(state="disabled")
    szovegdoboz.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(frame, command=szovegdoboz.yview)
    scrollbar.pack(side="right", fill="y")
    szovegdoboz.config(yscrollcommand=scrollbar.set)

    Button(ablak, text="Bezárás", command=ablak.destroy).pack()


# Numerical analysis
def numerikus_elemzes(adatok):
    numerikus_adatok = adatok.select_dtypes(include=["number"])
    if not numerikus_adatok.empty:
        szoveg = "Numerikus adatok statisztikai összefoglalása:\n\n"
        szoveg += str(numerikus_adatok.describe())
        megjelenit_ablak("Numerikus Elemzés", szoveg)


# Textual analysis
def szoveges_elemzes(adatok):
    szoveges_adatok = adatok.select_dtypes(include=["object"])
    szoveg = ""
    for oszlop in szoveges_adatok.columns:
        szoveg += f"'{oszlop}' oszlop leggyakoribb értékei:\n"
        szoveg += str(szoveges_adatok[oszlop].value_counts().head(5)) + "\n\n"
    if szoveg:
        megjelenit_ablak("Szöveges Elemzés", szoveg)


# Visualization
def adatok_vizualizacio(adatok):
    numerikus_adatok = adatok.select_dtypes(include=["number"])
    if not numerikus_adatok.empty:
        numerikus_adatok.hist(bins=20, figsize=(10, 6))
        plt.suptitle("Numerikus adatok hisztogramjai")
        plt.show()

    for oszlop in adatok.select_dtypes(include=["object"]).columns:
        if adatok[oszlop].nunique() < 20:  # Only visualize columns with fewer categories
            adatok[oszlop].value_counts().plot(kind="bar", figsize=(10, 6))
            plt.title(f"{oszlop} gyakorisága")
            plt.xlabel(oszlop)
            plt.ylabel("Előfordulások száma")
            plt.show()


# Main program
if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    adatok = adat_beolvasas()
    if adatok is not None:
        numerikus_elemzes(adatok)
        szoveges_elemzes(adatok)
        adatok_vizualizacio(adatok)
