# Validador de Planilhas

Esta é uma aplicação web para validar o formato e os tipos de dados de planilhas.

## Funcionalidades

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
    git clone <url-do-repositorio>
    cd validador-planilha
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