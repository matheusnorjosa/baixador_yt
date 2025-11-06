# YouTube MP3 Downloader PRO (v2.0)

# --------------------------------------------------------------------------------------------------
# 1. Importações de Módulos
# --------------------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import re
import yt_dlp
import json
import sys

# --------------------------------------------------------------------------------------------------
# 2. Configurações Globais e Carregamento Inicial
# --------------------------------------------------------------------------------------------------
CONFIG_PATH = 'config.json'
DEFAULT_FOLDER = 'downloads_mp3' # Pasta padrão para downloads
ICONS_SUBFOLDER_NAME = 'icons'

# Determina o caminho base da aplicação para encontrar recursos (ícones, config.json)
# Funciona tanto em modo de desenvolvimento quanto em executável PyInstaller
if getattr(sys, 'frozen', False):
    # Se estiver rodando como executável PyInstaller
    APPLICATION_BASE_PATH = sys._MEIPASS
else:
    # Se estiver rodando como script Python
    APPLICATION_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

ICONS_FULL_PATH = os.path.join(APPLICATION_BASE_PATH, ICONS_SUBFOLDER_NAME)
CONFIG_FULL_PATH = os.path.join(APPLICATION_BASE_PATH, CONFIG_PATH)
FFMPEG_PATH = os.path.join(APPLICATION_BASE_PATH, 'bin', 'ffmpeg.exe')
FFPROBE_PATH = os.path.join(APPLICATION_BASE_PATH, 'bin', 'ffprobe.exe')

# Carrega configurações ou define valores padrão
initial_download_folder = os.path.join(APPLICATION_BASE_PATH, DEFAULT_FOLDER)
initial_quality = "192kbps"
initial_format_type = "MP3"

try:
    if os.path.exists(CONFIG_FULL_PATH):
        with open(CONFIG_FULL_PATH, 'r') as f:
            config = json.load(f)
            initial_download_folder = config.get('pasta', initial_download_folder)
            initial_quality = config.get('qualidade', initial_quality)
            initial_format_type = config.get('formato_tipo', initial_format_type)
except (json.JSONDecodeError, FileNotFoundError):
    # Se o arquivo de configuração estiver corrompido ou não for encontrado, usa os valores padrão
    pass

# --------------------------------------------------------------------------------------------------
# 3. Classe Principal da Aplicação
# --------------------------------------------------------------------------------------------------
class YouTubeMP3Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3/MP4 Downloader PRO")
        self.root.geometry("800x650") # Tamanho inicial da janela
        self.root.resizable(False, False) # Impede redimensionamento
        self.root.configure(bg='#ECEFF1') # Cor de fundo leve

        self.fila = [] # Fila de URLs para download
        self.em_processamento = False # Flag para indicar se há um download ativo
        self.pausado = False # Flag para pausar/retomar a fila
        self.download_folder = initial_download_folder
        os.makedirs(self.download_folder, exist_ok=True) # Garante que a pasta exista

        # Variáveis de controle para a GUI
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto")
        self.progress_var = tk.DoubleVar(value=0)
        self.quality_var = tk.StringVar(value=initial_quality)
        self.format_type_var = tk.StringVar(value=initial_format_type)

        # Referência ao widget OptionMenu de qualidade para atualização dinâmica
        self.quality_option_menu = None # Será inicializado em setup_ui

        self._load_icons()
        self.setup_ui() # setup_ui cria o self.quality_option_menu primeiro
        self._configure_ydl_opts() # Configura yt-dlp com base nas opções iniciais
        self._center_window() # Centraliza a janela após a criação da UI

        # Garante que a qualidade inicial seja válida e atualiza as opções do menu
        # Chamado APÓS self.setup_ui() para garantir que self.quality_option_menu existe
        self._update_quality_options(self.format_type_var.get())


    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _load_icons(self):
        self.icons = {}
        icon_names = {
            "download": "download.png",
            "playlist": "playlist.png",
            "folder": "folder.png",
            "pause": "pause.png",
            "play": "play.png",
            "clear": "clear.png",
            "open_folder": "open_folder.png"
        }
        try:
            for name, filename in icon_names.items():
                path = os.path.join(ICONS_FULL_PATH, filename)
                self.icons[name] = tk.PhotoImage(file=path)
        except Exception as e:
            messagebox.showerror("Erro de Ícone",
                                 f"Não foi possível carregar um ou mais ícones. "
                                 f"Certifique-se de que a pasta '{ICONS_SUBFOLDER_NAME}' e os arquivos .png estão corretos. "
                                 f"Erro: {e}")
            # Se os ícones essenciais não puderem ser carregados, a aplicação não pode iniciar corretamente.
            # Em um ambiente de produção, você pode querer fechar o app aqui.
            # self.root.destroy() 

    def _configure_ydl_opts(self):
        selected_format_type = self.format_type_var.get()
        selected_quality = self.quality_var.get()

        self.ydl_opts = {
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'no_color': True,
            'ignoreerrors': True,
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self.progresso],
            'extract_flat': True, # Para playlists, para extrair URLs sem baixar imediatamente
        }

        # Configura o caminho do FFmpeg se existir na pasta bin/
        if os.path.exists(FFMPEG_PATH):
            self.ydl_opts['ffmpeg_location'] = os.path.dirname(FFMPEG_PATH)

        if selected_format_type == "MP3":
            preferred_quality_audio = selected_quality.replace("kbps", "")
            self.ydl_opts['format'] = 'bestaudio/best'
            self.ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': preferred_quality_audio
            }]
        elif selected_format_type == "MP4":
            resolution_map = {
                "360p": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "480p": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            }
            self.ydl_opts['format'] = resolution_map.get(selected_quality, "best[ext=mp4]/best") # Padrão para melhor MP4 se não mapeado
            self.ydl_opts['postprocessors'] = [
                {'key': 'FFmpegVideoRemuxer', 'preferedformat': 'mp4'},
                {'key': 'FFmpegMetadata'}
            ]

    def setup_ui(self):
        # Estilos
        style = ttk.Style()
        style.theme_use('clam') # Tema mais moderno
        style.configure('TFrame', background='#ECEFF1')
        style.configure('TButton',
                        font=('Helvetica', 10, 'bold'),
                        background='#CFD8DC',
                        foreground='#333333',
                        padding=6)
        style.map('TButton',
                  background=[('active', '#B0BEC5')],
                  foreground=[('active', '#000000')])
        style.configure('TEntry',
                        font=('Helvetica', 10),
                        padding=5,
                        fieldbackground='white',
                        foreground='#333333')
        style.configure('TProgressbar',
                        background='#4CAF50', # Cor da barra de progresso
                        troughcolor='#CFD8DC', # Cor de fundo da barra
                        thickness=15)
        style.configure('TLabel', background='#ECEFF1', foreground='#333333')
        style.configure('Placeholder.TEntry', foreground='grey') # Estilo para placeholder

        # Frame Principal
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Título da Aplicação
        tk.Label(main_frame, text="YouTube MP3/MP4 Downloader PRO",
                 font=('Helvetica', 16, 'bold'), bg='#ECEFF1', fg='#263238').pack(pady=10)

        # Campo de URL
        url_frame = ttk.Frame(main_frame, style='TFrame')
        url_frame.pack(pady=10, fill=tk.X)

        tk.Label(url_frame, text="🔗 URL do vídeo/playlist:", bg='#ECEFF1', fg='#333333').pack(side=tk.LEFT, padx=(0, 5))
        self.url_entry_widget = ttk.Entry(url_frame, textvariable=self.url_var, width=60, style='TEntry')
        self.url_entry_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.url_entry_widget.bind("<FocusIn>", self._on_entry_focus_in)
        self.url_entry_widget.bind("<FocusOut>", self._on_entry_focus_out)
        self.url_entry_widget.bind("<Return>", lambda event: self.baixar_imediato_threaded())
        self._set_placeholder() # Define o placeholder inicial

        # Botões de Ação
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text=" Baixar Agora", command=self.baixar_imediato_threaded,
                   image=self.icons["download"], compound=tk.LEFT,
                   style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Adicionar Playlist", command=self.adicionar_playlist_threaded,
                   image=self.icons["playlist"], compound=tk.LEFT,
                   style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Escolher Pasta", command=self.escolher_pasta,
                   image=self.icons["folder"], compound=tk.LEFT,
                   style='TButton').pack(side=tk.LEFT, padx=5)

        # Frame para controle de qualidade e formato
        control_frame = ttk.Frame(main_frame, style='TFrame')
        control_frame.pack(pady=10)

        # Seleção de Formato (MP3/MP4)
        tk.Label(control_frame, text="🎥 Formato:", bg='#ECEFF1', fg='#333333').pack(side=tk.LEFT, padx=(0, 5))
        ttk.OptionMenu(
            control_frame,
            self.format_type_var,
            self.format_type_var.get(),
            "MP3", "MP4", # Opções de formato
            command=self._update_quality_options # Chama este método ao mudar o formato
        ).pack(side=tk.LEFT, padx=15) # Aumenta o padx para separar

        # Seleção de Qualidade (dinâmica)
        tk.Label(control_frame, text="🔊 Qualidade:", bg='#ECEFF1', fg='#333333').pack(side=tk.LEFT, padx=(15, 5))
        # self.quality_option_menu é uma referência ao widget OptionMenu de qualidade
        self.quality_option_menu = ttk.OptionMenu( # <--- Inicializa aqui
            control_frame,
            self.quality_var,
            self.quality_var.get(),
            *self._get_quality_options_for_format(self.format_type_var.get()), # Opções iniciais
            command=lambda x: self._update_ydl_options_and_save() # Salva e reconfigura ao mudar qualidade
        )
        self.quality_option_menu.pack(side=tk.LEFT, padx=5)

        # Status e Progresso
        tk.Label(main_frame, textvariable=self.status_var,
                 font=('Helvetica', 10, 'italic'), bg='#ECEFF1', fg='#546E7A').pack(pady=5)
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100, style='TProgressbar')
        self.progress_bar.pack(pady=10, fill=tk.X)

        # Fila de Downloads
        tk.Label(main_frame, text="📥 Fila de Downloads:",
                 font=('Helvetica', 12, 'bold'), bg='#ECEFF1', fg='#263238').pack(pady=(10, 5))
        list_frame = ttk.Frame(main_frame, style='TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.listbox = tk.Listbox(list_frame, height=10, font=('Consolas', 9),
                                  bg='white', fg='#333333', selectbackground='#B0BEC5', selectforeground='black')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Botões de Controle da Fila
        queue_control_frame = ttk.Frame(main_frame, style='TFrame')
        queue_control_frame.pack(pady=10)

        ttk.Button(queue_control_frame, text=" Pausar", command=self.pausar_download,
                   image=self.icons["pause"], compound=tk.LEFT,
                   style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(queue_control_frame, text=" Retomar", command=self.retomar_download,
                   image=self.icons["play"], compound=tk.LEFT,
                   style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(queue_control_frame, text=" Limpar Fila", command=self.limpar_fila,
                   image=self.icons["clear"], compound=tk.LEFT,
                   style='TButton').pack(side=tk.LEFT, padx=5)

        # Botão "Abrir Pasta" (inicialmente oculto)
        self.open_folder_button = ttk.Button(main_frame, text=" Abrir Pasta", command=self.open_download_folder,
                                             image=self.icons["open_folder"], compound=tk.LEFT,
                                             style='TButton')
        self.open_folder_button.pack(side=tk.LEFT, pady=10, padx=10)
        self.open_folder_button.pack_forget() # Oculta inicialmente

    def _set_placeholder(self):
        if not self.url_var.get():
            self.url_entry_widget.insert(0, "Cole a URL do vídeo ou playlist aqui...")
            self.url_entry_widget.config(style='Placeholder.TEntry')

    def _on_entry_focus_in(self, event):
        if self.url_entry_widget.get() == "Cole a URL do vídeo ou playlist aqui...":
            self.url_entry_widget.delete(0, tk.END)
            self.url_entry_widget.config(style='TEntry')

    def _on_entry_focus_out(self, event):
        self._set_placeholder()

    def _get_quality_options_for_format(self, format_type):
        """Retorna a lista de opções de qualidade com base no tipo de formato."""
        if format_type == "MP3":
            return ["128kbps", "192kbps", "256kbps", "320kbps"]
        elif format_type == "MP4":
            return ["360p", "480p", "720p", "1080p"]
        return []

    def _update_quality_options(self, selected_format_type):
        """Atualiza as opções do menu de qualidade e o valor padrão."""
        new_options = self._get_quality_options_for_format(selected_format_type)

        # Limpa o menu existente
        menu = self.quality_option_menu["menu"]
        menu.delete(0, "end")

        # Adiciona as novas opções
        for option in new_options:
            # CORREÇÃO: Usando lambda para definir a command corretamente
            menu.add_command(label=option, command=lambda opt=option: self._set_quality_and_update(opt))

        # Define um valor padrão razoável para o novo formato, se o valor atual não for mais válido
        if selected_format_type == "MP3":
            if self.quality_var.get() not in new_options:
                self.quality_var.set("192kbps") # Padrão para MP3
        elif selected_format_type == "MP4":
            if self.quality_var.get() not in new_options:
                self.quality_var.set("720p") # Padrão para MP4

        # Reconfigura yt-dlp e salva as configurações após a atualização do menu.
        self._update_ydl_options_and_save()

    def _set_quality_and_update(self, quality_value):
        """Define a quality_var e chama o método de atualização de ydl_opts e salvamento."""
        self.quality_var.set(quality_value)
        self._update_ydl_options_and_save()


    def _update_ydl_options_and_save(self):
        """Atualiza as opções do yt-dlp e salva as configurações."""
        self._configure_ydl_opts()
        self.salvar_config()

    def salvar_config(self):
        """Salva as configurações atuais em um arquivo JSON."""
        config = {
            'pasta': self.download_folder,
            'qualidade': self.quality_var.get(),
            'formato_tipo': self.format_type_var.get()
        }
        try:
            with open(CONFIG_FULL_PATH, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Erro ao Salvar Configurações", f"Não foi possível salvar as configurações: {e}")

    def sanitize_filename(self, filename):
        """Remove caracteres inválidos de um nome de arquivo."""
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
        filename = re.sub(r'\s+', '_', filename).strip()
        filename = re.sub(r'_+', '_', filename)
        return filename

    def progresso(self, d):
        """Callback de progresso para yt-dlp, atualiza a GUI."""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                percent = (downloaded_bytes / total_bytes) * 100
                self.root.after(0, self.progress_var.set, percent)
                speed = d.get('speed')
                eta = d.get('eta')
                status_text = f"⬇️ Baixando: {percent:.1f}%"
                if speed:
                    status_text += f" | Velocidade: {self._format_bytes(speed)}/s"
                if eta is not None:
                    status_text += f" | ETA: {self._format_eta(eta)}"
                self.root.after(0, self.status_var.set, status_text)
            else:
                self.root.after(0, self.status_var.set, "⬇️ Baixando...")
        elif d['status'] == 'finished':
            self.root.after(0, self.progress_var.set, 100)
            self.root.after(0, self.status_var.set, "🟢 Download concluído!")
            self.root.after(0, self.open_folder_button.pack) # Mostra o botão Abrir Pasta
            self.root.after(0, self.url_var.set, "") # Limpa o campo de URL
            self.root.after(0, self._set_placeholder) # Restaura o placeholder
        elif d['status'] == 'error':
            self.root.after(0, self.status_var.set, "🔴 Erro no download!")
            self.root.after(0, self.progress_var.set, 0)

    def _format_bytes(self, bytes_val):
        """Formata bytes para KB/MB/GB."""
        if bytes_val is None:
            return "N/A"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f}{unit}"
            bytes_val /= 1024.0

    def _format_eta(self, seconds):
        """Formata segundos para HH:MM:SS."""
        if seconds is None:
            return "N/A"
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def baixar_imediato_threaded(self):
        """Inicia o download de um único vídeo em uma nova thread."""
        url = self.url_var.get()
        if not url or url == "Cole a URL do vídeo ou playlist aqui...":
            messagebox.showwarning("URL Vazia", "Por favor, insira uma URL de vídeo ou playlist.")
            return

        self.open_folder_button.pack_forget() # Oculta o botão Abrir Pasta
        self.status_var.set("🔍 Buscando informações...")
        self.progress_var.set(0)
        threading.Thread(target=self._executar_download_unico, args=(url,)).start()

    def _executar_download_unico(self, url):
        """Executa o download de um único vídeo/áudio."""
        try:
            self._configure_ydl_opts() # Garante que as opções estão atualizadas antes do download
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
        except yt_dlp.DownloadError as e:
            self.root.after(0, self.status_var.set, f"🔴 Erro no download: {e}")
            self.root.after(0, self.progress_var.set, 0)
        except Exception as e:
            self.root.after(0, self.status_var.set, f"🔴 Erro inesperado: {e}")
            self.root.after(0, self.progress_var.set, 0)

    def adicionar_playlist_threaded(self):
        """Adiciona uma playlist à fila em uma nova thread."""
        url = self.url_var.get()
        if not url or url == "Cole a URL do vídeo ou playlist aqui...":
            messagebox.showwarning("URL Vazia", "Por favor, insira uma URL de vídeo ou playlist.")
            return

        self.open_folder_button.pack_forget() # Oculta o botão Abrir Pasta
        self.status_var.set("🔍 Analisando playlist...")
        self.progress_var.set(0)
        threading.Thread(target=self._processar_playlist, args=(url,)).start()

    def _processar_playlist(self, url):
        """Processa a URL da playlist para adicionar vídeos à fila."""
        try:
            # Usar uma configuração mínima de ydl_opts para a análise da playlist
            # para não incluir post-processadores que podem falhar ou atrasar a análise.
            playlist_analysis_opts = {
                'extract_flat': True,
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True # Ignorar erros de vídeos indisponíveis na playlist
            }
            with yt_dlp.YoutubeDL(playlist_analysis_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            if 'entries' in info:
                added_count = 0
                for entry in info['entries']:
                    if entry and 'url' in entry: # Garante que a entrada é válida
                        title = self.sanitize_filename(entry.get('title', 'Vídeo sem título'))
                        self.root.after(0, lambda t=title, u=entry['url']: self.fila.append({"title": t, "url": u, "status": "Pendente"}))
                        added_count += 1
                self.root.after(0, self.atualizar_fila)
                self.root.after(0, self.status_var.set, f"Playlist adicionada! {added_count} vídeos na fila.")
                if added_count > 0: # Só inicia se houver vídeos adicionados
                    self.root.after(0, self.processar_fila)
                self.root.after(0, self.url_var.set, "") # Limpa o campo de URL
                self.root.after(0, self._set_placeholder) # Restaura o placeholder
            else:
                self.root.after(0, self.status_var.set, "🔴 URL não é uma playlist válida ou não contém vídeos.")
        except yt_dlp.DownloadError as e:
            self.root.after(0, self.status_var.set, f"🔴 Erro ao analisar playlist: {e}")
        except Exception as e:
            self.root.after(0, self.status_var.set, f"🔴 Erro inesperado ao analisar playlist: {e}")

    def atualizar_fila(self):
        """Atualiza a exibição da fila na Listbox."""
        self.listbox.delete(0, tk.END)
        for i, item in enumerate(self.fila):
            display_text = f"{i+1}. {item['title']} - {item['status']}"
            self.listbox.insert(tk.END, display_text)
            # Adicionando cores para status
            if item['status'] == "Baixando...":
                self.listbox.itemconfig(i, {'fg': '#1E88E5'}) # Azul
            elif item['status'] == "Concluído":
                self.listbox.itemconfig(i, {'fg': '#4CAF50'}) # Verde
            elif item['status'] == "Erro":
                self.listbox.itemconfig(i, {'fg': '#E53935'}) # Vermelho
            else: # "Pendente"
                self.listbox.itemconfig(i, {'fg': '#333333'})

    def limpar_fila(self):
        """Limpa todos os itens da fila."""
        if messagebox.askyesno("Limpar Fila", "Tem certeza que deseja limpar a fila de downloads?"):
            self.fila.clear()
            self.atualizar_fila()
            self.status_var.set("Fila limpa. Pronto.")
            self.pausado = False
            self.em_processamento = False
            self.progress_var.set(0)
            self.open_folder_button.pack_forget()

    def pausar_download(self):
        """Pausa o processamento da fila."""
        if self.em_processamento and not self.pausado:
            self.pausado = True
            self.status_var.set("⏸ Fila pausada. Concluindo download atual...")
        elif not self.em_processamento:
            self.status_var.set("Fila não está ativa para pausar.")

    def retomar_download(self):
        """Retoma o processamento da fila."""
        if self.pausado:
            self.pausado = False
            self.status_var.set("▶ Retomando fila...")
            self.processar_fila()
        elif not self.em_processamento and self.fila:
            self.status_var.set("Iniciando processamento da fila...")
            self.processar_fila()
        else:
            self.status_var.set("Fila já está ativa ou vazia.")

    def processar_fila(self):
        """Inicia o processamento da fila em uma nova thread se não estiver ativo."""
        if not self.em_processamento and self.fila:
            self.em_processamento = True
            self.pausado = False
            self.open_folder_button.pack_forget()
            threading.Thread(target=self.executar_fila).start()

    def executar_fila(self):
        """Loop principal que processa os downloads da fila."""
        while self.fila and not self.pausado:
            current_item_dict = self.fila[0] # Pega o primeiro item como dicionário
            
            # Atualiza status visualmente na Listbox
            self.root.after(0, lambda: self.listbox.itemconfig(0, {'fg': '#1E88E5'})) # Azul para "baixando"
            self.root.after(0, self.progress_var.set, 0) # Zera barra para novo item

            current_item_dict['status'] = "Baixando..."
            self.root.after(0, self.atualizar_fila) # Atualiza a Listbox com o novo status

            self.root.after(0, lambda: self.status_var.set(f"Baixando: {current_item_dict['title']}"))
            
            try:
                self._configure_ydl_opts() # Garante que as opções (formato, qualidade) estão atualizadas
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([current_item_dict['url']])
                
                current_item_dict['status'] = "Concluído"
            except yt_dlp.DownloadError as e:
                current_item_dict['status'] = "Erro"
                self.root.after(0, self.status_var.set, f"🔴 Erro no download de {current_item_dict['title']}: {e}")
            except Exception as e:
                current_item_dict['status'] = "Erro"
                self.root.after(0, self.status_var.set, f"🔴 Erro inesperado em {current_item_dict['title']}: {e}")
            finally:
                self.root.after(0, self.atualizar_fila) # Atualiza Listbox com status final (Concluído/Erro)
                # Remove o item da fila após tentar o download (sucesso ou erro)
                self.root.after(0, lambda: self.fila.pop(0))
                self.root.after(0, self.atualizar_fila) # Atualiza a Listbox para remover o item concluído/com erro

        self.em_processamento = False
        if not self.fila and not self.pausado:
            self.root.after(0, self.status_var.set, "Todos os downloads concluídos! Pronto.")
            self.root.after(0, self.progress_var.set, 0)
            self.root.after(0, self.open_folder_button.pack) # Mostra o botão Abrir Pasta
        elif self.pausado:
            self.root.after(0, self.status_var.set, "Fila pausada.")

    def escolher_pasta(self):
        """Abre uma caixa de diálogo para o usuário escolher a pasta de download."""
        new_folder = filedialog.askdirectory(initialdir=self.download_folder)
        if new_folder:
            self.download_folder = new_folder
            self._update_ydl_options_and_save() # Salva a nova pasta e reconfigura yt-dlp
            messagebox.showinfo("Pasta Selecionada", f"A pasta de downloads foi definida para:\n{self.download_folder}")

    def open_download_folder(self):
        """Abre a pasta de downloads no explorador de arquivos do sistema."""
        try:
            if sys.platform == "win32":
                os.startfile(self.download_folder)
            elif sys.platform == "darwin": # macOS
                os.system(f"open \"{self.download_folder}\"")
            else: # Linux
                os.system(f"xdg-open \"{self.download_folder}\"")
        except Exception as e:
            messagebox.showerror("Erro ao Abrir Pasta", f"Não foi possível abrir a pasta:\n{e}")

# --------------------------------------------------------------------------------------------------
# 4. Ponto de Entrada da Aplicação
# --------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeMP3Downloader(root)
    root.mainloop()