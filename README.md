# 🎵 YouTube MP3/MP4 Downloader PRO

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Latest-orange.svg)](https://github.com/yt-dlp/yt-dlp)

Um aplicativo desktop moderno e intuitivo para baixar vídeos e áudios do YouTube com interface gráfica elegante.

## ✨ Características

- 🎥 **Download de vídeos individuais e playlists completas**
- 🎵 **Conversão para MP3** com qualidades de 128kbps a 320kbps
- 🎬 **Download de vídeos MP4** em resoluções de 360p a 1080p
- 📋 **Sistema de fila inteligente** para múltiplos downloads
- ⏸️ **Controles de pausa/retomar** para gerenciar downloads
- 📁 **Pasta de destino personalizável** com configurações persistentes
- 🎨 **Interface moderna** com ícones intuitivos e feedback visual
- 📊 **Barra de progresso em tempo real** com velocidade e ETA
- 🔄 **Threading assíncrono** para interface responsiva

## 🖼️ Screenshots

![Interface Principal](https://via.placeholder.com/800x600/ECEFF1/263238?text=YouTube+MP3%2FMP4+Downloader+PRO)

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8 ou superior**
- **FFmpeg** (instalação necessária)

#### Instalação do FFmpeg

⚠️ **Importante!** O FFmpeg precisa ser instalado no seu sistema:

**Windows:**
1. Baixe do site oficial: [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extraia os arquivos e adicione ao PATH do sistema
3. Ou use: `choco install ffmpeg` (se tiver Chocolatey)
4. Ou use: `winget install ffmpeg` (Windows 10+)

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

Para verificar se está instalado corretamente, execute:
```bash
ffmpeg -version
```

### Instalação do Projeto

1. **Clone o repositório:**
```bash
git clone https://github.com/matheusnorjosa/baixador_yt.git
cd baixador_yt
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute o aplicativo:**
```bash
python main.py
```

## 📖 Como Usar

### Interface Principal

1. **Cole a URL** do vídeo ou playlist do YouTube no campo de entrada
2. **Selecione o formato:**
   - **MP3**: Para baixar apenas o áudio
   - **MP4**: Para baixar o vídeo completo
3. **Escolha a qualidade** desejada
4. **Clique em "Baixar Agora"** para download imediato
5. **Ou "Adicionar Playlist"** para processar múltiplos vídeos

### Gerenciamento de Fila

- **Pausar**: Interrompe o processamento da fila
- **Retomar**: Continua o processamento
- **Limpar Fila**: Remove todos os itens pendentes
- **Abrir Pasta**: Acessa rapidamente os arquivos baixados

### Configurações

- **Pasta de Download**: Personalize onde salvar os arquivos
- **Qualidade**: Configure a qualidade padrão para MP3/MP4
- **Formato**: Defina o formato padrão (MP3 ou MP4)

## 🏗️ Estrutura do Projeto

```
baixador_yt/
├── main.py              # Aplicação principal
├── requirements.txt     # Dependências Python
├── README.md           # Este arquivo
├── LICENSE             # Licença MIT
├── .gitignore          # Arquivos ignorados pelo Git
├── CONTRIBUTING.md     # Guia de contribuição
├── CODE_OF_CONDUCT.md  # Código de conduta
└── icons/              # Ícones da interface
    ├── download.png
    ├── playlist.png
    ├── folder.png
    ├── pause.png
    ├── play.png
    ├── clear.png
    └── open_folder.png
```

## 🔧 Desenvolvimento

### Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Tkinter/TTK**: Interface gráfica moderna
- **yt-dlp**: Motor de download do YouTube
- **FFmpeg**: Conversão de áudio/vídeo
- **Threading**: Operações assíncronas

### Arquitetura

O projeto segue uma arquitetura orientada a objetos com a classe principal `YouTubeMP3Downloader` que gerencia:

- Interface do usuário
- Sistema de fila de downloads
- Configurações persistentes
- Threading para operações longas
- Tratamento de erros robusto

### Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📋 Roadmap

- [ ] Histórico de downloads
- [ ] Busca de vídeos integrada
- [ ] Download de legendas
- [ ] Suporte a mais formatos (WAV, FLAC)
- [ ] Tema escuro/claro
- [ ] Atalhos de teclado
- [ ] Drag & drop de URLs

## 🐛 Resolução de Problemas

### Erro: "FFmpeg not found"
- Certifique-se de que o FFmpeg está instalado no sistema
- Verifique se está no PATH: `ffmpeg -version`
- Reinstale o FFmpeg seguindo as instruções de instalação acima

### Erro: "couldn't open 'icons/...'"
- Verifique se a pasta `icons/` existe e contém todos os arquivos PNG
- Os ícones devem ter fundo transparente

### Download falha
- Verifique sua conexão com a internet
- Alguns vídeos podem ter restrições de download
- Tente com uma URL diferente

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Matheus Norjosa**
- GitHub: [@matheusnorjosa](https://github.com/matheusnorjosa)

## 🙏 Agradecimentos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Motor de download
- [FFmpeg](https://ffmpeg.org/) - Conversão de mídia
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Interface gráfica

## ⭐ Se este projeto te ajudou, considere dar uma estrela!

---

**⚠️ Aviso Legal**: Este software é apenas para fins educacionais. Respeite os termos de serviço do YouTube e os direitos autorais dos criadores de conteúdo.
