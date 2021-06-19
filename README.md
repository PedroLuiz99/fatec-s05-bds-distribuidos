# Fatec - Projeto de Bancos de Dados Distribuídos
Banco de dados e gerador de registros simples para implementação do projeto de replicação MySQL → Aurora utilizando RDS.


# Dependências
* MySQL Server
* Python 3.6 ou superior (Apenas se for re-gerar os dados de exemplo)
* Pip (Apenas se for re-gerar os dados de exemplo)
  
# Dependências do Pip
Somente será necessário caso deseje re-gerar os dados de exemplo.
* Faker
* Dateutil

Você pode instalá-las com o comando `pip install -r data_generator/requirements.txt`

# Executando o projeto
Para criação das tabelas, rode o arquivo `001-ddl-and-roles.sql` dentro da sua instância de banco de dados;

Para popular o banco de dados, você pode utilizar o arquivo `data_generator/generated_employees.sql` deste projeto ou gerar um novo seguindo os passos abaixo:
* Com as dependências instaladas, abra um shell dentro do diretório `data_generator` e execute o comando:
```shell
python generate_employees.py
```

* O comando gerará um novo arquivo `generated_employees.sql` com 50 funcionários e suas folhas de pagamento.