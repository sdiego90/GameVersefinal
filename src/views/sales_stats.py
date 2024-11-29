import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import io
from PIL import Image, ImageTk
from src.utils.theme import Theme


class SalesStatsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Estadísticas de Ventas")
        self.geometry("800x600")
        self.configure(bg=Theme.BG_DARK)

        self.sales_data = self._load_sales_data()
        self._setup_ui()

    def _load_sales_data(self):
        try:
            return pd.read_excel('data/ventas_temp.xlsx')
        except:
            return pd.DataFrame(columns=['Fecha', 'Juego', 'Cantidad', 'Total'])

    def _setup_ui(self):
        main_frame = tk.Frame(self, bg=Theme.BG_DARK, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Filtro Frame
        filter_frame = tk.Frame(main_frame, bg=Theme.BG_SECONDARY, padx=10, pady=5)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(filter_frame, text="Desarrolladora:",
                 bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=5)

        # Lista de desarrolladoras únicas
        desarrolladoras = ['Todas'] + sorted(pd.read_excel('data/games.xlsx')['Marca'].unique().tolist())

        self.dev_var = tk.StringVar(value='Todas')
        dev_cb = ttk.Combobox(filter_frame,
                              textvariable=self.dev_var,
                              values=desarrolladoras,
                              width=30)
        dev_cb.pack(side=tk.LEFT, padx=5)
        dev_cb.bind('<<ComboboxSelected>>', self._update_stats)

        # Resto del código existente...

    def _update_stats(self, event=None):
        # Filtrar datos según desarrolladora seleccionada
        if self.dev_var.get() != 'Todas':
            games_by_dev = pd.read_excel('data/games.xlsx')
            games_list = games_by_dev[games_by_dev['Marca'] == self.dev_var.get()]['Nombre'].tolist()
            filtered_data = self.sales_data[self.sales_data['Juego'].isin(games_list)]
        else:
            filtered_data = self.sales_data

        # Actualizar estadísticas y gráfico
        self._show_stats(filtered_data)
        self._refresh_graph(filtered_data)

    def _show_stats(self, data):
        # Actualizar estadísticas con datos filtrados
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        if not data.empty:
            total_ingresos = data['Total'].sum()
            ventas_por_juego = data.groupby('Juego')['Cantidad'].sum()
            juego_mas_vendido = ventas_por_juego.idxmax()
            cantidad_mas_vendida = ventas_por_juego.max()

            tk.Label(self.stats_frame,
                     text=f"Ingresos Totales: ${total_ingresos:,.2f}",
                     font=Theme.SUBTITLE_FONT,
                     bg=Theme.BG_SECONDARY,
                     fg=Theme.ACCENT).pack(pady=5)

            tk.Label(self.stats_frame,
                     text=f"Juego Más Vendido: {juego_mas_vendido} ({cantidad_mas_vendida} unidades)",
                     font=Theme.SUBTITLE_FONT,
                     bg=Theme.BG_SECONDARY,
                     fg=Theme.ACCENT).pack(pady=5)

    def _refresh_graph(self, data):
        # Actualizar gráfico con datos filtrados
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        if not data.empty:
            self._create_sales_graph(self.graph_frame, data)
        else:
            tk.Label(self.graph_frame,
                     text="No hay datos de ventas disponibles",
                     font=Theme.SUBTITLE_FONT,
                     bg=Theme.BG_DARK,
                     fg=Theme.TEXT_PRIMARY).pack(expand=True)

    def _create_sales_graph(self, frame):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.barplot(data=self.sales_data,
                    x='Fecha',
                    y='Total',
                    ax=ax,
                    color='#00ff9d')

        ax.set_title('Ventas por Fecha', fontsize=14, pad=20)
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Total Ventas ($)', fontsize=12)

        plt.xticks(rotation=45, ha='right')

        # Guardar y mostrar
        buffer = io.BytesIO()
        plt.savefig(buffer,
                    format='png',
                    transparent=False,
                    bbox_inches='tight',
                    dpi=100)
        buffer.seek(0)

        image = Image.open(buffer)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(frame, image=photo, bg=Theme.BG_DARK)
        label.image = photo
        label.pack(expand=True)

        plt.close()


def register_sale(game_name, quantity, total):
    try:
        try:
            df = pd.read_excel('data/ventas_temp.xlsx')
        except:
            df = pd.DataFrame(columns=['Fecha', 'Juego', 'Cantidad', 'Total'])

        new_sale = {
            'Fecha': datetime.now().strftime('%Y-%m-%d'),
            'Juego': game_name,
            'Cantidad': quantity,
            'Total': total
        }

        df = pd.concat([df, pd.DataFrame([new_sale])], ignore_index=True)
        df.to_excel('data/ventas_temp.xlsx', index=False)

    except Exception as e:
        print(f"Error al registrar venta: {e}")