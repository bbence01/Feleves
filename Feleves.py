import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Toplevel, Text, Scrollbar, Frame, Button, Checkbutton, BooleanVar, Label

# Load and clean data dynamically
def adat_beolvasas():
    """
    Fájl kiválasztása egy párbeszédablakból és adat beolvasása CSV, Excel vagy TXT fájlformátumból.
    :return: Pandas DataFrame az adatokkal
    """
    fajl_nev = filedialog.askopenfilename(
        title="Válassz egy fájlt",
        filetypes=[
            ("Minden adatfájl", "*.csv;*.xlsx;*.xls;*.txt"),
            ("CSV fájlok", "*.csv"),
            ("Excel fájlok", "*.xlsx;*.xls"),
            ("TXT fájlok", "*.txt"),
        ],
    )
    if not fajl_nev:
        return None

    try:
        if fajl_nev.endswith(".csv"):
            adat = pd.read_csv(fajl_nev)
        elif fajl_nev.endswith((".xls", ".xlsx")):
            adat = pd.read_excel(fajl_nev, engine="openpyxl")
        elif fajl_nev.endswith(".txt"):
            with open(fajl_nev, 'r') as file:
                first_line = file.readline()
                delimiter = detect_delimiter(first_line)
                adat = pd.read_csv(fajl_nev, delimiter=delimiter)
        else:
            raise ValueError("Nem támogatott fájlformátum!")
        return adat
    except Exception as e:
        megjelenit_ablak("Hiba", f"Hiba történt az állomány beolvasása során: {e}")
        return None

# Detect delimiter for TXT files
def detect_delimiter(first_line):
    delimiters = [',', '\t', ';', '|']
    delimiter_count = {delimiter: first_line.count(delimiter) for delimiter in delimiters}
    return max(delimiter_count, key=delimiter_count.get)

# Statistical analysis selection window
def select_analysis_options(adatok):
    """
    Creates a GUI for the user to choose statistical tools and columns for analysis.
    """
    analysis_window = Toplevel()
    analysis_window.title("Analysis Options")
    analysis_window.geometry("600x600")  # Increased height to accommodate more options

    # Column selection
    Label(analysis_window, text="Válassza ki az elemzendő oszlopokat:").pack()
    column_vars = {}
    for col in adatok.columns:
        var = BooleanVar(value=True)
        column_vars[col] = var
        Checkbutton(analysis_window, text=col, variable=var).pack(anchor='w')

    # Statistical tools selection
    Label(analysis_window, text="Válassza ki az alkalmazandó statisztikai eszközöket:").pack()
    stats_tools = {
        "Átlag (Mean)": BooleanVar(value=True),
        "Medián (Median)": BooleanVar(value=True),
        "Szórás (Standard Deviation)": BooleanVar(value=True),
        "Minimum": BooleanVar(value=True),
        "Maximum": BooleanVar(value=True),
        "Módusz (Mode)": BooleanVar(value=True),  # Added mode for categorical data
        "Gyakoriság (Value Counts)": BooleanVar(value=True),  # Added value counts
    }
    for tool, var in stats_tools.items():
        Checkbutton(analysis_window, text=tool, variable=var).pack(anchor='w')

    # Confirm button
    Button(
        analysis_window,
        text="Elemzés indítása",
        command=lambda: perform_analysis(adatok, column_vars, stats_tools),
    ).pack()

    # Close button with graphical window callback
    Button(
        analysis_window,
        text="Tovább a vizualizációhoz",
        command=lambda: [select_visualization_options(adatok), analysis_window.destroy()],
    ).pack()

    print("Analysis Options Window Created.")

# Perform the selected analysis
def perform_analysis(adatok, column_vars, stats_tools):
    """
    Perform the analysis based on selected options.
    """
    # Filter columns
    selected_columns = [col for col, var in column_vars.items() if var.get()]
    data_to_analyze = adatok[selected_columns]

    results = ""

    # Numerical analysis
    numeric_data = data_to_analyze.select_dtypes(include=["number"])
    if not numeric_data.empty:
        results += "Numerikus adatok statisztikai eredményei:\n\n"
        if stats_tools["Átlag (Mean)"].get():
            results += f"Átlag:\n{numeric_data.mean()}\n\n"
        if stats_tools["Medián (Median)"].get():
            results += f"Medián:\n{numeric_data.median()}\n\n"
        if stats_tools["Szórás (Standard Deviation)"].get():
            results += f"Szórás:\n{numeric_data.std()}\n\n"
        if stats_tools["Minimum"].get():
            results += f"Minimum:\n{numeric_data.min()}\n\n"
        if stats_tools["Maximum"].get():
            results += f"Maximum:\n{numeric_data.max()}\n\n"

    # Categorical analysis
    categorical_data = data_to_analyze.select_dtypes(include=["object", "category"])
    if not categorical_data.empty:
        results += "Kategorikus adatok statisztikai eredményei:\n\n"
        if stats_tools["Módusz (Mode)"].get():
            mode_result = categorical_data.mode().iloc[0]
            results += f"Módusz:\n{mode_result}\n\n"
        if stats_tools["Gyakoriság (Value Counts)"].get():
            for col in categorical_data.columns:
                results += f"Gyakoriság - {col}:\n{categorical_data[col].value_counts()}\n\n"

    if results:
        megjelenit_ablak("Elemzés Eredményei", results)
    else:
        megjelenit_ablak("Elemzés Eredményei", "Nincs megjeleníthető eredmény a kiválasztott opciókhoz.")

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

def select_visualization_options(adatok):
    """
    Creates a GUI for the user to choose data visualization options.
    """
    print("Opening Visualization Options Window...")  # Debugging log

    # Create the Toplevel window
    visualization_window = Toplevel()
    visualization_window.title("Visualization Options")
    visualization_window.geometry("600x600")  # Increased height

    # Ensure window creation
    visualization_window.update_idletasks()
    print("Visualization Options Window Created.")  # Debugging log

    # Column selection
    Label(visualization_window, text="Válassza ki a megjelenítendő oszlopokat:").pack()
    column_vars = {}
    for col in adatok.columns:
        var = BooleanVar(value=True)
        column_vars[col] = var
        Checkbutton(visualization_window, text=col, variable=var).pack(anchor='w')

    # Visualization type selection
    Label(visualization_window, text="Válassza ki a diagram típusát:").pack()
    visualization_types = {
        "Hisztogram (Numeric)": BooleanVar(value=True),
        "Oszlopdiagram (Categorical)": BooleanVar(value=True),
        "Kördiagram (Pie Chart - Categorical)": BooleanVar(value=True),  # Added pie chart option
    }
    for vis_type, var in visualization_types.items():
        Checkbutton(visualization_window, text=vis_type, variable=var).pack(anchor='w')

    # Confirm button
    Button(
        visualization_window,
        text="Megjelenítés indítása",
        command=lambda: perform_visualization(adatok, column_vars, visualization_types),
    ).pack()

    # Close button
    Button(visualization_window, text="Bezárás", command=visualization_window.destroy).pack()

    # Ensure the window is displayed and responsive
    print("Visualization Options Window Ready.")  # Debugging log

def perform_visualization(adatok, column_vars, visualization_types):
    """
    Perform visualization based on selected options.
    """
    # Filter selected columns
    selected_columns = [col for col, var in column_vars.items() if var.get()]
    data_to_visualize = adatok[selected_columns]

    # Generate visualizations
    if visualization_types["Hisztogram (Numeric)"].get():
        numeric_data = data_to_visualize.select_dtypes(include=["number"])
        if not numeric_data.empty:
            numeric_data.hist(bins=20, figsize=(10, 6))
            plt.suptitle("Hisztogramok a numerikus oszlopokhoz")
            plt.show()
        else:
            megjelenit_ablak("Figyelmeztetés", "Nincs numerikus adat a hisztogramokhoz.")

    if visualization_types["Oszlopdiagram (Categorical)"].get():
        categorical_data = data_to_visualize.select_dtypes(include=["object", "category"])
        if not categorical_data.empty:
            for col in categorical_data.columns:
                if categorical_data[col].nunique() < 20:  # Limit to manageable categories
                    categorical_data[col].value_counts().plot(kind="bar", figsize=(10, 6))
                    plt.title(f"Oszlopdiagram: {col}")
                    plt.xlabel(col)
                    plt.ylabel("Előfordulások száma")
                    plt.show()
                else:
                    megjelenit_ablak("Figyelmeztetés", f"Túl sok kategória az oszlopdiagramhoz: {col}")
        else:
            megjelenit_ablak("Figyelmeztetés", "Nincs kategorikus adat az oszlopdiagramokhoz.")

    if visualization_types["Kördiagram (Pie Chart - Categorical)"].get():
        categorical_data = data_to_visualize.select_dtypes(include=["object", "category"])
        if not categorical_data.empty:
            for col in categorical_data.columns:
                if categorical_data[col].nunique() < 10:  # Limit to manageable categories
                    categorical_data[col].value_counts().plot(kind="pie", figsize=(8, 8), autopct='%1.1f%%')
                    plt.title(f"Kördiagram: {col}")
                    plt.ylabel('')  # Hide y-label for pie chart
                    plt.show()
                else:
                    megjelenit_ablak("Figyelmeztetés", f"Túl sok kategória a kördiagramhoz: {col}")
        else:
            megjelenit_ablak("Figyelmeztetés", "Nincs kategorikus adat a kördiagramokhoz.")

# Main program
if __name__ == "__main__":
    root = Tk()
    # root.withdraw()  # You can hide the root window if desired
    root.title("Adat Analízis és Vizualizáció")
    root.geometry("200x100")  # Set size for the root window

    # Start button to initiate data loading and analysis options
    Button(
        root,
        text="Adatok Beolvasása",
        command=lambda: [adatok := adat_beolvasas(), select_analysis_options(adatok) if adatok is not None else None],
    ).pack(pady=20)

    root.mainloop()  # Single mainloop
