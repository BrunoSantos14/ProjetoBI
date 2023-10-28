# Criação do Database projetobi


## Descrição do Projeto

Este projeto foi desenvolvido como parte da disciplina de Business Intelligence do curso BI Master. Consiste em um script Python responsável pela criação do modelo transacional do projeto, incluindo tabelas e relacionamentos.

## Funcionalidades

### 1. Criação de Tabelas

* Utilizou-se principalmente as bibliotecas pandas e Faker.
* As tabelas "funcionarios" e "clientes" foram criadas com dados fictícios gerados pela biblioteca Faker.
* As tabelas "filiais" e "cargos" foram criadas manualmente, devido ao menor porte.
* A tabela de "produtos" foi gerada no Mackaroo, e posteriormente transformada em um dicionário para facilitar a implementação no código.
* A tabela de "vendas" foi gerada aleatoriamente processando os dados das outras tabelas.

### 2. Cadastro do Banco

* Responsável pela criação do database *projetobi* no PostgreSQL.
* Adiciona as tabelas do projeto juntamente com seus relacionamentos.

### 3. Interface Gráfica

Utilizou-se o ttk bootstrap para criar uma interface gráfica amigável.

Permite que qualquer usuário, mesmo sem familiaridade com Python, acesse a base de dados.

![1696959894132](image/README/1696959894132.png)

## Instruções de Uso

1. Execute o arquivo exe disponibilizado ou execute o script *app.py*.
2. Ao ser iniciado, o sistema irá solicitar o login e senha do PostgreSQL.
3. Um popup do Windows irá aparecer em verde caso o banco tenha sido cadastrado com sucesso, ou em vermelho em caso de erro.

   ![1696960028544](image/README/1696960028544.png)

## Observações

* Requer a versão 15.6 do PostgreSQL para cadastro correto. Versões anteriores não são suportadas e futuras não foram verificadas.
* O sistema só pode ser executado uma única vez. Ele irá criar o database chamado *projetobi* com as tabelas e relacionamentos necessários.
