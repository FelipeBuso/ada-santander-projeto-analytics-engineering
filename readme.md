## Venv

- Criar e iniciar ambiente virtual

  `python3 -m venv .venv && source .venv/bin/activate --no-site-packages`

## Bibliotecas

- Instalar bibliotecas do projeto

  `pip install -r  requirements.txt`

## PostgreSQL

- Subir um container com PostgresSQL usando Docker Compose

      - Na raiz do projeto digite:

  `docker compose up -d`

- Caso não tenho o docker compose instalado:

  `https://docs.docker.com/compose/install/`

## Prisma ORM

- Instalando o Prisma

  `pip install prisma`

- Geranda as tabelas do projeto

  `prisma generate --schema ./prisma/schema.prisma`
