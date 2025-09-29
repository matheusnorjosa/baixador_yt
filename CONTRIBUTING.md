# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o YouTube MP3/MP4 Downloader PRO! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Como Contribuir

### 1. Fork e Clone

1. Faça um fork do repositório
2. Clone seu fork localmente:
```bash
git clone https://github.com/SEU_USUARIO/baixador_yt.git
cd baixador_yt
```

### 2. Configurar Ambiente de Desenvolvimento

1. Crie um ambiente virtual:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Instale o FFmpeg (veja o README.md para instruções detalhadas)

### 3. Criar uma Branch

```bash
git checkout -b feature/nome-da-sua-feature
# ou
git checkout -b fix/descricao-do-bug
```

### 4. Fazer Mudanças

- Mantenha o código limpo e bem documentado
- Siga o estilo de código existente
- Adicione comentários para código complexo
- Teste suas mudanças antes de fazer commit

### 5. Testar

Execute o aplicativo para garantir que tudo funciona:
```bash
python main.py
```

### 6. Commit e Push

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade X"
git push origin feature/nome-da-sua-feature
```

### 7. Pull Request

1. Vá para o repositório original no GitHub
2. Clique em "New Pull Request"
3. Descreva suas mudanças claramente
4. Aguarde a revisão

## 📝 Convenções de Commit

Use o padrão [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` mudanças na documentação
- `style:` formatação, ponto e vírgula, etc.
- `refactor:` refatoração de código
- `test:` adição de testes
- `chore:` mudanças em ferramentas, configurações, etc.

Exemplos:
```
feat: adiciona suporte a download de legendas
fix: corrige erro de validação de URL
docs: atualiza instruções de instalação
```

## 🎯 Áreas para Contribuição

### Funcionalidades
- [ ] Histórico de downloads
- [ ] Busca de vídeos integrada
- [ ] Download de legendas
- [ ] Suporte a mais formatos (WAV, FLAC)
- [ ] Configurações avançadas (proxy, cookies)

### Interface
- [ ] Tema escuro/claro
- [ ] Atalhos de teclado
- [ ] Drag & drop de URLs
- [ ] Preview de vídeo
- [ ] Melhorias de acessibilidade

### Técnico
- [ ] Testes automatizados
- [ ] Logs mais detalhados
- [ ] Retry automático para downloads falhados
- [ ] Downloads paralelos
- [ ] Validação de URL melhorada

### Documentação
- [ ] Guias de instalação para diferentes sistemas
- [ ] Screenshots da interface
- [ ] Vídeo tutorial
- [ ] FAQ expandido

## 🐛 Reportando Bugs

Ao reportar um bug, inclua:

1. **Descrição clara** do problema
2. **Passos para reproduzir** o bug
3. **Comportamento esperado** vs **comportamento atual**
4. **Screenshots** se aplicável
5. **Informações do sistema:**
   - Sistema operacional
   - Versão do Python
   - Versão do FFmpeg

## 💡 Sugerindo Funcionalidades

Para sugerir novas funcionalidades:

1. Verifique se já não foi sugerida
2. Descreva a funcionalidade detalhadamente
3. Explique o caso de uso
4. Considere implementar você mesmo!

## 📋 Checklist para Pull Requests

- [ ] Código segue o estilo existente
- [ ] Mudanças foram testadas
- [ ] Documentação foi atualizada se necessário
- [ ] Commit messages seguem as convenções
- [ ] Não há conflitos com a branch principal

## 🏷️ Labels

- `bug`: Algo não está funcionando
- `enhancement`: Nova funcionalidade ou melhoria
- `documentation`: Melhorias na documentação
- `good first issue`: Bom para iniciantes
- `help wanted`: Precisa de ajuda extra
- `question`: Mais informações são necessárias

## 📞 Suporte

Se você tem dúvidas sobre como contribuir:

1. Abra uma [issue](https://github.com/matheusnorjosa/baixador_yt/issues)
2. Use o label `question`
3. Descreva sua dúvida claramente

## 🙏 Obrigado!

Sua contribuição é muito valorizada! Cada contribuição, por menor que seja, ajuda a tornar este projeto melhor para todos.

---

**Lembre-se**: Este é um projeto de código aberto. Seja respeitoso, construtivo e siga o [Código de Conduta](CODE_OF_CONDUCT.md).
