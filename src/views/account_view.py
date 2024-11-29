# views/account_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from src.utils.theme import Theme
from src.utils.config import ADMIN_CREDENTIALS
from .sales_stats import SalesStatsWindow


class StockManagerWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Administrar Stock")
        self.geometry("800x600")
        self.configure(bg=Theme.BG_DARK)

        # Cargar datos
        self.df = pd.read_excel('data/games.xlsx')

        self._setup_ui()

    def _setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=Theme.BG_DARK, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Lista de juegos
        game_frame = tk.Frame(main_frame, bg=Theme.BG_DARK)
        game_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Crear Treeview
        columns = ('ID', 'Nombre', 'Stock Actual')
        self.tree = ttk.Treeview(game_frame, columns=columns, show='headings')

        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre del Juego')
        self.tree.heading('Stock Actual', text='Stock Actual')

        self.tree.column('ID', width=100)
        self.tree.column('Nombre', width=400)
        self.tree.column('Stock Actual', width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(game_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar Treeview y scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para modificar stock
        modify_frame = tk.Frame(main_frame, bg=Theme.BG_SECONDARY, pady=10, padx=10)
        modify_frame.pack(fill=tk.X)

        # Entrada para nuevo stock
        tk.Label(modify_frame, text="Nuevo Stock:",
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=5)

        self.stock_var = tk.StringVar()
        stock_entry = tk.Entry(modify_frame, textvariable=self.stock_var)
        stock_entry.pack(side=tk.LEFT, padx=5)

        # Botón actualizar
        update_btn = tk.Button(modify_frame,
                               text="Actualizar Stock",
                               command=self._update_stock,
                               bg=Theme.ACCENT,
                               fg=Theme.BG_DARK)
        update_btn.pack(side=tk.LEFT, padx=20)

        # Cargar datos
        self._load_games()

    def _load_games(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in self.df.iterrows():
            self.tree.insert('', tk.END, values=(row['ID del Juego'], row['Nombre'], row['Stock']))

    def _update_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un juego")
            return

        try:
            new_stock = int(self.stock_var.get())
            if new_stock < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido")
            return

        item = self.tree.item(selected[0])
        game_id = item['values'][0]

        # Actualizar DataFrame
        idx = self.df[self.df['ID del Juego'] == game_id].index[0]
        self.df.at[idx, 'Stock'] = new_stock

        # Guardar en Excel
        try:
            self.df.to_excel('data/games.xlsx', index=False)
            messagebox.showinfo("Éxito", "Stock actualizado correctamente")
            self._load_games()  # Recargar lista
            self.stock_var.set("")  # Limpiar entrada
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los cambios: {str(e)}")


class AddGameWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Agregar Nuevo Juego")
        self.geometry("600x700")
        self.configure(bg=Theme.BG_DARK)

        self._setup_ui()

    def _setup_ui(self):
        main_frame = tk.Frame(self, bg=Theme.BG_DARK, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(main_frame, text="Agregar Nuevo Juego",
                 font=Theme.TITLE_FONT,
                 bg=Theme.BG_DARK,
                 fg=Theme.TEXT_PRIMARY).pack(pady=(0, 20))

        # Formulario
        form_frame = tk.Frame(main_frame, bg=Theme.BG_SECONDARY, padx=20, pady=20)
        form_frame.pack(fill=tk.X)

        # Campos del formulario
        fields = [
            ("Nombre del Juego:", "nombre"),
            ("ID del Juego:", "id"),
            ("Desarrolladora:", "desarrolladora"),
            ("Precio Base ($):", "precio"),
            ("Stock Inicial:", "stock")
        ]

        self.entries = {}

        for label_text, field_name in fields:
            field_frame = tk.Frame(form_frame, bg=Theme.BG_SECONDARY)
            field_frame.pack(fill=tk.X, pady=5)

            tk.Label(field_frame, text=label_text,
                     bg=Theme.BG_SECONDARY,
                     fg=Theme.TEXT_PRIMARY,
                     font=Theme.NORMAL_FONT,
                     width=15,
                     anchor='w').pack(side=tk.LEFT)

            self.entries[field_name] = tk.Entry(field_frame, width=40)
            self.entries[field_name].pack(side=tk.LEFT, padx=10)

        # Clasificación ESRB (Combobox)
        field_frame = tk.Frame(form_frame, bg=Theme.BG_SECONDARY)
        field_frame.pack(fill=tk.X, pady=5)

        tk.Label(field_frame, text="Clasificación ESRB:",
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY,
                 font=Theme.NORMAL_FONT,
                 width=15,
                 anchor='w').pack(side=tk.LEFT)

        self.esrb_var = tk.StringVar()
        self.esrb_cb = ttk.Combobox(field_frame,
                                    textvariable=self.esrb_var,
                                    values=['E', 'E10+', 'T', 'M'],
                                    width=37)
        self.esrb_cb.pack(side=tk.LEFT, padx=10)

        # Plataformas
        platforms_frame = tk.Frame(form_frame, bg=Theme.BG_SECONDARY)
        platforms_frame.pack(fill=tk.X, pady=5)

        tk.Label(platforms_frame, text="Plataformas:",
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY,
                 font=Theme.NORMAL_FONT,
                 width=15,
                 anchor='w').pack(side=tk.LEFT)

        self.platform_vars = {
            'PC': tk.BooleanVar(),
            'PlayStation 5': tk.BooleanVar(),
            'PlayStation 4': tk.BooleanVar(),
            'Xbox Series X/S': tk.BooleanVar(),
            'Xbox One': tk.BooleanVar(),
            'Nintendo Switch': tk.BooleanVar()
        }

        platform_subframe = tk.Frame(platforms_frame, bg=Theme.BG_SECONDARY)
        platform_subframe.pack(side=tk.LEFT, padx=10)

        for i, (platform, var) in enumerate(self.platform_vars.items()):
            row = i // 2
            col = i % 2
            tk.Checkbutton(platform_subframe,
                           text=platform,
                           variable=var,
                           bg=Theme.BG_SECONDARY,
                           fg=Theme.TEXT_PRIMARY,
                           selectcolor=Theme.BG_DARK).grid(row=row, column=col, sticky='w', padx=5)

        # Botones
        button_frame = tk.Frame(main_frame, bg=Theme.BG_DARK)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Guardar",
                  font=Theme.SUBTITLE_FONT,
                  bg=Theme.ACCENT,
                  fg=Theme.BG_DARK,
                  command=self._save_game,
                  width=15).pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Cancelar",
                  font=Theme.SUBTITLE_FONT,
                  bg=Theme.BG_SECONDARY,
                  fg=Theme.TEXT_PRIMARY,
                  command=self.destroy,
                  width=15).pack(side=tk.LEFT, padx=10)

    def _save_game(self):
        try:
            # Validar campos requeridos
            required_fields = ['nombre', 'id', 'desarrolladora', 'precio', 'stock']
            for field in required_fields:
                if not self.entries[field].get().strip():
                    messagebox.showerror("Error", f"El campo {field} es requerido")
                    return

            # Validar ID y valores numéricos
            game_id = self.entries['id'].get().strip()
            price = float(self.entries['precio'].get().strip())
            stock = int(self.entries['stock'].get().strip())

            if price < 0 or stock < 0:
                messagebox.showerror("Error", "El precio y stock deben ser valores positivos")
                return

            # Obtener plataformas seleccionadas
            platforms = [platform for platform, var in self.platform_vars.items() if var.get()]
            if not platforms:
                messagebox.showerror("Error", "Debe seleccionar al menos una plataforma")
                return

            # Crear nuevo registro
            new_game = {
                'Nombre': self.entries['nombre'].get().strip(),
                'ID del Juego': game_id,
                'Marca': self.entries['desarrolladora'].get().strip(),
                'Clasificación': self.esrb_var.get(),
                'Plataformas Disponibles': ", ".join(platforms),
                'Precio Base': price,
                'Stock': stock
            }

            # Cargar Excel existente
            df = pd.read_excel('data/games.xlsx')

            # Verificar si el ID ya existe
            if game_id in df['ID del Juego'].values:
                messagebox.showerror("Error", "Ya existe un juego con ese ID")
                return

            # Añadir nuevo juego
            df_new = pd.concat([df, pd.DataFrame([new_game])], ignore_index=True)

            # Guardar en Excel
            df_new.to_excel('data/games.xlsx', index=False)

            messagebox.showinfo("Éxito", "Juego agregado correctamente")
            self.destroy()

        except ValueError:
            messagebox.showerror("Error", "Por favor verifica los valores numéricos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el juego: {str(e)}")


class AccountView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BG_DARK)
        self._setup_login_form()

    def _open_stats(self):
        stats_window = SalesStatsWindow(self)
        stats_window.grab_set()

    def _setup_login_form(self):
        # Frame central para el formulario
        form_frame = tk.Frame(self, bg=Theme.BG_SECONDARY,
                              padx=40, pady=40)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Título
        tk.Label(form_frame, text="Iniciar Sesión",
                 font=Theme.TITLE_FONT,
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY).pack(pady=(0, 20))

        # Email
        tk.Label(form_frame, text="Email:",
                 font=Theme.NORMAL_FONT,
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY).pack(anchor=tk.W)

        self.email_var = tk.StringVar()
        email_entry = tk.Entry(form_frame, textvariable=self.email_var,
                               font=Theme.NORMAL_FONT,
                               width=30)
        email_entry.pack(pady=(5, 15))

        # Contraseña
        tk.Label(form_frame, text="Contraseña:",
                 font=Theme.NORMAL_FONT,
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY).pack(anchor=tk.W)

        self.password_var = tk.StringVar()
        password_entry = tk.Entry(form_frame, textvariable=self.password_var,
                                  font=Theme.NORMAL_FONT,
                                  width=30,
                                  show="*")
        password_entry.pack(pady=(5, 20))

        # Botón de login
        login_btn = tk.Button(form_frame, text="Iniciar Sesión",
                              font=Theme.SUBTITLE_FONT,
                              bg=Theme.ACCENT,
                              fg=Theme.BG_DARK,
                              command=self._validate_login,
                              width=20)
        login_btn.pack(pady=(10, 0))

    def _validate_login(self):
        email = self.email_var.get()
        password = self.password_var.get()

        if email in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[email] == password:
            self._show_admin_panel()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    def _show_admin_panel(self):
        # Limpiar el frame actual
        for widget in self.winfo_children():
            widget.destroy()

        # Crear panel de administrador
        admin_frame = tk.Frame(self, bg=Theme.BG_DARK, padx=20, pady=20)
        admin_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(admin_frame, text="Panel de Administración",
                 font=Theme.TITLE_FONT,
                 bg=Theme.BG_DARK,
                 fg=Theme.TEXT_PRIMARY).pack(pady=(0, 20))

        # Botón para gestionar stock
        stock_btn = tk.Button(admin_frame, text="Gestionar Stock",
                              font=Theme.SUBTITLE_FONT,
                              bg=Theme.ACCENT,
                              fg=Theme.BG_DARK,
                              command=self._open_stock_manager,
                              width=25)
        stock_btn.pack(pady=10)

        # Botón para agregar nuevo juego
        add_game_btn = tk.Button(admin_frame, text="Agregar Nuevo Juego",
                                 font=Theme.SUBTITLE_FONT,
                                 bg=Theme.ACCENT,
                                 fg=Theme.BG_DARK,
                                 command=self._open_add_game,
                                 width=25)
        add_game_btn.pack(pady=10)

        # Botón para eliminar juego
        delete_game_btn = tk.Button(admin_frame, text="Eliminar Juego",
                                    font=Theme.SUBTITLE_FONT,
                                    bg=Theme.ACCENT,
                                    fg=Theme.BG_DARK,
                                    command=self._open_delete_game,
                                    width=25)
        delete_game_btn.pack(pady=10)

        stats_btn = tk.Button(admin_frame, text="Mostrar Estadísticas",
                              font=Theme.SUBTITLE_FONT,
                              bg=Theme.ACCENT,
                              fg=Theme.BG_DARK,
                              command=self._open_stats,
                              width=25)
        stats_btn.pack(pady=10)

        def _open_stats(self):
            stats_window = SalesStatsWindow(self)
            stats_window.grab_set()





    def _open_delete_game(self):
        delete_window = DeleteGameWindow(self)
        delete_window.grab_set()  # Hacer la ventana modal

    def _open_stock_manager(self):
        stock_window = StockManagerWindow(self)
        stock_window.grab_set()  # Hacer la ventana modal

    def _open_add_game(self):
        add_window = AddGameWindow(self)
        add_window.grab_set()  # Hacer la ventana modal


# Añadir esta nueva clase en account_view.py

class DeleteGameWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Eliminar Juego")
        self.geometry("800x600")
        self.configure(bg=Theme.BG_DARK)

        # Cargar datos
        self.df = pd.read_excel('data/games.xlsx')

        self._setup_ui()

    def _setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=Theme.BG_DARK, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(main_frame, text="Selecciona el juego a eliminar",
                 font=Theme.TITLE_FONT,
                 bg=Theme.BG_DARK,
                 fg=Theme.TEXT_PRIMARY).pack(pady=(0, 20))

        # Frame para la lista
        list_frame = tk.Frame(main_frame, bg=Theme.BG_DARK)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Crear Treeview
        columns = ('ID', 'Nombre', 'Desarrolladora', 'Plataforma')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')

        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre del Juego')
        self.tree.heading('Desarrolladora', text='Desarrolladora')
        self.tree.heading('Plataforma', text='Plataforma')

        self.tree.column('ID', width=100)
        self.tree.column('Nombre', width=300)
        self.tree.column('Desarrolladora', width=200)
        self.tree.column('Plataforma', width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar Treeview y scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones
        button_frame = tk.Frame(main_frame, bg=Theme.BG_DARK)
        button_frame.pack(fill=tk.X, pady=10)

        delete_btn = tk.Button(button_frame,
                               text="Eliminar Juego",
                               command=self._delete_game,
                               bg=Theme.ACCENT,
                               fg=Theme.BG_DARK,
                               font=Theme.SUBTITLE_FONT)
        delete_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(button_frame,
                               text="Cancelar",
                               command=self.destroy,
                               bg=Theme.BG_SECONDARY,
                               fg=Theme.TEXT_PRIMARY,
                               font=Theme.SUBTITLE_FONT)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        # Cargar datos
        self._load_games()

    def _load_games(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in self.df.iterrows():
            self.tree.insert('', tk.END, values=(
                row['ID del Juego'],
                row['Nombre'],
                row['Marca'],
                row['Plataformas Disponibles']
            ))

    def _delete_game(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un juego para eliminar")
            return

        game = self.tree.item(selected[0])
        game_id = game['values'][0]
        game_name = game['values'][1]

        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar eliminación",
                                   f"¿Estás seguro que deseas eliminar el juego?\n\n{game_name}"):
            return

        try:
            # Eliminar del DataFrame
            self.df = self.df[self.df['ID del Juego'] != game_id]

            # Guardar cambios en Excel
            self.df.to_excel('data/games.xlsx', index=False)

            messagebox.showinfo("Éxito", "Juego eliminado correctamente")
            self._load_games()  # Recargar lista

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el juego: {str(e)}")
