# views/catalog_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from src.utils.theme import Theme
from .sales_stats import register_sale


class CatalogView(tk.Frame):

    def _sell_game(self):
        selected = self.game_tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un juego para vender")
            return

        item = self.game_tree.item(selected[0])
        game_name = item['values'][0]

        # Obtener datos completos del juego
        game_data = self.df[self.df['Nombre'] == game_name].iloc[0]

        sell_window = SellGameWindow(self, game_data)
        sell_window.grab_set()
        # Esperar a que se cierre la ventana
        self.wait_window(sell_window)
        # Recargar datos
        self.df = pd.read_excel('data/games.xlsx')
        self._update_tree(self.df)

    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BG_DARK)
        self.df = None
        self._setup_filters()
        self._setup_game_list()
        self._load_excel_data()
        self._load_games()

    def _load_excel_data(self):
        try:
            # Leer el archivo Excel directamente
            self.df = pd.read_excel('data/games.xlsx')

            # Renombrar las columnas según los nombres exactos del Excel
            self.df.columns = ['Nombre', 'ID del Juego', 'Marca', 'Clasificación',
                               'Plataformas Disponibles', 'Precio Base', 'Stock']

            # Limpiar los datos
            self.df = self.df.fillna('')  # Rellenar valores NaN

            # Convertir precios a float y stock a int
            self.df['Precio Base'] = pd.to_numeric(self.df['Precio Base'], errors='coerce')
            self.df['Stock'] = pd.to_numeric(self.df['Stock'], errors='coerce')

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo Excel: {str(e)}")
            print(f"Error detallado: {e}")

    def _setup_filters(self):
        filter_frame = tk.Frame(self, bg=Theme.BG_SECONDARY, pady=10, padx=10)
        filter_frame.pack(fill=tk.X)

        # Filtro de desarrolladora/marca
        marca_frame = tk.Frame(filter_frame, bg=Theme.BG_SECONDARY)
        marca_frame.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(marca_frame, text="Desarrolladora:",
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY,
                 font=Theme.NORMAL_FONT).pack(side=tk.LEFT, padx=5)

        self.marca_var = tk.StringVar()
        self.marca_cb = ttk.Combobox(marca_frame, textvariable=self.marca_var, width=20)
        self.marca_cb.pack(side=tk.LEFT)
        self.marca_cb.bind('<<ComboboxSelected>>', self._apply_filters)

        # Filtro de precio
        price_frame = tk.Frame(filter_frame, bg=Theme.BG_SECONDARY)
        price_frame.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(price_frame, text="Precio máximo:",
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY,
                 font=Theme.NORMAL_FONT).pack(side=tk.LEFT, padx=5)

        self.price_var = tk.StringVar()
        self.price_entry = tk.Entry(price_frame, textvariable=self.price_var, width=10)
        self.price_entry.pack(side=tk.LEFT)
        self.price_entry.bind('<Return>', self._apply_filters)

        # Filtro de plataforma
        platform_frame = tk.Frame(filter_frame, bg=Theme.BG_SECONDARY)
        platform_frame.pack(side=tk.LEFT)

        tk.Label(platform_frame, text="Plataforma:",
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY,
                 font=Theme.NORMAL_FONT).pack(side=tk.LEFT, padx=5)

        self.platform_var = tk.StringVar()
        self.platform_cb = ttk.Combobox(platform_frame, textvariable=self.platform_var, width=20)
        self.platform_cb.pack(side=tk.LEFT)
        self.platform_cb.bind('<<ComboboxSelected>>', self._apply_filters)

    def _setup_game_list(self):
        games_frame = tk.Frame(self, bg=Theme.BG_DARK)
        games_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configurar estilo
        style = ttk.Style()
        style.configure("Treeview",
                        background="#1a1a1a",
                        foreground="white",
                        fieldbackground="#1a1a1a",
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background="#2d2d2d",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3d3d3d')])

        # Configurar columnas
        columns = ('Nombre', 'Precio', 'Marca', 'Clasificación', 'Stock', 'Plataforma')
        self.game_tree = ttk.Treeview(games_frame, columns=columns, show='headings', height=20)

        # Configurar ancho de columnas
        column_widths = {
            'Nombre': 300,
            'Precio': 100,
            'Marca': 150,
            'Clasificación': 100,
            'Stock': 100,
            'Plataforma': 200
        }

        for col in columns:
            self.game_tree.heading(col, text=col)
            self.game_tree.column(col, width=column_widths.get(col, 150))

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(games_frame, orient=tk.VERTICAL, command=self.game_tree.yview)
        x_scrollbar = ttk.Scrollbar(games_frame, orient=tk.HORIZONTAL, command=self.game_tree.xview)
        self.game_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Empaquetar elementos
        self.game_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        sell_btn = tk.Button(games_frame,
                             text="Vender Juego Seleccionado",
                             command=self._sell_game,
                             bg=Theme.ACCENT,
                             fg=Theme.BG_DARK,
                             font=Theme.SUBTITLE_FONT)
        sell_btn.pack(pady=10)

    def _sell_game(self):
        selected = self.game_tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un juego para vender")
            return

        item = self.game_tree.item(selected[0])
        game_name = item['values'][0]

        # Obtener datos completos del juego
        game_data = self.df[self.df['Nombre'] == game_name].iloc[0]

        sell_window = SellGameWindow(self, game_data)
        sell_window.grab_set()



    def _load_games(self):
        if self.df is not None:
            # Actualizar comboboxes con valores únicos
            marcas = sorted(self.df['Marca'].unique().tolist())
            platforms = sorted(self.df['Plataformas Disponibles'].unique().tolist())

            self.marca_cb['values'] = ['Todas'] + marcas
            self.marca_cb.set('Todas')

            self.platform_cb['values'] = ['Todas'] + platforms
            self.platform_cb.set('Todas')

            # Mostrar todos los juegos inicialmente
            self._update_tree(self.df)

    def _apply_filters(self, event=None):
        if self.df is None:
            return

        filtered_df = self.df.copy()

        # Aplicar filtro de marca/desarrolladora
        if self.marca_var.get() and self.marca_var.get() != 'Todas':
            filtered_df = filtered_df[filtered_df['Marca'] == self.marca_var.get()]

        # Aplicar filtro de precio
        if self.price_var.get():
            try:
                max_price = float(self.price_var.get())
                filtered_df = filtered_df[filtered_df['Precio Base'] <= max_price]
            except ValueError:
                pass

        # Aplicar filtro de plataforma
        if self.platform_var.get() and self.platform_var.get() != 'Todas':
            filtered_df = filtered_df[filtered_df['Plataformas Disponibles'] == self.platform_var.get()]

        # Actualizar la vista
        self._update_tree(filtered_df)

    def _update_tree(self, df):
        # Limpiar árbol actual
        for item in self.game_tree.get_children():
            self.game_tree.delete(item)

        # Insertar datos
        for _, row in df.iterrows():
            values = [
                row['Nombre'],
                f"${row['Precio Base']:.2f}",
                row['Marca'],
                row['Clasificación'],
                row['Stock'],
                row['Plataformas Disponibles']
            ]
            self.game_tree.insert('', tk.END, values=values)


class SellGameWindow(tk.Toplevel):
    def __init__(self, parent, game_data):
        super().__init__(parent)
        self.title("Vender Juego")
        self.geometry("400x300")
        self.configure(bg=Theme.BG_DARK)

        self.game_data = game_data
        self.df = pd.read_excel('data/games.xlsx')

        self._setup_ui()

    def _setup_ui(self):
        main_frame = tk.Frame(self, bg=Theme.BG_DARK, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Información del juego
        tk.Label(main_frame,
                 text=f"Juego: {self.game_data['Nombre']}",
                 font=Theme.SUBTITLE_FONT,
                 bg=Theme.BG_DARK,
                 fg=Theme.TEXT_PRIMARY).pack(pady=5)

        tk.Label(main_frame,
                 text=f"Precio: ${self.game_data['Precio Base']:.2f}",
                 font=Theme.NORMAL_FONT,
                 bg=Theme.BG_DARK,
                 fg=Theme.TEXT_PRIMARY).pack(pady=5)

        tk.Label(main_frame,
                 text=f"Stock disponible: {self.game_data['Stock']}",
                 font=Theme.NORMAL_FONT,
                 bg=Theme.BG_DARK,
                 fg=Theme.TEXT_PRIMARY).pack(pady=5)

        # Entrada para cantidad
        quantity_frame = tk.Frame(main_frame, bg=Theme.BG_DARK)
        quantity_frame.pack(pady=20)

        tk.Label(quantity_frame,
                 text="Cantidad:",
                 font=Theme.NORMAL_FONT,
                 bg=Theme.BG_DARK,
                 fg=Theme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=5)

        self.quantity_var = tk.StringVar()
        self.quantity_entry = tk.Entry(quantity_frame,
                                       textvariable=self.quantity_var,
                                       width=10)
        self.quantity_entry.pack(side=tk.LEFT, padx=5)

        # Botones
        button_frame = tk.Frame(main_frame, bg=Theme.BG_DARK)
        button_frame.pack(pady=20)

        tk.Button(button_frame,
                  text="Vender",
                  command=self._process_sale,
                  bg=Theme.ACCENT,
                  fg=Theme.BG_DARK,
                  font=Theme.SUBTITLE_FONT).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame,
                  text="Cancelar",
                  command=self.destroy,
                  bg=Theme.BG_SECONDARY,
                  fg=Theme.TEXT_PRIMARY,
                  font=Theme.SUBTITLE_FONT).pack(side=tk.LEFT, padx=5)

    def _process_sale(self):
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return

            current_stock = self.game_data['Stock']

            if current_stock == 0:
                messagebox.showerror("Error", "No disponible en stock")
                return

            if quantity > current_stock:
                messagebox.showerror("Error", "No hay suficiente stock para vender")
                return

            # Actualizar stock
            game_id = self.game_data['ID del Juego']
            idx = self.df[self.df['ID del Juego'] == game_id].index[0]
            new_stock = current_stock - quantity
            self.df.at[idx, 'Stock'] = new_stock

            # Guardar cambios
            self.df.to_excel('data/games.xlsx', index=False)

            total = quantity * self.game_data['Precio Base']

            # Registrar la venta
            register_sale(self.game_data['Nombre'], quantity, total)

            messagebox.showinfo("Éxito",
                                f"Venta realizada con éxito\n\n"
                                f"Total: ${total:.2f}\n"
                                f"Nuevo stock: {new_stock}")

            self.destroy()

        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa una cantidad válida")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la venta: {str(e)}")