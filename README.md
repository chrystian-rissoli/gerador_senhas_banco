# Gerador de Senhas Bancarias

Projeto academico de DevOps com uma API simples em Python + Flask para geracao de senhas seguras, testes com `pytest`, containerizacao com Docker e automacao com GitHub Actions.

## Objetivo

Disponibilizar uma API REST enxuta para gerar senhas fortes com parametros configuraveis, mantendo uma estrutura clara e facil de validar nas etapas da disciplina.

## Estrutura do projeto

```text
.
|-- .github/workflows/
|-- app.py
|-- Dockerfile
|-- requirements.txt
|-- tests/test_app.py
`-- README.md
```

## Como executar localmente

### 1. Criar e ativar ambiente virtual

No Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Executar a aplicacao

```bash
python app.py
```

Aplicacao disponivel em `http://localhost:5000`.

## Testes

```bash
pytest -q
```

## Rotas da API

- `GET /` retorna uma mensagem simples indicando que a API esta no ar.
- `GET /health` retorna o status da aplicacao em JSON.
- `GET /gerar-senha` gera uma senha aleatoria com parametros opcionais via query string.

Parametros disponiveis em `GET /gerar-senha`:

- `comprimento` (int, padrao `12`): comprimento da senha entre 8 e 128.
- `maiusculas` (bool, padrao `true`): inclui letras maiusculas.
- `minusculas` (bool, padrao `true`): inclui letras minusculas.
- `numeros` (bool, padrao `true`): inclui numeros.
- `especiais` (bool, padrao `true`): inclui caracteres especiais.

Exemplo:

```text
GET /gerar-senha?comprimento=16&especiais=false
```

## Docker

### Build da imagem

```bash
docker build -t gerador-senhas-banco:latest .
```

### Executar o container

```bash
docker run --name gerador-senhas-banco -d -p 5000:5000 gerador-senhas-banco:latest
```

### Testar a API em container

```bash
curl http://localhost:5000/health
```

## GitHub Actions

- `CI`: instala dependencias e executa os testes com `pytest`.
- `CD`: valida o build da imagem Docker em push e pull request, sem depender de Docker Hub ou secrets externos.
