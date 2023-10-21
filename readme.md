## Venv

- Criar e iniciar ambiente virtual

```
python3 -m venv .venv && source .venv/bin/activate --no-site-packages
```

## Bibliotecas

- Instalar bibliotecas do projeto

```
pip install -r  requirements.txt
```

## Variáveis de ambiente

- Crie um arquivo chamado `.env` na raiz do seu projeto com as os valores das variáveis de ambiente de acordo com àquelas do arquivo `.env.example`.

## PostgreSQL

- Subir um container com PostgresSQL usando Docker Compose

  - Na raiz do projeto digite:

  ```
  docker compose up -d
  ```

  - Caso não tenho o docker compose instalado:

  ```
  https://docs.docker.com/compose/install/
  ```

- Criar um banco de dados no PostgresSQL:

  `acessar o container:`

```
docker exec -it <NOME_DO_CONTAINER> bash
```

`Conectar com o PostgresSQL:`

```
psql -h localhost -U postgres
```

`Criar o banco de dados:`

```
CREATE DATABASE <NOME_DO_BANCO_DE_DADOS>;
```

## Prisma ORM (Opcional)

### Usamos o SQLAlchemy para modelagem e conexão com o POstgresSQL, mas existe a opção de usar o Prisma ORM:

- Instalando o Prisma

```
pip install prisma
```

- Geranda as tabelas do projeto

```
prisma generate --schema ./prisma/schema.prisma
```
