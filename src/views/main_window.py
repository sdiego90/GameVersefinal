# src/views/main_window.py
import tkinter as tk
from tkinter import ttk
from src.utils.theme import Theme
from src.views.catalog_view import CatalogView
from src.views.account_view import AccountView


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GameVerse")
        self.geometry("1200x800")
        self.configure(bg=Theme.BG_DARK)

        self._setup_navigation()
        self._setup_main_frame()

        # Inicialmente mostrar el catálogo
        self.show_catalog()

    def _setup_navigation(self):
        # Barra de navegación
        nav_frame = tk.Frame(self, bg=Theme.BG_SECONDARY, height=60)
        nav_frame.pack(fill=tk.X, side=tk.TOP)
        nav_frame.pack_propagate(False)

        # Logo
        logo_label = tk.Label(nav_frame, text="GameVerse",
                              font=Theme.TITLE_FONT,
                              bg=Theme.BG_SECONDARY,
                              fg=Theme.ACCENT)
        logo_label.pack(side=tk.LEFT, padx=20)

        # Botones de navegación
        catalog_btn = tk.Button(nav_frame, text="Catálogo",
                                font=Theme.NORMAL_FONT,
                                bg=Theme.BG_SECONDARY,
                                fg=Theme.TEXT_PRIMARY,
                                bd=0,
                                command=self.show_catalog)
        catalog_btn.pack(side=tk.LEFT, padx=10)

        account_btn = tk.Button(nav_frame, text="Mi Cuenta",
                                font=Theme.NORMAL_FONT,
                                bg=Theme.BG_SECONDARY,
                                fg=Theme.TEXT_PRIMARY,
                                bd=0,
                                command=self.show_account)
        account_btn.pack(side=tk.LEFT, padx=10)

    def _setup_main_frame(self):
        self.main_frame = tk.Frame(self, bg=Theme.BG_DARK)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_catalog(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        catalog = CatalogView(self.main_frame)
        catalog.pack(fill=tk.BOTH, expand=True)

    def show_account(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        account = AccountView(self.main_frame)
        account.pack(fill=tk.BOTH, expand=True)