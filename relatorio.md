# RDS: Replicação de banco de dados com MySQL e Aurora
Relatório para a disciplina de Bancos de Dados Distribuídos

Aluno: Pedro Luiz Domingues

## Criando a instância MySQL
* Acesse o console AWS;
* Acesse o serviço de RDS (Relational Database Service);
* Clique em **Create database**;
* Na seção _Choose a database creation method_ Selecione **_Standard create_** para liberar todas as opções de configuração;
* Em _Engine Options_ selecione **_MySQL_**, edição **_Community_** e a versão pode ser a mais recente disponível (para este relatório foi utilizada a versão 8.0.25);
* Em _Templates_ selecione **_Dev/Test_**;
* Em _Settings_ defina um nome para sua instância (no nosso exemplo foi utilizado _my-employees-main_)
* Logo abaixo, em _Credential settings_ defina um usuário e senha Master para a instância. É recomendado utilizar o usuário `admin` previamente preenchido na interface;. Guarde esses dados pois eles serão usados posteriormente;
* Em _DB Instance Class_  marque a opção **_Burstable classes (includes t classes)_** e ative a opção **_Include previous generation classes_**. Em seguida selecione o Shape **_db.t2.small_** para criar uma instância com o mínimo de recursos possível (para diminuir custos);
* Em _Storage_, altere o tipo e tamanho do armazenamento como preferir, neste tutorial deixaremos os valores padrão;
* Nesta mesma seção desative a opção **_Enable storage autoscaling_** para evitar custos desnecessários;
* Em _Availability & durability_ deixe selecionada a opção **_Do not create a standby instance_**;
* Na seção _Connectivity_ Apenas a opção **_Public access_** para **_Yes_**. O resto deixe como está;
* Em _Database authentication_ deixe marcado **_Password authentication_**;
* Expanda a seção _Additional configuration_
	* Desmarque a opção **_Enable automatic backups_**;
	* Desmarque a opção **_Enable encryption_**;
	* Desmarque a opção **_Enable Enhanced monitoring_**;
	* Desmarque a opção **_Enable auto minor version upgrade_**;
* Clique em **_Create Database_**, em alguns minutos ela estará de pé com status "Available" na tela que aparecer. Caso o status não atualize dê um F5 na página.

## Criando a Replicação com Aurora
* Na página em que o tutorial anterior nos deixou (Console AWS > RDS > Databases), Marque a instância criada, clique em **_Actions_**  e **_Create read replica_**. Uma nova tela se abrirá para configuração da instância;
* Em **_Settings_** defina um nome para a instância de réplica. No nosso exemplo utilizamos `aurora-employees-replica`;
* Em _Region_ deixe o valor padrão;
* Em _DB Instance Class_  selecione o mesmo shape utilizado para a instância principal (**_db.t2.small_**);
* Em Storage, demarque a opção **_Enable storage autoscaling_**;
* Em _Availability & durability_ marque **_Do not create a standby instance_**;
* Em _Connectivity_ marque a opção **_Publicly accessible_** e deixe o resto como está;
* Em _Database authentication_ marque **_Password authentication_**;
* Expanda a seção _Additional configuration_
	* Desmarque a opção **_Enable encryption_**;
	* Desmarque a opção **_Enable Enhanced monitoring_**;
	* Desmarque a opção **_Enable auto minor version upgrade_**;
* Clique em **_Create Read Replica_**, em alguns minutos ela estará de pé com status "Available" na tela que aparecer. Caso o status não atualize dê um F5 na página.

Ao final da criação das duas intâncias o painel do RDS deve se parecer com isso:
![Painel RDS](https://i.imgur.com/2ABEg4C.png)

## Acessando as instâncias
Para este tutorial utilizamos o software _Datagrip_ para acesso às instâncias. A Jetbrains disponibiliza licenças de estudante utilizando o email da Fatec no cadastro. É possível se cadastrar neste site: [https://www.jetbrains.com/pt-br/community/education/](https://www.jetbrains.com/pt-br/community/education/).
> O mesmo tutorial serve tanto para acessar o banco principal como o MySQL.

* Acesse a listagem de bancos de dados dentro do painel do RDS;
* Clique sobre o nome da instância que deseja acessar;
* Na seção _Connectivity & security_, dentro de _Endpoint & port_, haverá um item chamado _Endpoint_ com um endereço num formato parecido com este: `nome-da-instancia.id-da-conta.us-east-1.rds.amazonaws.com`. Copie este link;
* Dentro do Datagrip, acesse o menu lateral _Database_ e clique no símbolo de `+`;
* No menu dropdown que aparecer selecione **Data Source** e **MySQL** (Este tipo de datasource também é compatível com o Aurora);
* No Popup que surgir preencha da seguinte forma:
	* **Host:** Endereço copiado do painel da AWS;
	* **Port:** 3306 (ou a porta que você configurou no painel, caso tenha alterado);
	* **User:** Usuário master informado no momento da criação da instância;
	*  **Password:** Senha master informada no momento da criação da instância;
* Caso o Datagrip dê um aviso de "_missing drivers_", clique no botão "Download" que aparecerá. Isso baixará os drivers de conexão necessários;
* Clique em _Test Connection_ para garantir que está tudo certo; 

Ao final, se tudo estiver correto você deve ter uma tela parecida com esta:
![Datasource Datagrip](https://i.imgur.com/PGOUv8p.png)

* Clique em _OK_ para fechar a janela e iniciar a conexão com o banco de dados;
* Uma guia console será aberta para execução de queries. Você também pode abrir arquivos `.sql` para executar na base por dentro do programa.
* Caso deseje, para abrir uma nova guia de console selecione o Data Source criado e clique no ícone de console no topo da guia;

## Testando a replicação
Para alimentar o banco de dados foi desenvolvido o seguinte projeto: [https://github.com/PedroLuiz99/fatec-s05-bds-distribuidos](https://github.com/PedroLuiz99/fatec-s05-bds-distribuidos)

* Execute o arquivo `001-ddl-and-roles.sql` no banco de dados principal para criar as tabelas
* Execute o arquivo `data_generator/generated_employees.sql` no banco de dados principal para popular as tabelas com dados gerados automaticamente.
* Caso deseje gerar novos dados leia as instruções no arquivo `README.md`

Todos os dados criados deve aparecer replicados nos dois bancos de dados como nas imagens abaixo:

### Employee
Nó principal:
![](https://i.imgur.com/dFcJi10.png)

Nó réplica:
![](https://i.imgur.com/o207LEt.png)


### Payroll
Nó principal:
![](https://i.imgur.com/1aujO3r.png)

Nó réplica:
![](https://i.imgur.com/qCIpQ1C.png)


### Payroll Item
Nó principal:
![](https://i.imgur.com/5VhWaAi.png)

Nó réplica:
![](https://i.imgur.com/flEQDPw.png)


