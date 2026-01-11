import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Rectangle, Circle
import tkinter.messagebox as messagebox
from tooltip import ToolTip
from calc import calc
import webbrowser
import os
import sys

PAD_X = 10
PAD_Y = 6
FONT_TITLE = ("Helvetica", 13, "bold")
FONT_TEXT = ("Helvetica", 12)

class Geometri(ctk.CTkFrame):
    def __init__(self, master, funderingsform_var):
        super().__init__(master, fg_color="transparent")
        
        funderingsform = funderingsform_var.get()

        if funderingsform == "Stribe":
            labels = ["Bredde, B [m]:", "FUK [m u.t.]:", "Vandstand, VSP [m u.t.]:"]
        elif funderingsform == "Rektangulært":
            labels = ["Bredde, B [m]:", "Længde, L [m]:", "FUK [m u.t.]:", "Vandstand, VSP [m u.t.]:"]
        else:  # Cirkulært
            labels = ["Diameter, Ø [m]:", "FUK [m u.t.]:", "Vandstand, VSP [m u.t.]:"]

        self.entries_1 = {}
        for i, label_text in enumerate(labels):
            if label_text == "Bredde, B [m]:":
                label = ctk.CTkLabel(self, text=label_text + " ⓘ", font=FONT_TEXT, anchor="w", width=140)
                label.grid(row=i, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
                ToolTip(label, "Det gælder at bredde ≤ længde")
            else:
                label = ctk.CTkLabel(self, text=label_text, font=FONT_TEXT, anchor="w", width=140)
                label.grid(row=i, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
            entry = ctk.CTkEntry(self, placeholder_text="0", width=120)
            entry.grid(row=i, column=1, padx=PAD_X, pady=PAD_Y)
            self.entries_1[label_text] = entry
            
class Styrkeparametre(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        labels = ["φ [°]:", "c_u [kPa]:", "c' [kPa]:", "Ruhedsgrad:"]
        
        self.entries_2 = {}
        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self, text=label_text, font=FONT_TEXT, anchor="w", width=140)
            label.grid(row=i, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
            entry = ctk.CTkEntry(self, placeholder_text="0", width=120)
            entry.grid(row=i, column=1, padx=PAD_X, pady=PAD_Y)
            self.entries_2[label_text] = entry
            
class Egenvaegt(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        label = ctk.CTkLabel(self, text="Fundament, γ_g [kN/m3]:", font=FONT_TEXT, anchor="w", width=140)
        label.grid(row=0, column=0, padx=PAD_X, pady=(PAD_Y, 0), sticky="w")
        entry = ctk.CTkEntry(self, placeholder_text="0", width=120)
        entry.grid(row=0, column=1, padx=PAD_X, pady=(PAD_Y, 0))
        self.entry = entry  # Store reference to entry for later access

class Rumvaegt_jord(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        labels = ["Tør jord, γ_d [kN/m3]:", "Mættet jord, γ_m [kN/m3]:"]
        
        self.entries = {}
        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self, text=label_text, font=FONT_TEXT, anchor="w", width=140)
            label.grid(row=i, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
            entry = ctk.CTkEntry(self, placeholder_text="0", width=120)
            entry.grid(row=i, column=1, padx=PAD_X, pady=PAD_Y)
            self.entries[label_text] = entry  # Store reference to entry for later access
        
class CC(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        labels = ["γ_cu:", "γ_c':", f"γ_\u03C6:"]
        
        self.entries_CC = {}
        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self, text=label_text, font=FONT_TEXT, anchor="w", width=140)
            label.grid(row=i, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
            entry = ctk.CTkEntry(self, placeholder_text="0", width=120)
            entry.grid(row=i, column=1, padx=PAD_X, pady=PAD_Y)
            self.entries_CC[label_text] = entry
  
class Laster(ctk.CTkFrame):
    def __init__(self, master, funderingsform):
        super().__init__(master, fg_color="transparent")
        
        
        if funderingsform.get() == "Rektangulært":
            labels = ["V [kN]:", "H_B [kN]:", "H_L [kN]:", "M_B [kNm]:", "M_L [kNm]:"]
            tip = ["Lodret last i centrum af fundament", f"Vandret last parallel med fundamentsbredden.\nBæreevne eftervises for resulterende vandret\nlast ført parallel med fundamentsbredden", f"Vandret last parallel med fundamentslængden.\nBæreevne eftervises for resulterende vandret\nlast ført parallel med fundamentsbredden", "Moment om længdeakse", "Moment om breddeakse"]
        elif funderingsform.get() == "Stribe":
            labels = ["V [kN/m]:", "H [kN/m]:", "M [kNm/m]:"]
            tip = ["Lodret linjelast i centerlinje af fundament", "Vandret linjelast", "Moment pr. meter. Husk momentarm øges med funderingsdybden"]
        else:
            labels = ["V [kN]:", "H [kN]:", "M [kNm]:"]
            tip = ["Lodret last i centrum af fundament", "Vandret last", "Moment. Husk momentarm øges med funderingsdybden"]
        
        self.entries = {}
        
        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self, text=label_text+" ⓘ", font=FONT_TEXT, anchor="w", width=140)
            label.grid(row=i, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
            ToolTip(label, tip[i])
            entry = ctk.CTkEntry(self, placeholder_text="0", width=120)
            entry.grid(row=i, column=1, padx=PAD_X, pady=PAD_Y)

            self.entries[label_text] = entry

class Resultater(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")          
        
        # Felt til tegning af fundament
        self.canvas_frame_left = ctk.CTkFrame(self, corner_radius=10, fg_color="white")
        self.canvas_frame_left.grid(row=1, column=0, padx=(10,5), pady=(0,5), sticky="nsew")
        self.canvas_frame_right = ctk.CTkFrame(self, corner_radius=10, fg_color="white")
        self.canvas_frame_right.grid(row=1, column=1, padx=(10,5), pady=(0,5), sticky="nsew")
        
        # Add grid weights so both frames expand properly
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.canvas = None
        self.canvas_top = None
        
class Geometry_res(ctk.CTkFrame):
    def __init__(self, master, funderingsform):
        super().__init__(master, fg_color="transparent")     
        
        f = funderingsform.get()
        if f == "Stribe":
            self.label20 = ctk.CTkLabel(self, text="Effektivt areal:", font=FONT_TEXT)
            self.label20.grid(row=2, column=0, padx=PAD_X, pady=1, sticky="w")
            self.label30 = None
            self.label21 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
            self.label21.grid(row=2, column=1, padx=PAD_X, pady=1, sticky="w")
            self.label31 = None
        else:
            self.label20 = ctk.CTkLabel(self, text="Effektiv længde:", font=FONT_TEXT)
            self.label20.grid(row=2, column=0, padx=PAD_X, pady=1, sticky="w")
            self.label30 = ctk.CTkLabel(self, text="Effektivt areal:", font=FONT_TEXT)
            self.label30.grid(row=3, column=0, padx=PAD_X, pady=1, sticky="w")
            self.label21 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
            self.label21.grid(row=2, column=1, padx=PAD_X, pady=1, sticky="w")
            self.label31 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
            self.label31.grid(row=3, column=1, padx=PAD_X, pady=1, sticky="w")
            
        self.label00 = ctk.CTkLabel(self, text="Excentricitet:", font=FONT_TEXT)
        self.label00.grid(row=0, column=0, padx=PAD_X, pady=1, sticky="w")
        self.label10 = ctk.CTkLabel(self, text="Effektiv bredde:", font=FONT_TEXT)
        self.label10.grid(row=1, column=0, padx=PAD_X, pady=1, sticky="w")
        

        self.label01 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label01.grid(row=0, column=1, padx=PAD_X, pady=1, sticky="w")
        self.label11 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label11.grid(row=1, column=1, padx=PAD_X, pady=1, sticky="w")
        
        
        self.grid_columnconfigure(0, minsize=250, weight=0)
        self.grid_columnconfigure(1, minsize=150, weight=0)
        
        ToolTip(self.label01, f"Stærkt excentrisk belastning: e>0.3B")
        
class Styrker_res(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.label00 = ctk.CTkLabel(self, text="φ'_d:", font=FONT_TEXT)
        self.label00.grid(row=0, column=0, padx=PAD_X, pady=1, sticky="w")
        self.label10 = ctk.CTkLabel(self, text="c_ud:", font=FONT_TEXT)
        self.label10.grid(row=1, column=0, padx=PAD_X, pady=1, sticky="w")
        self.label20 = ctk.CTkLabel(self, text="c'_d:", font=FONT_TEXT)
        self.label20.grid(row=2, column=0, padx=PAD_X, pady=1, sticky="w")

        self.label01 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label01.grid(row=0, column=1, padx=PAD_X, pady=1, sticky="w")
        self.label11 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label11.grid(row=1, column=1, padx=PAD_X, pady=1, sticky="w")
        self.label21 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label21.grid(row=2, column=1, padx=PAD_X, pady=1, sticky="w")
        
        self.grid_columnconfigure(0, minsize=250, weight=0)
        self.grid_columnconfigure(1, minsize=150, weight=0)

class Drained_res(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.label00 = ctk.CTkLabel(self, text="Bæreevnefaktorer:", font=FONT_TEXT)
        self.label00.grid(row=0, column=0, padx=PAD_X, pady=0, sticky="w")
        self.label10 = ctk.CTkLabel(self, text="Formfaktorer:", font=FONT_TEXT)
        self.label10.grid(row=1, column=0, padx=PAD_X, pady=0, sticky="w")
        self.label20 = ctk.CTkLabel(self, text="Hældningsfaktorer:", font=FONT_TEXT)
        self.label20.grid(row=2, column=0, padx=PAD_X, pady=0, sticky="w")
        self.label30 = ctk.CTkLabel(self, text="Lodret bæreevne:", font=FONT_TEXT) #lodret bæreevne titel
        self.label30.grid(row=3, column=0, padx=PAD_X, pady=(10,1), sticky="w")
        self.label40 = ctk.CTkLabel(self, text="Vandret bæreevne:", font=FONT_TEXT)
        self.label40.grid(row=4, column=0, padx=PAD_X, pady=1, sticky="w")

        self.label01 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label01.grid(row=0, column=1, padx=PAD_X, pady=0, sticky="w")
        self.label02 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label02.grid(row=0, column=2, padx=PAD_X, pady=0, sticky="w")
        self.label03 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label03.grid(row=0, column=3, padx=PAD_X, pady=0, sticky="w")
        
        self.label11 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label11.grid(row=1, column=1, padx=PAD_X, pady=0, sticky="w")
        self.label12 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label12.grid(row=1, column=2, padx=PAD_X, pady=0, sticky="w")
        self.label13 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label13.grid(row=1, column=3, padx=PAD_X, pady=0, sticky="w")
        
        self.label21 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label21.grid(row=2, column=1, padx=PAD_X, pady=0, sticky="w")
        self.label22 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label22.grid(row=2, column=2, padx=PAD_X, pady=0, sticky="w")
        self.label23 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label23.grid(row=2, column=3, padx=PAD_X, pady=0, sticky="w")
        
        self.label31 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label31.grid(row=3, column=1, padx=PAD_X, pady=(10,1), sticky="w")
        self.label32 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label32.grid(row=3, column=2, padx=PAD_X, pady=(10,1), sticky="w")
        self.label33 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label33.grid(row=3, column=3, padx=PAD_X, pady=(10,1), sticky="w")
        
        self.label41 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label41.grid(row=4, column=1, padx=PAD_X, pady=0, sticky="w")
        self.label42 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label42.grid(row=4, column=2, padx=PAD_X, pady=0, sticky="w")
        self.label43 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label43.grid(row=4, column=3, padx=PAD_X, pady=0, sticky="w")
        
        self.grid_columnconfigure(0, minsize=250, weight=0)
        self.grid_columnconfigure(1, minsize=150, weight=0)
        self.grid_columnconfigure(2, minsize=150, weight=0)
        self.grid_columnconfigure(3, minsize=150, weight=0)

class Undrained_res(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.label00 = ctk.CTkLabel(self, text="Bæreevnefaktorer:", font=FONT_TEXT)
        self.label00.grid(row=0, column=0, padx=PAD_X, pady=0, sticky="w", )
        self.label10 = ctk.CTkLabel(self, text="Formfaktorer:", font=FONT_TEXT)
        self.label10.grid(row=1, column=0, padx=PAD_X, pady=0, sticky="w")
        self.label20 = ctk.CTkLabel(self, text="Hældningsfaktorer:", font=FONT_TEXT)
        self.label20.grid(row=2, column=0, padx=PAD_X, pady=0, sticky="w")
        self.label30 = ctk.CTkLabel(self, text="Lodret bæreevne:", font=FONT_TEXT) #lodret bæreevne titel
        self.label30.grid(row=3, column=0, padx=PAD_X, pady=(10,1), sticky="w") 
        self.label40 = ctk.CTkLabel(self, text="Vandret bæreevne:", font=FONT_TEXT)
        self.label40.grid(row=4, column=0, padx=PAD_X, pady=1, sticky="w")

        self.label01 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label01.grid(row=0, column=1, padx=PAD_X, pady=0, sticky="w")
        self.label11 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label11.grid(row=1, column=1, padx=PAD_X, pady=0, sticky="w")
        self.label21 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label21.grid(row=2, column=1, padx=PAD_X, pady=0, sticky="w")
        
        self.label31 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label31.grid(row=3, column=1, padx=PAD_X, pady=(10,0), sticky="w")
        self.label32 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label32.grid(row=3, column=2, padx=PAD_X, pady=(10,0), sticky="w")
        self.label33 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label33.grid(row=3, column=3, padx=PAD_X, pady=(10,0), sticky="w")
        
        self.label41 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label41.grid(row=4, column=1, padx=PAD_X, pady=0, sticky="w")
        self.label42 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label42.grid(row=4, column=2, padx=PAD_X, pady=0, sticky="w")
        self.label43 = ctk.CTkLabel(self, text="", font=FONT_TEXT)
        self.label43.grid(row=4, column=3, padx=PAD_X, pady=0, sticky="w")
        
        self.grid_columnconfigure(0, minsize=250, weight=0)
        self.grid_columnconfigure(1, minsize=150, weight=0)
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Set appearance mode and default color theme
        ctk.set_appearance_mode("Light")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("green") # Themes: "blue" (default), "dark-blue", "green"

        # Opret app-vindue
        self.title("Direkte Bæreevne Beregner - v1.0")
        self.geometry("1200x800")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)
        self.iconbitmap(resource_path("icon.ico"))
        
        # Top bjælke
        topbar = ctk.CTkFrame(self, fg_color="#e5e5e5", height=50, corner_radius=0)
        topbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        title = ctk.CTkLabel(topbar, text="Direkte Bæreevne Beregner", font=("Helvetica", 18, "bold"))
        title.pack(side="left", padx=20)
        beskrivelse = ctk.CTkLabel(topbar, text=f"Ved anvendelse af Terzaghis bæreevneformler jf. DS/EN 1997-1:2007 og DS/EN 1997-1 DK NA:2021", font=FONT_TEXT)
        beskrivelse.pack(side="left", padx=20, pady=5)
        
        # Venstre ramme til input
        self.left_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Højre ramme til output
        self.right_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Bund bjælke
        bottombar = ctk.CTkFrame(self, fg_color="#e5e5e5", height=30, corner_radius=0)
        bottombar.grid(row=2, column=0, columnspan=2, sticky="ew")
        footer = ctk.CTkLabel(bottombar, text="Udviklet af Niels Graversgaard Pedersen, kontakt:", font=("Helvetica", 10))
        footer.pack(side="left", padx=(20,0))
        # LinkedIn knap (designet til at ligne et link)
        linkedin_url = "https://www.linkedin.com/in/niels-g-pedersen/" 
        github_url = "https://github.com/NielsGP/Bearing-Capacity-Calculator"
        
        btn_linkedin = ctk.CTkButton(
            bottombar,
            text="LinkedIn",
            font=("Helvetica", 10, "bold"),
            fg_color="transparent",     # Gør baggrunden gennemsigtig
            text_color="#0077b5",       # LinkedIn blå farve
            hover_color="#d1d1d1",      # Let grå ved mouse-over
            width=0,                    # Tilpas bredde til tekst
            height=20,
            cursor="hand2",             # Viser hånd-cursor (virker på nogle OS)
            command=lambda: webbrowser.open_new_tab(linkedin_url)
        )
        btn_linkedin.pack(side="left", padx=5)
        
        # GitHub knap (Dokumentation)
        btn_github = ctk.CTkButton(
            bottombar,
            text="| GitHub Dokumentation",
            font=("Helvetica", 10, "bold"),
            fg_color="transparent",
            text_color="#24292e",       # Klassisk GitHub mørkegrå/sort
            hover_color="#d1d1d1",
            width=0,
            height=20,
            cursor="hand2",
            command=lambda: webbrowser.open_new_tab(github_url)
        )
        btn_github.pack(side="right", padx=20)
        
        self.create_left_sections()
        self.create_right_section()

    def create_left_sections(self):
        result_header = ctk.CTkLabel(self.left_frame, text="Input", font=("Helvetica", 18, "bold"))
        result_header.pack(pady=(10, 5))
        
        geom_card = ctk.CTkFrame(self.left_frame, fg_color="#f2f2f2", corner_radius=10)
        geom_card.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(geom_card, text="Geometri", font=FONT_TITLE).pack(anchor="w", padx=10, pady=(5,2))
        self.funderingsform = ctk.StringVar(value="Stribe")
        self.combobox = ctk.CTkComboBox(geom_card, values=["Stribe", "Rektangulært", "Cirkulært"], variable=self.funderingsform, font=("Helvetica", 12), width=280, command=self.update_geometri)
        self.combobox.pack(pady=PAD_Y)
        self.combobox.set("Stribe")  # Set initial value
        self.geometry_container = ctk.CTkFrame(geom_card, fg_color="transparent")
        self.geometry_container.pack()
        self.geometry_frame = Geometri(self.geometry_container, self.funderingsform)
        self.geometry_frame.pack(pady=PAD_Y)

        styrke_card = ctk.CTkFrame(self.left_frame, fg_color="#f2f2f2", corner_radius=10)
        styrke_card.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(styrke_card, text="Styrkeparametre", font=FONT_TITLE).pack(anchor="w", padx=10, pady=(5,2))
        self.styrke_frame = Styrkeparametre(styrke_card)
        self.styrke_frame.pack(pady=5)   
        
        egen_card = ctk.CTkFrame(self.left_frame, fg_color="#f2f2f2", corner_radius=10)
        egen_card.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(egen_card, text="Egenvægt og Rumvægt", font=FONT_TITLE).pack(anchor="w", padx=10, pady=(5,2))
        self.egenvaegt_var = ctk.StringVar(value="Nej")
        ctk.CTkLabel(egen_card, text="Medregn fundaments egenvægt:", width=280, font=FONT_TEXT).pack(anchor="w", padx=10, pady=(5,2))
        self.egenvaegt_combobox = ctk.CTkComboBox(egen_card, values=["Ja", "Nej"], variable=self.egenvaegt_var, font=FONT_TEXT, width=280, command=self.update_egenvaegt)
        self.egenvaegt_combobox.pack(pady=PAD_Y)
        self.egenvaegt_combobox.set("Nej")  # Set initial value
        self.egenvaegt_container = None
        self.egenvaegt_frame = None
        self.rumvaegt_jord_frame = Rumvaegt_jord(egen_card)
        self.rumvaegt_jord_frame.pack(pady=(0, 5))

        last_card = ctk.CTkFrame(self.left_frame, fg_color="#f2f2f2", corner_radius=10)
        last_card.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(last_card, text="Lastpåvirkning", font=FONT_TITLE).pack(anchor="w", padx=10, pady=(5,2))
        self.laster_med_var = ctk.StringVar(value="Nej")
        self.laster_combobox = ctk.CTkComboBox(last_card, values=["Ja", "Nej"], variable=self.laster_med_var, font=FONT_TEXT, width=280, command=self.update_laster)
        self.laster_combobox.pack(pady=PAD_Y)
        self.laster_combobox.set("Nej")  # Set initial value
        self.laster_container = None
        self.laster_frame = None

        CC_card = ctk.CTkFrame(self.left_frame, fg_color="#f2f2f2", corner_radius=10)
        CC_card.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(CC_card, text="Anvendt sikkerhed", font=FONT_TITLE).pack(anchor="w", padx=10, pady=(5,2))
        self.konsekvensklasse = ctk.StringVar(value="CC2")
        self.CC_combobox = ctk.CTkComboBox(CC_card, values=["CC2", "CC3", "Ingen sikkerhed", "Vælg selv"], variable=self.konsekvensklasse, font=FONT_TEXT, width=280, command=self.update_CC)
        self.CC_combobox.pack(pady=PAD_Y)
        self.CC_combobox.set("CC2")  # Set initial value
        self.sikkerheder = ctk.CTkLabel(CC_card, text="(γ_cu: 1.8, γ_c': 1.2 og γ_φ: 1.2)", font=FONT_TEXT)
        self.sikkerheder.pack(pady=5)
        self.CC_container = None
        self.CC_frame = None

        
        # Knap til beregning
        self.button = ctk.CTkButton(self.left_frame, text="Beregn!", command=self.beregn, width=280)
        self.button.pack(pady=15)
        self.bind("<Return>", lambda event: self.beregn()) # Bind Enter (and keypad Enter) to run calculation
        self.bind("<KP_Enter>", lambda event: self.beregn()) # Use lambda to discard the event argument passed by the bind callback

    def create_right_section(self):
        result_header = ctk.CTkLabel(self.right_frame, text="Resultater", font=("Helvetica", 18, "bold"))
        result_header.pack(pady=(0, 5))
        figur_card = ctk.CTkFrame(self.right_frame, fg_color="#f2f2f2", corner_radius=10)
        figur_card.pack(fill="x", pady=8, padx=5)
        self.resultater = Resultater(figur_card)
        self.resultater.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.excen_card = ctk.CTkFrame(self.right_frame, fg_color="#f2f2f2", corner_radius=10)
        self.excen_card.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(self.excen_card, text="Effektiv geomtri", font=FONT_TITLE).pack(anchor="w", padx=10, pady=(5,2))
        self.geometry_res = Geometry_res(self.excen_card, self.funderingsform)
        self.geometry_res.pack(expand=True, fill="both", padx=10, pady=5)
        
        styrker_res_card = ctk.CTkFrame(self.right_frame, fg_color="#f2f2f2", corner_radius=10)
        styrker_res_card.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(styrker_res_card, text="Regningsmæssige styrker", font=FONT_TITLE).pack(anchor="w", padx=10, pady=(5,2))
        self.styrker_res = Styrker_res(styrker_res_card)
        self.styrker_res.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.drained_card = ctk.CTkFrame(self.right_frame, fg_color="#f2f2f2", corner_radius=10)
        self.drained_card.pack(fill="x", pady=8, padx=5)
        self.drained_header = ctk.CTkLabel(self.drained_card, text="Bæreevne i drænet tilstand", font=FONT_TITLE, justify="left")
        self.drained_header.pack(anchor="w", padx=10, pady=(5,2))
        self.drained_res = Drained_res(self.drained_card)
        self.drained_res.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.undrained_card = ctk.CTkFrame(self.right_frame, fg_color="#f2f2f2", corner_radius=10)
        self.undrained_card.pack(fill="x", pady=8, padx=5)
        self.undrained_header = ctk.CTkLabel(self.undrained_card, text="Bæreevne i udrænet tilstand", font=FONT_TITLE)
        self.undrained_header.pack(anchor="w", padx=10, pady=(5,2))
        self.undrained_res = Undrained_res(self.undrained_card)
        self.undrained_res.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # graceful close
    
    def beregn(self):
        """Collect inputs, calculate bearing capacity, and update results and sketch."""
        # Parse inputs and validate
        parsed = self.parse_inputs()
        if not parsed:
            # parse_inputs already shows an error message
            return

        # Draw the sketches (cross-section and top view)
        self.display_sketch(parsed)
        self.show_res(parsed)

    def parse_inputs(self):
        """Læser og validere input. Returnerer en dict med keys: 
        funderingsform, width, depth, water, phi, cu, c, gamma_cu, gamma_c, gamma_phi, egenvægt fundament, rumvægt jord 
        or None on error (and shows a messagebox).
        """
        geo_entries = self.geometry_frame.entries_1
        
        # Geometri
        f = self.funderingsform.get()
        laster = self.laster_med_var.get()
        try:
            if f == "Stribe":
                B = float(geo_entries["Bredde, B [m]:"].get())
                FUK = float(geo_entries["FUK [m u.t.]:"].get())
                VSP = float(geo_entries["Vandstand, VSP [m u.t.]:"].get())
                width = B
            elif f == "Rektangulært":
                B = float(geo_entries["Bredde, B [m]:"].get())
                # read length
                L = float(geo_entries["Længde, L [m]:"].get())
                FUK = float(geo_entries["FUK [m u.t.]:"].get())
                VSP = float(geo_entries["Vandstand, VSP [m u.t.]:"].get())
                width = B
                length = L
            else:  # Cirkulært
                D = float(geo_entries["Diameter, Ø [m]:"].get())
                FUK = float(geo_entries["FUK [m u.t.]:"].get())
                VSP = float(geo_entries["Vandstand, VSP [m u.t.]:"].get())
                width = D  # treat diameter as width for sketch
                length = D
        except Exception:
            messagebox.showerror(title="Fejl i input", message="Tjek geometri-input: brug tal (fx 0.5)")
            return None

        # Styrkeparametre
        str_entries = self.styrke_frame.entries_2
        try:
            phi = float(str_entries["φ [°]:"].get())
            cu = float(str_entries["c_u [kPa]:"].get())
            c = float(str_entries["c' [kPa]:"].get())
            R = float(str_entries["Ruhedsgrad:"].get())
        except Exception:
            messagebox.showerror(title="Fejl i input", message="Tjek styrkeparametre: brug tal (fx 20.5)")
            return None
        
        # Sikkerhedsfaktorer
        try:
            CC_entries = self.CC_frame.entries_CC
        except Exception:
            pass
        
        cc = self.konsekvensklasse.get()
        if cc == "CC2":
            gamma_cu = 1.8
            gamma_c = 1.2
            gamma_phi = 1.2
        elif cc == "CC3":
            gamma_cu = 1.98
            gamma_c = 1.32
            gamma_phi = 1.32
        elif cc == "Ingen sikkerhed":
            gamma_cu = 1.0
            gamma_c = 1.0
            gamma_phi = 1.0
        else:
            try:
                gamma_cu = float(CC_entries["γ_cu:"].get())
                gamma_c = float(CC_entries["γ_c':"].get())
                gamma_phi = float(CC_entries[f"γ_\u03C6:"].get())
            except Exception:
                messagebox.showerror(title="Fejl i input", message="Tjek partialkoefficienter: brug tal (fx 1.35)")
                return None
        
        
        # laster
        V, HB, HL, H, MB, ML = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 # default if not included

        if laster == "Ja" and self.laster_frame is not None:
            laster_entries = self.laster_frame.entries
            try:
                if f == "Rektangulært":
                    V = float(laster_entries["V [kN]:"].get())
                    HB = float(laster_entries["H_B [kN]:"].get())
                    HL = float(laster_entries["H_L [kN]:"].get())
                    MB = float(laster_entries["M_B [kNm]:"].get())
                    ML = float(laster_entries["M_L [kNm]:"].get())
                    H = calc.res_vandret_last(HB,HL)
                elif f == "Stribe":
                    V = float(laster_entries["V [kN/m]:"].get())
                    HB = float(laster_entries["H [kN/m]:"].get())
                    H = HB
                    MB = float(laster_entries["M [kNm/m]:"].get())
                else:
                    V = float(laster_entries["V [kN]:"].get())
                    HB = float(laster_entries["H [kN]:"].get())
                    H = HB
                    MB = float(laster_entries["M [kNm]:"].get())
            except Exception:
                messagebox.showerror(title="Fejl i input", message="Tjek laster: brug tal (fx 10.4)")
                return None
        
        # Rumvægt jord
        gamma = 0.0  # default if not included
        try:
            gamma = float(self.rumvaegt_jord_frame.entries["Tør jord, γ_d [kN/m3]:"].get())
            gamma_m = float(self.rumvaegt_jord_frame.entries["Mættet jord, γ_m [kN/m3]:"].get())
        except Exception:
            messagebox.showerror(title="Fejl i input", message="Tjek rumvægt: brug tal (fx 19.0)")
            return None
        
        # Egenvægt medregning
        rumvaegt_fundament = 0.0  # default if not included
        if 'length' not in locals():
            length = 1
        if self.egenvaegt_var.get() == "Ja" and self.egenvaegt_frame is not None:
            try:
                rumvaegt_fundament = float(self.egenvaegt_frame.entry.get())
                egenvaegt_fundament = calc.egenvaegt(f, FUK, width, length, rumvaegt_fundament)
                V = V + egenvaegt_fundament
                V_ef = V - calc.vandtryk(FUK, VSP, width, length)
            except Exception:
                messagebox.showerror(title="Fejl i input", message="Tjek egenvægt: brug tal (fx 24.0)")
                return None
        else:
            V_ef = V
        
        # Effektiv lodret last:
        
        
        if laster == "Ja":
            B_ef, L_ef, A_ef, e_B, e_L,_ = calc.excentricitet(self, V, MB, ML, width, length)
        else: 
            B_ef = width
            L_ef = length
            A_ef = width*length
            e_B = float(0)
            e_L = float(0)
        
        #Effektiv rumvægt og spændinger    
        gamma_ef, q_ef, q = calc.gamma_ef(gamma, gamma_m, FUK, VSP, B_ef)

        # basic sanity
        if width <= 0:
            messagebox.showerror(title="Fejl i input", message="Bredde/diameter skal være > 0")
            return None

        # default length for strip if not provided
        if 'length' not in locals() or length is None:
            # for a strip foundation show an elongated plan; choose 4x width as reasonable default
            length = max(width * 4, 1.0)

        return {
            "funderingsform": f,
            "B_ef": B_ef,
            "L_ef": L_ef,
            "A_ef": A_ef,
            "e_B": e_B,
            "e_L": e_L,
            "width": width,
            "depth": FUK,
            "water": VSP,
            "length": length,
            "phi": phi,
            "cu": cu,
            "c": c,
            "gamma_cu": gamma_cu, # sikkerheder --v
            "gamma_c": gamma_c,
            "gamma_phi": gamma_phi,
            "gamma": gamma, #rumvægte --v
            "gamma_m": gamma_m,
            "gamma_ef": gamma_ef,
            "gamma_g": rumvaegt_fundament,
            "q_ef": q_ef,
            "q": q,
            "V": V,
            "V_ef": V_ef,
            "HB": HB,
            "HL": HL,
            "H": H,
            "MB": MB,
            "ML": ML,
            "R": R,
        }
        
    def update_geometri(self, choice):
        # Destroy old frame inside container
        for widget in self.geometry_container.winfo_children():
            widget.destroy()
        
        # Create new Geometri inside the same container
        self.geometry_frame = Geometri(self.geometry_container, self.funderingsform)
        self.geometry_frame.pack(pady=PAD_Y)
        
        # Opdater resultatsektionen for effektiv geometri
        self.geometry_res.destroy()
        self.geometry_res = Geometry_res(self.excen_card, self.funderingsform)
        self.geometry_res.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.update_laster(self.laster_med_var.get())
        
    def update_egenvaegt(self, choice):
        # Destroy old frame if it exists
        if self.egenvaegt_frame:
            self.egenvaegt_frame.destroy()
            self.egenvaegt_frame = None
        if self.egenvaegt_container:
            self.egenvaegt_container.destroy()
            self.egenvaegt_container = None

        # Create new frame if needed
        if choice == "Ja":
            self.egenvaegt_container = ctk.CTkFrame(self.egenvaegt_combobox.master, fg_color="transparent")
            self.egenvaegt_container.pack(after=self.egenvaegt_combobox)
            self.egenvaegt_frame = Egenvaegt(self.egenvaegt_container)
            self.egenvaegt_frame.pack(pady=5)
        
    def update_laster(self, choice):
        # Destroy old frame if it exists
        if self.laster_frame:
            self.laster_frame.destroy()
            self.laster_frame = None
        if self.laster_container:
            self.laster_container.destroy()
            self.laster_container = None

        # Create new frame if needed
        if choice == "Ja":
            self.laster_container = ctk.CTkFrame(self.laster_combobox.master, fg_color="transparent")
            self.laster_container.pack(after=self.laster_combobox)
            self.laster_frame = Laster(self.laster_container, self.funderingsform)
            self.laster_frame.pack(pady=5)
 
    def update_CC(self, choice):
        # Destroy old frame and container if they exist
        if self.CC_frame:
            self.CC_frame.destroy()
            self.CC_frame = None
        if self.CC_container:
            self.CC_container.destroy()
            self.CC_container = None
        if hasattr(self, "sikkerheder"):
            self.sikkerheder.destroy()

        # Create new frame and container if needed
        if choice == "Vælg selv":
            self.CC_container = ctk.CTkFrame(self.CC_combobox.master, fg_color="transparent")
            self.CC_container.pack(after=self.CC_combobox)
            self.CC_frame = CC(self.CC_container)
            self.CC_frame.pack(pady=5)

        # Update safety factors label
        if choice == "CC2":
            text = "(γ_cu: 1.8, γ_c': 1.2 og γ_φ: 1.2)"
        elif choice == "CC3":
            text = "(γ_cu: 1.98, γ_c': 1.32 og γ_φ: 1.32)"
        elif choice == "Ingen sikkerhed":
            text = "(γ_cu: 1.0, γ_c': 1.0 og γ_φ: 1.0)"
        else:
            text = ""
    
        if text:
            self.sikkerheder = ctk.CTkLabel(self.CC_combobox.master, text=text, font=("Helvetica", 12))
            self.sikkerheder.pack(after=self.CC_combobox, pady=5)
        
    def on_close(self):
        plt.close('all')  # ensure no figures stay open
        self.destroy()
        
    def show_res(self, parsed):
        f = self.funderingsform.get()
        laster = self.laster_med_var.get()
        
        ## Geometri ---------------------------------
        B_ef, L_ef, A_ef, e_B, e_L, res = calc.excentricitet(self, parsed["V"], parsed["MB"], parsed["ML"], parsed["width"], parsed["length"])
        if f == "Stribe":
            self.geometry_res.label01.configure(text=f"{res} ⓘ (e = {e_B:.2f}) m)")
            self.geometry_res.label11.configure(text=f"B' = {B_ef:.2f} m")
            self.geometry_res.label21.configure(text=f"A' = {A_ef:.2f} m^2/m")
        elif f == "Cirkulært":
            self.geometry_res.label01.configure(text=f"{res} ⓘ (e = {e_B:.2f}) m)")
            self.geometry_res.label11.configure(text=f"B' = {B_ef:.2f} m")
            self.geometry_res.label21.configure(text=f"L' = {L_ef:.2f} m")
            self.geometry_res.label31.configure(text=f"A' = {A_ef:.2f} m^2")
        else:
            self.geometry_res.label01.configure(text=f"{res} ⓘ (e_B = {e_B:.2f} m, e_L = {e_L:.2f} m)")
            self.geometry_res.label11.configure(text=f"B' = {B_ef:.2f} m")
            self.geometry_res.label21.configure(text=f"L' = {L_ef:.2f} m")
            self.geometry_res.label31.configure(text=f"A' = {A_ef:.2f} m^2")
        
        ## Regningsmæssige styrker ---------------------------------
        self.styrker_res.label01.configure(text=f"{math.degrees(np.atan(np.tan(math.radians(parsed["phi"]))/parsed["gamma_phi"])):.2f}°")
        self.styrker_res.label11.configure(text=f"{parsed["cu"]/parsed["gamma_cu"]:.2f} kPa")
        self.styrker_res.label21.configure(text=f"{parsed["c"]/parsed["gamma_c"]:.2f} kPa")

        ## Drænet Bæreevne ---------------------------------
        # Bæreevnefaktorer
        Ng, Nc, Nq = calc.N_faktor(parsed)
        self.drained_res.label01.configure(text=f"N_γ = {Ng:.2f}")
        self.drained_res.label02.configure(text=f"N_c = {Nc:.2f}")
        self.drained_res.label03.configure(text=f"N_q = {Nq:.2f}")
        sg, sc, sq = calc.s_faktor(f, parsed["B_ef"], parsed["L_ef"])
        self.drained_res.label11.configure(text=f"s_γ = {sg:.2f}")
        self.drained_res.label12.configure(text=f"s_c = {sc:.2f}")
        self.drained_res.label13.configure(text=f"s_q = {sq:.2f}")
        ig, ic, iq = calc.i_faktor(f, parsed)
        self.drained_res.label21.configure(text=f"i_γ = {ig:.2f}")
        self.drained_res.label22.configure(text=f"i_c = {ic:.2f}")
        self.drained_res.label23.configure(text=f"i_q = {iq:.2f}")
        
        # drænet lodret bæreevne
        R_Rd, R_Rd_A = calc.drained_bearing_cap(parsed, Ng, sg, ig, Nq, sq, iq, Nc, sc, ic)
        lodret_tekst_1 = f"R_Rd = {R_Rd:.1f} kN/m" if f == "Stribe" else f"R_Rd = {R_Rd:.1f} kN"
        self.drained_res.label31.configure(text=f"R_Rd/A' = {R_Rd_A:.1f} kN/m2")
        self.drained_res.label32.configure(text=lodret_tekst_1)
        if parsed["V"] < R_Rd:
            kontrol_R_drained = f"≥ V_Ed = {parsed["V"]:.1f} kN/m   OK!" if f == "Stribe" else f"≥ V_Ed = {parsed["V"]:.1f} kN   OK!"
            self.drained_res.label33.configure(text=f"{kontrol_R_drained}")
        else:
            kontrol_R_drained = f"< V_Ed = {parsed["V"]:.1f} kN/m   EJ OK!" if f == "Stribe" else f"< V_Ed = {parsed["V"]:.1f} kN   EJ OK!"
            self.drained_res.label33.configure(text=f"{kontrol_R_drained}")
            
        # drænet vandret bæreevne
        vandret_bæreevne_d = calc.drained_bearing_cap_hor(parsed)
        vandret_tekst_d = f"V'_d tan(\u03B4_d) = {vandret_bæreevne_d:.1f} kN/m" if f == "Stribe" else f"V'_d*tan(\u03B4_d) = {vandret_bæreevne_d:.1f} kN"
        self.drained_res.label41.configure(text=vandret_tekst_d)
        if parsed["H"] <= vandret_bæreevne_d:
            kontrol_H_drained = f"≥ H_Ed = {parsed["H"]:.1f} kN/m   OK!" if f == "Stribe" else f"≥ H_Ed = {parsed["H"]:.1f} kN   OK!"
            self.drained_res.label43.configure(text=f"{kontrol_H_drained}")
        else:
            kontrol_H_drained = f"< H_Ed = {parsed["H"]:.1f} kN/m   EJ OK!" if f == "Stribe" else f"< H_Ed = {parsed["H"]:.1f} kN   EJ OK!"
            self.drained_res.label43.configure(text=f"{kontrol_H_drained}")   
        
        # Farveskift hvis enten vandret eller lodret ikke er OK
        if ("EJ OK!" in kontrol_R_drained or "EJ OK!" in kontrol_H_drained):
            self.drained_card.configure(fg_color="#fd9620")
        else:
            self.drained_card.configure(fg_color="#b4f7b4")
        
            
        ## Udrænet Bæreevne  ---------------------------------
        # Bæreevnefaktorer
        Nc0, sc0, ic0 = calc.udr_faktorer(f, parsed["B_ef"], parsed["L_ef"], parsed["H"], parsed["A_ef"], parsed["cu"]) 
        self.undrained_res.label01.configure(text=f"N_c0 = {Nc0:.2f}")
        self.undrained_res.label11.configure(text=f"s_c0 = {sc0:.2f}")
        self.undrained_res.label21.configure(text=f"i_c0 = {ic0:.2f}")
        
        # Kontrol af behov for eftervisning af udrænet bæreevne
        if parsed["cu"] == 0 and parsed["c"] == 0:
            self.undrained_header.configure(text="Bæreevne i udrænet tilstand (Angivet jord er friktionsjord. Se bort fra udrænet bæreevne)")
        elif parsed["cu"] == 0:
            self.undrained_header.configure(text="Bæreevne i udrænet tilstand (cu = 0)")
        else:
            self.undrained_header.configure(text="Bæreevne i udrænet tilstand")
        
        # udrænet lodret bæreevne
        R_Rd, R_Rd_A = calc.undrained_bearing_cap(parsed, Nc0, sc0, ic0)
        lodret_tekst_2 = f"R_Rd = {R_Rd:.1f} kN/m" if f == "Stribe" else f"R_Rd = {R_Rd:.1f}"
        self.undrained_res.label31.configure(text=f"R_Rd/A' = {R_Rd_A:.1f} kN/m2")
        self.undrained_res.label32.configure(text=lodret_tekst_2)
        if parsed["V"] <= R_Rd:
            kontrol_R_undrained = f"≥ V_Ed = {parsed["V"]} kN/m   OK!" if f == "Stribe" else f"≥ V_Ed = {parsed["V"]} kN   OK!"
            self.undrained_res.label33.configure(text=f"{kontrol_R_undrained}")
        else:
            kontrol_R_undrained = f"< V_Ed = {parsed["V"]} kN/m   EJ OK!" if f == "Stribe" else f"< V_Ed = {parsed["V"]} kN   EJ OK!"
            self.undrained_res.label33.configure(text=f"{kontrol_R_undrained}")
        
        # udrænet vandret bæreevne
        undrained_hor_cap_1 = (parsed["cu"]/parsed["gamma_cu"])*parsed["A_ef"]
        undrained_hor_cap_2 = 0.4*parsed["V"]
        vandret_tekst_1 = f"min(A' c_ud = {undrained_hor_cap_1:.1f} kN/m ;" if f == "Stribe" else f"min(A' c_ud = {undrained_hor_cap_1:.1f} kN ;"
        vandret_tekst_2 = f"0.4V = {undrained_hor_cap_2:.1f} kN/m)" if f == "Stribe" else f"0.4V = {undrained_hor_cap_2:.1f} kN)"
        self.undrained_res.label41.configure(text=vandret_tekst_1)
        self.undrained_res.label42.configure(text=vandret_tekst_2)
        if parsed["H"] <= min(undrained_hor_cap_1, undrained_hor_cap_2):
            kontrol_H_undrained = f"≥ H_Ed = {parsed["H"]} kN/m   OK!" if f == "Stribe" else f"≥ H_Ed = {parsed["V"]} kN   OK!"
            self.undrained_res.label43.configure(text=f"{kontrol_H_undrained}")
        else:
            kontrol_H_undrained = f"< H_Ed = {parsed["H"]:.1f} kN/m   EJ OK!" if f == "Stribe" else f"< H_Ed = {parsed["H"]:.1f} kN   EJ OK!"
            self.undrained_res.label43.configure(text=f"{kontrol_H_undrained}")
        
        # Farveskift hvis enten vandret eller lodret ikke er OK
        if ("EJ OK!" in kontrol_R_undrained or "EJ OK!" in kontrol_H_undrained):
            self.undrained_card.configure(fg_color="#fd9620")
        else:
            self.undrained_card.configure(fg_color="#b4f7b4")

    def display_sketch(self, parsed):
        f = parsed["funderingsform"]
        width = parsed["width"]
        depth = parsed["depth"]
        water = parsed["water"]
        length = parsed.get("length", None)
        V = parsed["V"]
        HB = parsed["HB"]
        HL = parsed["HL"]
        H = parsed["H"]
        MB = parsed["MB"]
        ML = parsed["ML"]
        
        f = self.funderingsform.get()
        laster = self.laster_med_var.get()
        
        if laster == "Ja":
            width_ef, length_ef, area_ef, e_B, e_L,_ = calc.excentricitet(self, parsed["V"], parsed["MB"], parsed["ML"], parsed["width"], parsed["length"])
            
        # Safety: avoid zero or extremely small widths that break plotting limits
        if width <= 0:
            width = 0.1

        # Destroy previous canvases if present
        if self.resultater.canvas:
            try:
                self.resultater.canvas.get_tk_widget().destroy()
            except Exception:
                pass
        if self.resultater.canvas_top:
            try:
                self.resultater.canvas_top.get_tk_widget().destroy()
            except Exception:
                pass
        # ========== FIG_LEFT (cross-section) ==========
        fig_left, ax_left = plt.subplots(figsize=(4,4))

        x_lim = width+(width+2*depth)/3
        y_lim_l = -depth-depth/2
        y_lim_u = width*0.4+0.4
        
        # Ground line
        ax_left.plot([-x_lim, x_lim], [0,0], color="black")
        soil = Rectangle(
            (-x_lim, y_lim_l/10),       # start below ground
            2*x_lim,                    # full width
            -y_lim_l/10,                # height
            facecolor="none",           # transparent fill
            hatch="\\\\",               # diagonal other direction
            linewidth=0.5,
            zorder=0)
        ax_left.add_patch(soil)

        # Fundament (use Rectangle from patches)
        rect = Rectangle(
            (-width/2, -depth),
            width,
            depth,
            facecolor="lightgrey",
            edgecolor="black",
            linewidth=1,
            zorder=1)
        ax_left.add_patch(rect)
        
        # Vandspejl
        ax_left.axhline(-water, color="blue", linestyle="--", linewidth=2)
        if depth - width*0.1 < water < depth + width*0.1:
            ax_left.text(width*0.7, -water, f"VSP = -{water:.2f} m", va="bottom", fontsize=10, color="blue")
        else:
            ax_left.text(-width*0.7, -water, f"VSP = -{water:.2f} m", va="bottom", ha="right", fontsize=10, color="blue")
        ax_left.text(-width*0.7, -depth, f"FUK = -{depth:.2f} m", ha="right", va="bottom", fontsize=10)
        
        # vis rumvægt
        ax_left.text((x_lim+width/2)/2, -depth/2, f"γ_d/γ_m =\n {parsed["gamma"]:.2f}/{parsed["gamma_m"]:.2f} kN/m3", va="center", ha="center", fontsize=10, color="#b3b1b1")
        if parsed["gamma_g"] != 0:
            ax_left.text(0, -depth/2, f"γ_g =\n {parsed["gamma_g"]:.2f} kN/m^3", va="center", ha="center", fontsize=10, color="#b3b1b1")

        ax_left.set_xlim(-x_lim, x_lim)
        ax_left.set_ylim(y_lim_l, y_lim_u)
        ax_left.set_aspect("equal")
        ax_left.axis("off")

        # --- MÅLLINJE FOR BREDDE ---
        y_dim = -depth-0.3  # lidt under FUK
        ax_left.plot([-width/2, width/2], [y_dim, y_dim], color="black")  # main line
        ax_left.plot([-width/2, -width/2], [y_dim-0.1, y_dim+0.1], color="black") # venstre "hak"
        ax_left.plot([width/2, width/2], [y_dim-0.1, y_dim+0.1], color="black")   # højre "hak"
        if f == "Cirkulært":
            ax_left.text(0, y_dim-0.2, f"Ø = {width:.2f} m", ha="center", va="top", fontsize=10)
        else:
            ax_left.text(0, y_dim-0.2, f"B = {width:.2f} m", ha="center", va="top", fontsize=10)

        # Horisontal force (H)
        if H != 0:
            arrow_len = width * 0.6
            ax_left.arrow(arrow_len, 0, -arrow_len, 0, head_width=width*0.1, head_length=width*0.1,
                        fc="red", ec="red", linewidth=2, length_includes_head=True, zorder=5)
            label_H = f"H = {H:.1f} kN"
            ax_left.text(arrow_len - arrow_len/2, 0.1*width, label_H, color="red",
                        fontsize=9, va="center", ha="left")

        # Vertical force (V)
        if V != 0:
            arrow_len = width * 0.6
            ax_left.arrow(0, arrow_len, 0, -arrow_len, head_width=width*0.1, head_length=width*0.1,
                        fc="red", ec="red", linewidth=2, length_includes_head=True, zorder=5)
            label_V = f"V = {V:.1f} kN/m" if f == "Stribe" else f"V = {V:.1f} kN"
            ax_left.text(0.1*width, arrow_len - arrow_len/2, label_V, color="red",
                        fontsize=9, va="center", ha="left")

        # Moment around lengthwise axis (MB) — draw a curved arrow above foundation
        if MB != 0:
            arc_center_y = 0.3
            radius = width * 0.4
            theta = np.linspace(np.pi/6, 5*np.pi/6, 40)
            ax_left.plot(radius * np.cos(theta), arc_center_y + radius * np.sin(theta),
                        color="purple", linewidth=2, zorder=10)
            # Add arrowhead to curved arrow
            ax_left.arrow(radius * np.cos(theta[35]), arc_center_y + radius * np.sin(theta[35]), 0.1*np.cos(theta[30]), -0.1*np.sin(theta[30]), head_width=width*0.10, head_length=width*0.10, fc="purple", ec="purple", zorder=11)
            label_MB = f"M = {MB:.1f} kNm/m" if f == "Stribe" else f"M_B = {MB:.1f} kNm"
            ax_left.text(0, arc_center_y + radius*1.1, label_MB, color="purple", fontsize=9, ha="center", va="bottom", zorder=9)


        # ========== FIG_TOP (plan view) ==========
        # Ensure length is set
        if f == "Stribe":
            length = width * 4

        fig_top, ax_right = plt.subplots(figsize=(4,4))
        
        if f == "Cirkulært":
            circ = Circle((0, 0), radius=width/2, facecolor="lightgrey", edgecolor="black", zorder=1)
            ax_right.add_patch(circ)
            ax_right.set_xlim(-width*0.75, width*0.75)
            ax_right.set_ylim(-width*0.75, width*0.75)
            
            if laster == "Ja":
                width_ef, length_ef, _, e_B, _, _= calc.excentricitet(self, parsed["V"], parsed["MB"], parsed["ML"], parsed["width"], parsed["length"])
                R = width/2
                # Create a grid of points over the circle
                n = 400
                x = np.linspace(-R, R, n)
                y = np.linspace(-R, R, n)
                X, Y = np.meshgrid(x, y)

                # Mask for original circle (center 0,0)
                inside_main = X**2 + Y**2 <= R**2
                # Mask for shifted circle (center at (0, e))
                inside_shifted = X**2 + (Y - e_B)**2 <= R**2
                # Intersection = effective contact area
                effective_mask = inside_main & inside_shifted

                # Plot as a hashed overlay
                ax_right.contourf(
                    X, Y, effective_mask,
                    levels=[0.5, 1],
                    hatches=["///"], colors="none", zorder=3
                )
                # Geometric center (foundation)
                ax_right.plot(0, 0, marker="+", color="black", markersize=10, label="Geometrisk centrum", zorder=6)
                # Eccentric load center (shifted upward)
                ax_right.plot(0, e_B, marker="o", color="black", markersize=10, label="Lastcentrum", zorder=7)

                # Stiblet linje omkring effektivt areal
                theta = np.linspace(0, 2*np.pi, 400)
                x_shifted = R * np.cos(theta)
                y_shifted = e_B + R * np.sin(theta)

                # Keep only points inside main circle
                mask_inside = x_shifted**2 + y_shifted**2 <= R**2
                x_clipped = x_shifted[mask_inside]
                y_clipped = y_shifted[mask_inside]

                ax_right.plot(x_clipped, y_clipped, color="gray", linestyle="--", linewidth=1, zorder=4)

        else:
            # Draw rectangle with length along x-axis, width along y-axis
            rect_top = Rectangle(
                (-length/2, -width/2), 
                length, width, 
                facecolor="lightgrey", 
                edgecolor="black", 
                zorder=1)
            ax_right.add_patch(rect_top)
            if laster == "Ja":
                width_ef, length_ef, _, _, _, _ = calc.excentricitet(self, parsed["V"], parsed["MB"], parsed["ML"], parsed["width"], parsed["length"])
                length_ef = width*4 if f == "Stribe" else length_ef
                rect_exc = Rectangle(
                    (-length/2+(length-length_ef), -width/2+(width-width_ef)), #øverste venstre hjørne
                    length_ef, width_ef, 
                    facecolor="lightgrey", 
                    hatch="///",
                    edgecolor="grey",
                    zorder=2)
                ax_right.add_patch(rect_exc)
            rect_top = Rectangle(
                (-length/2, -width/2), 
                length, width, 
                edgecolor="black", 
                zorder=1)
            if width > length:
                lim = width*0.75
            else:
                lim = length*0.75
            ax_right.set_xlim(-lim, lim)
            ax_right.set_ylim(-lim, lim)

        
        # --- MÅLLINJER FOR LÆNGDE, BREDDE OG DIAMETER ---
        # Use axis limits to compute dimension-line positions so they remain inside the plotting area
        xlim = ax_right.get_xlim()
        ylim = ax_right.get_ylim()
        tick_len = (ylim[1] - ylim[0]) * 0.03
        x_dim = -(xlim[1] - (xlim[1] - xlim[0]) * 0.04)
        y_dim = -width*1.2 if f == "Stribe" else -(ylim[1] - (ylim[1] - ylim[0]) * 0.04)
        
        if f == "Cirkulært":
            # diameter across center
            ax_right.plot([-width/2, width/2], [width*0.6, width*0.6], color="black", zorder=2)
            ax_right.plot([-width/2, -width/2], [-tick_len+width*0.6, tick_len+width*0.6], color="black", zorder=2)
            ax_right.plot([width/2, width/2], [-tick_len+width*0.6, tick_len+width*0.6], color="black", zorder=2)
            ax_right.text(0, width*0.6+width*0.02, f"Ø = {width:.2f} m", ha="center", va="bottom", fontsize=10, zorder=2)
            if laster == "Ja":
                ax_right.plot([x_dim, x_dim], [0, e_B], color="black", zorder=2)
                ax_right.plot([x_dim - tick_len, x_dim + tick_len], [0, 0], color="black", zorder=2)
                ax_right.plot([x_dim - tick_len, x_dim + tick_len], [e_B, e_B], color="black", zorder=2)
                ax_right.text(x_dim + tick_len * 0.6, e_B/2, f"e = {e_B:.2f} m", ha="left", va="center", fontsize=10, rotation=-90, zorder=2)
                
        else:
            # horizontal (length) dimension: place just inside top ylim
            ax_right.plot([-length/2, length/2], [y_dim, y_dim], color="black", zorder=2)
            ax_right.plot([-length/2, -length/2], [y_dim - tick_len, y_dim + tick_len], color="black", zorder=2)
            ax_right.plot([length/2, length/2], [y_dim - tick_len, y_dim + tick_len], color="black", zorder=2)
            if f == "Stribe":
                length_text = "L = ∞"
            else:
                length_text = f"L = {length:.2f} m"
            ax_right.text(0, y_dim - tick_len * 0.6, length_text, ha="center", va="top", fontsize=9, zorder=2)

            # vertical (width) dimension: place just inside right xlim
            ax_right.plot([x_dim, x_dim], [-width/2, width/2], color="black", zorder=2)
            ax_right.plot([x_dim - tick_len, x_dim + tick_len], [-width/2, -width/2], color="black", zorder=2)
            ax_right.plot([x_dim - tick_len, x_dim + tick_len], [width/2, width/2], color="black", zorder=2)
            ax_right.text(x_dim + tick_len * 0.6, 0, f"B = {width:.2f} m", ha="left", va="center", fontsize=9, rotation=-90, zorder=2)

            # Effektiv bredde og længde
            if laster == "Ja":
                y_dim = -y_dim
                x_dim = -x_dim
                if f == "Rektangulært":
                    right_x = length/2
                    left_x = length/2-length_ef
                    ax_right.plot([left_x, right_x], [y_dim, y_dim], color="black", zorder=2)
                    ax_right.plot([left_x, left_x], [y_dim - tick_len, y_dim + tick_len], color="black", zorder=2)
                    ax_right.plot([right_x, right_x], [y_dim - tick_len, y_dim + tick_len], color="black", zorder=2)
                    ax_right.text((right_x+left_x)/2, y_dim + tick_len * 0.6, f"L' = {length_ef:.2f} m", ha="center", va="bottom", fontsize=9, zorder=2)
                top_y = width/2
                bottom_y = width/2-width_ef
                ax_right.plot([x_dim, x_dim], [top_y, bottom_y], color="black", zorder=2)
                ax_right.plot([x_dim - tick_len, x_dim + tick_len], [bottom_y, bottom_y], color="black", zorder=2)
                ax_right.plot([x_dim - tick_len, x_dim + tick_len], [top_y, top_y], color="black", zorder=2)
                ax_right.text(x_dim + tick_len * 0.6, (top_y+bottom_y)/2, f"B' = {width_ef:.2f} m", ha="left", va="center", rotation=-90, fontsize=9, zorder=2)

        # Horizontal force HL (x-direction)
        if HL != 0:
            ax_right.arrow(0, 0, width*0.4, 0, head_width=width*0.05, head_length=width*0.05,
                        fc="red", ec="red", linewidth=2, length_includes_head=True, zorder=5)
            ax_right.text(width*0.2, width*0.02, f"H_L = {HL:.1f} kN", color="red",
                        fontsize=9, va="bottom", ha="left")

        # Horizontal force HL (y-direction)
        if HB != 0:
            if f == "Stribe":
                y_load = width * 0.3
                n_arrows = 15
                x_positions = np.linspace(-length/2, length/2, n_arrows)
                for x in x_positions:
                    ax_right.plot([-length/2, length/2], [-width/2 - 0.3, -width/2 - 0.3], color="red", linewidth=1.5)
                    ax_right.arrow(x, -width/2-y_load, 0, 0.25, head_width=width*0.05, head_length=width*0.05,
                        fc="red", ec="red", linewidth=1.5, length_includes_head=True, zorder=6)
                    ax_right.text(0, -width/2-y_load - 0.15, f"H = {HB:.1f} kN/m", color="red",
                        fontsize=9, ha="center", va="top", zorder=7)
            else:  
                ax_right.arrow(0, 0, 0, width*0.4, head_width=width*0.05, head_length=width*0.05,
                        fc="red", ec="red", linewidth=2, length_includes_head=True, zorder=5)
                ax_right.text(-width*0.02, width*0.2, f"H_B = {HB:.1f} kN", color="red",
                        fontsize=9, ha="right", va="center")

        # Draw MB (moment around length axis)
        if MB != 0:
            if f == "Stribe":
                ax_right.arrow(length*0.2, 0, -length*0.4, 0, head_width=length*0.05, head_length=length*0.05,
                            fc="purple", ec="purple", linewidth=2, length_includes_head=True, zorder=5)
                # Two small dash marks across the circle to symbolize the right-hand rule
                dash_start = [length*0.02-length*0.02, length*0.02+length*0.02]
                dash_end = [-length*0.05, length*0.05]
                ax_right.plot(dash_start, dash_end, color="purple", linewidth=2)
                dash_x = [-length*0.02-length*0.02, -length*0.02+length*0.02]
                dash_y = [-length*0.05, length*0.05]
                ax_right.plot(dash_x, dash_y, color="purple", linewidth=2)
                label_MB = f"M = {MB:.1f} kNm/m"
                ax_right.text(0, length*0.05, label_MB,
                        color="purple", fontsize=9, ha="center", va="bottom")
            else:
                ax_right.arrow(0, 0, -width*0.4, 0, head_width=width*0.05, head_length=width*0.05,
                            fc="purple", ec="purple", linewidth=2, length_includes_head=True, zorder=5)
                # Two small dash marks across the circle to symbolize the right-hand rule
                dash_start = [-width*0.18-width*0.02, -width*0.18+width*0.02]
                dash_end = [-width*0.1, width*0.1]
                ax_right.plot(dash_start, dash_end, color="purple", linewidth=2)
                dash_x = [-width*0.22-width*0.02, -width*0.22+width*0.02]
                dash_y = [-width*0.1, width*0.1]
                ax_right.plot(dash_x, dash_y, color="purple", linewidth=2)
                label_MB = f"M_B = {MB:.1f} kNm"
                ax_right.text(width*0.02, -width*0.2, label_MB,
                        color="purple", fontsize=9, ha="right", va="bottom")

        # Draw ML (moment around width axis)
        if ML != 0:
                ax_right.arrow(0, -width*0.4, 0, width*0.4, head_width=width*0.05, head_length=width*0.05,
                    fc="purple", ec="purple", linewidth=2, length_includes_head=True, zorder=5)
                # Two small dash marks across the circle to symbolize the right-hand rule
                dash_y = [-width*0.18-width*0.02, -width*0.18+width*0.02]
                dash_x = [-width*0.05, width*0.05]
                ax_right.plot(dash_x, dash_y, color="purple", linewidth=2)
                dash_y = [-width*0.22-width*0.02, -width*0.22+width*0.02]
                dash_x = [-width*0.05, width*0.05]
                ax_right.plot(dash_x, dash_y, color="purple", linewidth=2)
                ax_right.text(width*0.02, -width*0.2, f"M_L = {MB:.1f} kNm",
                    color="purple", fontsize=9, ha="left", va="bottom")
        
        ax_right.set_aspect("equal")
        ax_right.axis("off")

        # Place left (cross-section) and right (top-view) canvases side-by-side
        
        if hasattr(self.resultater, "toolbar_frame_left") and self.resultater.toolbar_frame_left:
            self.resultater.toolbar_frame_left.destroy()
        
        self.plot_titel_left = ctk.CTkLabel(self.resultater, text="Snittegning:", font=FONT_TITLE)
        self.plot_titel_left.grid(column=0, row=0, padx=10, pady=(5,2), sticky="w")
        self.resultater.canvas = FigureCanvasTkAgg(fig_left, master=self.resultater.canvas_frame_left)
        self.resultater.canvas.draw()
        self.resultater.canvas.get_tk_widget().pack(expand=True, fill="both", pady=5, padx=5, anchor="center")
        self.resultater.toolbar_frame_left = ctk.CTkFrame(self.resultater.canvas_frame_left, fg_color="transparent")
        self.resultater.toolbar_frame_left.pack(side="bottom", fill="x", padx=5, pady=5)

        self.resultater.toolbar = NavigationToolbar2Tk(self.resultater.canvas, self.resultater.toolbar_frame_left)
        self.resultater.toolbar.config(background="white")
        self.resultater.toolbar._message_label.config(background="white")
        for i, child in enumerate(self.resultater.toolbar.winfo_children()):
            if i in [1, 2, 6]:  # Index 1 er 'Back', Index 2 er 'Forward'
                child.pack_forget()  # Skjuler knappen fra visningen
            else:
                # Gør de resterende knapper (Home, Pan, Zoom, Save) hvide
                child.config(background="white")
        self.resultater.toolbar.update()
        
        if hasattr(self.resultater, "toolbar_frame_right") and self.resultater.toolbar_frame_right:
            self.resultater.toolbar_frame_right.destroy()

        self.plot_titel_right = ctk.CTkLabel(self.resultater, text="Plantegning:", font=FONT_TITLE)
        self.plot_titel_right.grid(column=1, row=0, padx=10, pady=(5,2), sticky="w")
        self.resultater.canvas_top = FigureCanvasTkAgg(fig_top, master=self.resultater.canvas_frame_right)
        self.resultater.canvas_top.draw()
        self.resultater.canvas_top.get_tk_widget().pack(expand=True, fill="both", pady=5, padx=5, anchor="center")
        self.resultater.toolbar_frame_right = ctk.CTkFrame(self.resultater.canvas_frame_right, fg_color="transparent")
        self.resultater.toolbar_frame_right.pack(side="bottom", fill="x", padx=5, pady=5)

        self.resultater.toolbar = NavigationToolbar2Tk(self.resultater.canvas_top, self.resultater.toolbar_frame_right)
        self.resultater.toolbar.config(background="white")
        self.resultater.toolbar._message_label.config(background="white")
        for i, child in enumerate(self.resultater.toolbar.winfo_children()):
            if i in [1, 2, 6]:  # Index 1 er 'Back', Index 2 er 'Forward'
                child.pack_forget()  # Skjuler knappen fra visningen
            else:
                # Gør de resterende knapper (Home, Pan, Zoom, Save) hvide
                child.config(background="white")
        self.resultater.toolbar.update()

        plt.close(fig_left)
        plt.close(fig_top)
 
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
                  
if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        import traceback, tkinter.messagebox as messagebox
        traceback.print_exc()
        try:
            messagebox.showerror("Fejl ved opstart", f"Uventet fejl:\n{e}")
        except Exception:
            # If GUI can't start, just exit after printing traceback
            pass