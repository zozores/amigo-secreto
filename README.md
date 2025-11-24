# 🎁 Amigo Secreto

Aplicação web simples e moderna para realizar sorteios de Amigo Secreto, desenvolvida com Python (FastAPI) e Tailwind CSS.

## 🚀 Funcionalidades

- **Painel Administrativo**: Protegido por senha.
- **Cadastro de Participantes**: Adicione nomes facilmente.
- **Sorteio Automático**: Algoritmo que garante que ninguém tire a si mesmo.
- **Links Mágicos**: Cada participante recebe um link único para revelar seu amigo secreto.
- **Interface Responsiva**: Design limpo e moderno com Tailwind CSS.

## 🛠️ Tecnologias

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, SQLite.
- **Frontend**: HTML5, Jinja2 Templates, Tailwind CSS (CDN).
- **Containerização**: Docker.

## 📦 Como Rodar

### Pré-requisitos

- Python 3.11+
- Pip

### Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/amigo-secreto.git
   cd amigo-secreto
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   uvicorn main:app --reload
   ```

4. Acesse `http://127.0.0.1:8000`.

### 🐳 Rodando com Docker

1. Construa a imagem:
   ```bash
   docker build -t amigo-secreto .
   ```

2. Execute o container:
   ```bash
   docker run -d -p 8000:8000 -e SECRET_KEY=sua_chave_secreta -e ADMIN_PASSWORD=admin amigo-secreto
   ```

## 🔑 Acesso

- **Senha Padrão do Admin**: `admin` (ou a definida na variável de ambiente `ADMIN_PASSWORD`).
- **Rota de Revelação**: Pública, acessível apenas via link gerado (token UUID).

## 📝 Licença

Este projeto está sob a licença MIT.
