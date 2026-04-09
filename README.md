# Validador de Planilhas

Esta é uma aplicação web para validar o formato e os tipos de dados de planilhas.

Criado para resolver o problema nos dados e metadados nos arquivos enviados por usuários para uma pipeline de ETL

## Funcionalidades

-   **Controle de Acesso Baseado em Funções (RBAC):** Separação de permissões para usuários 'Admin' e 'User'.
-   **Gerenciamento de Usuários:** Administradores podem adicionar, editar e excluir usuários. O registro público foi desativado.
-   **Validação de Nomes de Arquivo:** Configure padrões Regex para o nome de arquivos por planilha.
-   **Controle de Versão:** Acompanhe as versões dos arquivos enviados para cada planilha.
-   **Rastreamento de Downloads:** Registra quem e quando baixou cada arquivo.
-   Upload de planilhas nos formatos CSV ou XLSX.
-   Definição de regras de validação para cada planilha, incluindo:
    -   Nome da coluna
    -   Tipo de dado (STRING, INTEGER, FLOAT, DATE, BOOLEAN)
    -   Formato da data (ex: DD/MM/AAAA)
    -   Campo obrigatório
-   Validação de arquivos enviados de acordo com as regras definidas.
-   Visualização de um relatório de erros de validação.
-   Download do relatório de erros em PDF.
-   Se o arquivo for válido, ele é salvo com um ID único e pode ser baixado.
-   Visualizar e baixar planilhas previamente salvas e validadas na página "Arquivos Salvos".

## Tecnologias Utilizadas

-   Python
-   Flask
-   SQLAlchemy
-   PostgreSQL
-   Docker
-   Pandas
-   FPDF

## Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/rickadt/file-data-validator.git
    cd file-data-validator
    ```

2.  **Inicie o banco de dados PostgreSQL:**
    ```bash
    docker-compose up -d
    ```

3.  **Instale as dependências:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

5.  **Acesse a aplicação:**
    Abra seu navegador e vá para `http://127.0.0.1:5000`.

## Como Usar

### Controle de Acesso (RBAC)

A aplicação implementa um controle de acesso baseado em funções (RBAC) com dois tipos de usuários:

-   **Admin:** Pode criar, editar e excluir configurações de planilhas e suas regras de validação. Também pode fazer upload e download de *qualquer* planilha.
-   **User:** Pode apenas fazer upload e download das planilhas para as quais possui permissão de acesso (definida pelos administradores).

### Usuário Administrador Padrão

Após executar o `python create_db.py` pela primeira vez, um usuário administrador padrão será criado automaticamente com as seguintes credenciais:

-   **Usuário (username):** `admin`
-   **Email:** `admin@local`
-   **Senha:** `admin`
-   **Função (role):** `Admin`

Você pode usar essas credenciais para fazer login e começar a configurar planilhas e regras. É **altamente recomendável** que você altere a senha padrão ou crie novos usuários administradores assim que possível.

1.  **Crie uma nova configuração de planilha:**
    -   Vá para a página "Planilhas".
    -   Clique em "Adicionar Planilha" e dê um nome a ela.

2.  **Adicione regras de validação:**
    -   Clique em "Adicionar Regra" para a planilha desejada.
    -   Preencha o formulário com o nome da coluna, tipo de dado, formato da data (se aplicável) e se a coluna é obrigatória.

3.  **Faça upload de uma planilha para validação:**
    -   Vá para a página "Upload".
    -   Escolha o arquivo e selecione a configuração de planilha correspondente.
    -   Clique em "Fazer Upload e Validar".

4.  **Visualize o relatório:**
    -   Se houver erros, um relatório será exibido.
    -   Você pode baixar o relatório em PDF.

5.  **Baixe o arquivo validado:**
    -   Se o arquivo for válido, você será redirecionado para uma página de sucesso com um ID único para o arquivo.
    -   Você pode usar o link fornecido para baixar o arquivo validado.

## Endpoints da API

A aplicação oferece endpoints da API para consulta de arquivos, que podem ser acessados via ferramentas de linha de comando como `curl` ou `wget`, ou a partir de outras aplicações. Todos os endpoints da API exigem autenticação.

Para autenticar em um endpoint da API, você precisa primeiro fazer login na interface web para obter uma sessão válida, ou configurar um mecanismo de autenticação de token (que não está implementado no momento, mas pode ser adicionado).

### Autenticando com `curl` (Obtendo Cookies de Sessão)

Para usar os endpoints da API com `curl`, você precisará de cookies de sessão válidos. Você pode obtê-los fazendo uma requisição de login e salvando os cookies:

1.  **Faça login e salve os cookies:**
    ```bash
    curl -c cookies.txt -X POST -d "username=seu_usuario&password=sua_senha" http://127.0.0.1:5000/login
    ```
    (Substitua `seu_usuario` e `sua_senha` pelas suas credenciais reais. O arquivo `cookies.txt` será criado e conterá seus cookies de sessão.)

2.  **Use os cookies em requisições subsequentes:**
    Com os cookies salvos em `cookies.txt`, você pode usá-los com a flag `-b` (`--cookie`) em suas requisições da API.

    Exemplo:
    ```bash
    curl -b cookies.txt http://127.0.0.1:5000/api/files
    ```

### Listar todos os arquivos

**GET** `/api/files`

Retorna uma lista de todos os arquivos acessíveis ao usuário autenticado.

```bash
curl -b cookies.txt http://127.0.0.1:5000/api/files
```

Exemplo de resposta:

```json
[
  {
    "id": "uuid1",
    "filename": "minha_planilha.csv",
    "spreadsheet_name": "Planilha RH",
    "version": 1,
    "upload_timestamp": "2023-10-27T10:00:00",
    "download_url": "http://127.0.0.1:5000/download/uuid1"
  }
]
```

### Obter o último arquivo enviado

**GET** `/api/files/latest`

Retorna os detalhes do arquivo mais recentemente enviado, acessível ao usuário autenticado.

```bash
curl -b <cookies_da_sessao> http://127.0.0.1:5000/api/files/latest
```

Exemplo de resposta:

```json
{
  "id": "uuid2",
  "filename": "planilha_vendas_q4.xlsx",
  "spreadsheet_name": "Dados de Vendas",
  "version": 3,
  "upload_timestamp": "2023-10-27T11:30:00",
  "download_url": "http://127.0.0.1:5000/download/uuid2"
}
```

### Obter a última versão de um arquivo por nome

**GET** `/api/files/latest_version/<filename>`

Retorna os detalhes da versão mais recente de um arquivo específico, acessível ao usuário autenticado. Substitua `<filename>` pelo nome original do arquivo.

```bash
curl -b <cookies_da_sessao> http://127.0.0.1:5000/api/files/latest_version/minha_planilha.csv
```

Exemplo de resposta:

```json
{
  "id": "uuid1",
  "filename": "minha_planilha.csv",
  "spreadsheet_name": "Planilha RH",
  "version": 5,
  "upload_timestamp": "2023-10-27T14:15:00",
  "download_url": "http://127.0.0.1:5000/download/uuid1"
}
```

### Baixar um arquivo

**GET** `/download/<file_id>`

Este endpoint é o mesmo usado pela interface web. Permite baixar um arquivo específico usando seu ID único. A autenticação é necessária.

```bash
curl -b <cookies_da_sessao> -o arquivo_baixado.ext http://127.0.0.1:5000/download/uuid1
```

### Exemplo de Autenticação e Download com Python (requests)

Para automatizar a interação com a API usando Python, você pode utilizar a biblioteca `requests`. Primeiro, instale-a: `pip install requests`.

```python
import requests
import os

BASE_URL = "http://127.0.0.1:5000"
USERNAME = "seu_usuario"
PASSWORD = "sua_senha"
DOWNLOAD_DIR = "downloads_api"

# 1. Autenticar e obter cookies de sessão
session = requests.Session()
login_data = {
    'username': USERNAME,
    'password': PASSWORD
}
login_response = session.post(f"{BASE_URL}/login", data=login_data)

if "Olá, " not in login_response.text: # Checa se o login foi bem-sucedido (ajustar conforme sua página de sucesso)
    print("Falha na autenticação. Verifique usuário e senha.")
else:
    print(f"Autenticação bem-sucedida para {USERNAME}!")

    # 2. Listar todos os arquivos acessíveis
    print("\nListando todos os arquivos acessíveis:")
    files_response = session.get(f"{BASE_URL}/api/files")
    if files_response.status_code == 200:
        files = files_response.json()
        if files:
            for file_info in files:
                print(f"  - {file_info['filename']} (ID: {file_info['id']}, Versão: {file_info['version']}, Planilha: {file_info['spreadsheet_name']})")
        else:
            print("  Nenhum arquivo encontrado.")
    else:
        print(f"Erro ao listar arquivos: {files_response.status_code} - {files_response.text}")

    # 3. Baixar o arquivo mais recente (exemplo)
    # Primeiro, obter o ID do arquivo mais recente
    latest_file_response = session.get(f"{BASE_URL}/api/files/latest")
    if latest_file_response.status_code == 200:
        latest_file_info = latest_file_response.json()
        if latest_file_info:
            file_id_to_download = latest_file_info['id']
            file_name_to_save = f"latest_{latest_file_info['filename']}" # Nome para salvar no disco
            download_url = f"{BASE_URL}/download/{file_id_to_download}"

            print(f"\nBaixando o arquivo mais recente (ID: {file_id_to_download}, Nome: {file_name_to_save})...")
            download_response = session.get(download_url, stream=True)

            if download_response.status_code == 200:
                os.makedirs(DOWNLOAD_DIR, exist_ok=True)
                download_path = os.path.join(DOWNLOAD_DIR, file_name_to_save)
                with open(download_path, 'wb') as f:
                    for chunk in download_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Arquivo baixado com sucesso para: {download_path}")
            else:
                print(f"Erro ao baixar arquivo: {download_response.status_code} - {download_response.text}")
        else:
            print("Nenhum arquivo recente para baixar.")
    else:
        print(f"Erro ao obter o último arquivo: {latest_file_response.status_code} - {latest_file_response.text}")

    # 4. Baixar a última versão de um arquivo específico (exemplo)
    specific_filename = "planilha_exemplo.xlsx" # Substitua pelo nome do arquivo que você quer
    latest_version_response = session.get(f"{BASE_URL}/api/files/latest_version/{specific_filename}")
    if latest_version_response.status_code == 200:
        specific_file_info = latest_version_response.json()
        if specific_file_info:
            file_id_to_download = specific_file_info['id']
            file_name_to_save = f"latest_version_{specific_file_info['filename']}"
            download_url = f"{BASE_URL}/download/{file_id_to_download}"

            print(f"\nBaixando a última versão de '{specific_filename}' (ID: {file_id_to_download}, Nome: {file_name_to_save})...")
            download_response = session.get(download_url, stream=True)

            if download_response.status_code == 200:
                os.makedirs(DOWNLOAD_DIR, exist_ok=True)
                download_path = os.path.join(DOWNLOAD_DIR, file_name_to_save)
                with open(download_path, 'wb') as f:
                    for chunk in download_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Arquivo baixado com sucesso para: {download_path}")
            else:
                print(f"Erro ao baixar arquivo: {download_response.status_code} - {download_response.text}")
        else:
            print(f"Nenhuma versão de '{specific_filename}' encontrada.")
    else:
        print(f"Erro ao obter a última versão de '{specific_filename}': {latest_version_response.status_code} - {latest_version_response.text}")
```

