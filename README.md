# Ponto - Controle de Horas Extras

![GitHub](https://img.shields.io/badge/version-0.0.1-blue)
![GitHub](https://img.shields.io/badge/license-MIT-green)

**Ponto** é uma ferramenta simples e eficaz para gerenciar o controle de horários e calcular horas extras. Desenvolvido em Python, este programa permite que você registre, liste e exclua entradas de horários de trabalho, além de calcular automaticamente as horas extras com base na jornada de trabalho padrão de 9 horas.

## 🚀 Começando

### Pré-requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados:

- Python 3.x
- PostgreSQL
- `psycopg2` (biblioteca para conexão com PostgreSQL)
- `python-dotenv` (para gerenciamento de variáveis de ambiente)

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/pablodeas/ponto.git
   cd ponto
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados:

   - Crie um banco de dados PostgreSQL.
   - Crie a tabela necessária com o seguinte comando SQL:

     ```sql
     CREATE TABLE public.ponto (
         id SERIAL PRIMARY KEY,
         hr_begin TIME NOT NULL,
         hr_end TIME NOT NULL,
         dia DATE NOT NULL,
         extra INTEGER NOT NULL
     );
     ```

4. Configure as variáveis de ambiente:

   - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

     ```env
     DATABASE=nome_do_banco
     DB_USER=usuario
     DB_PASSWORD=senha
     DB_CONTAINER=container
     HOST=host
     PORT=porta
     ```

## 📋 Uso

O **Ponto** é uma aplicação de linha de comando (CLI) que oferece os seguintes comandos:

### Listar Registros

Para listar todos os registros de horários:

```bash
python3 main.py list
```

### Inserir Registro

Para inserir um novo registro de horário:

```bash
python3 main.py insert <entrada> <saida> <data>
```

- `<entrada>`: Horário de entrada no formato `HH:MM` (ex: `08:00`).
- `<saida>`: Horário de saída no formato `HH:MM` (ex: `17:30`).
- `<data>`: Data no formato `YYYY-MM-DD` (ex: `2025-02-28`).

### Excluir Registro

Para excluir um registro pelo ID:

```bash
python3 main.py delete <id>
```

- `<id>`: ID do registro que deseja excluir.

## 🛠️ Funcionalidades

- **Cálculo Automático de Horas Extras**: O programa calcula automaticamente as horas extras com base na jornada de trabalho de 9 horas.
- **Registro de Horários**: Permite registrar horários de entrada e saída.
- **Listagem de Registros**: Exibe todos os registros de horários de forma organizada.
- **Exclusão de Registros**: Permite a exclusão de registros pelo ID.

## 👏 Contribuição

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

Developed by [Pablo Andrade](https://github.com/pablodeas).