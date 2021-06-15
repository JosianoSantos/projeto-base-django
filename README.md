# Projeto base #

#AVISO #

- Sempre excluir o que não for necessário no projeto a ser feito
- Sempre criar um secret key nova, para não usar a mesma em mais de um projeto


Esse projeto usa varáveis de ambiente, é necessário ter um arquivo .env na raizo do projeto com as seguintes configurações:

### .env ###

DEBUG=True

SECRET_KEY='colar aqui a srcret key'

DATABASE_URL=sqlite://./db.sqlite3

DOMINIO_URL=http://localhost:8000

EMAIL_ADMINISTRACAO = ''

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_HOST_USER = ""

EMAIL_HOST_PASSWORD = ""

EMAIL_USE_TLS = True