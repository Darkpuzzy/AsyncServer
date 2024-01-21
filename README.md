# Async Sockets Server and Client manager

---

_Install requirements_

```
pip install alembic
pip install -r requirements.txt
```

[//]: # (_Initialization Alembic in directory "migrations"_)

[//]: # (```)

[//]: # (alembic init migrations)

[//]: # (```)

Migrations alembic:
```
cd server/

alembic upgrade head
```

Reverse migration:
```
alembic downgrade -1
```init – prepares the project to work with alembic
upgrade – upgrade the database to a later version
downgrade – revert to a previous version
revision – creates a new revision file
```


# _RUNNING_

_Start Server_
```
cd server
python osi_server.py
```

_Start Client_
Two client, where client_adm.py is admin client, client_vm.py is just client virtual machine
```
python client/client_adm.py
python client/client_vm.py
```

_For a client, enter ___help___ in terminal_


# _Stack_

- [x] <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-plain.svg" alt="postgresql" width="15" height="15"/> PostgreSQL <br/>
- [x] <a href="https://docs.sqlalchemy.org/en/20"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlalchemy/sqlalchemy-plain.svg" alt="sqlalchemy" width="15" height="15"/> SqlAlchemy 2.0<br/></a>
- [x] <a href="https://docs.pydantic.dev/">🕳 Pydantic 2.5.1<br/></a>
- [x] <a href="https://alembic.sqlalchemy.org/en/latest/">⚗ Alembic<br/></a>
