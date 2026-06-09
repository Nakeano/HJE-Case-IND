# PulseCheck

Projeto acadêmico desenvolvido para o case PulseCheck — Programa de Trainee HJE.

O objetivo do MVP é criar um painel interno de monitoramento cardíaco que permite à equipe acompanhar em tempo real o estado das medições dos usuários, identificar sessões com alertas pendentes e registrar revisões clínicas com rastreabilidade de operador.

## Tecnologias utilizadas

- HTML
- CSS
- JavaScript
- Python
- Flask
- Flask-CORS

## Estrutura de pastas

```
HJE-Case-IND/
├── backend/
│   ├── app.py
│   ├── data.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html
├── README.md
└── .gitignore
```

## Pré-requisitos

- Python 3.10+
- pip

## Como rodar localmente

**1. Clone o repositório**

```bash
git clone https://github.com/Nakeano/HJE-Case-IND.git
cd HJE-Case-IND
```

**2. Instale as dependências**

```bash
cd backend
pip install -r requirements.txt
```

**3. Inicie o backend**

```bash
python app.py
```

O servidor ficará disponível em `http://localhost:5000`.

**4. Abra o frontend**

Abra o arquivo `frontend/index.html` diretamente no navegador.

## Rotas disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/usuarios` | Lista todos os usuários com dados de monitoramento |
| `GET` | `/usuarios/<id>` | Retorna dados e histórico de medições de um usuário |
| `POST` | `/usuarios/<id>/acompanhamento` | Registra revisão de um caso Irregular |
