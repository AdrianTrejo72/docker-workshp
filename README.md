# docker-workshp
workshop codespaces


# Run Postgres

docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

-v es el volume que usare para salvar la informacion...esta no esta en mi maquina, sino en container
-p es Volume mapping del hostport : containerport

Una vez ejecutado el comando y Postgres abierto para la comunicacion: debemos instalar o usar pgcli.... estas se ven el el .toml en el apartado DEV, hasta abajo

Porque DEV? Por que son herramientas unicamente para nosotros poder desarrollar la app, no es algo que se necesita en produccion
# Run pgcli
  > uv add --dev pgcli
para conectarse con pgcli a postgres usamos:

  > uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

  donde:
uv run executes a command in the context of the virtual environment
-h is the host. Since we're running locally we can use localhost.
-p is the port.
-u is the username.
-d is the database name.

pgcli commands:
> /dt -- check databases
Aqui puedo corrr comandos sql para postgres sin necesidad de un portal como SSMS, esto es postgres CLI (CommandLineInterface)

# Instalar Jupyter
> uv add --dev Jupyter 
> uv run jupyter notebook

Creara la instancia de Jupyter y nos conectaremos al puerto abierto (8888) para crear notebooks en el navegador.
** NOTA: Apartir de aqui ya estamos en JUPYTER creando el pipeline con python
** Aqui debemos usar el url y Token que nos da la terminal


En el notebook lo usaremos para generar el script del pipeline:
-Download con el prexif
-Read en chunks con pandas
-Convert datatime columns
-Insert en PostgreSQL usando SQLAlchemy y psycopg2

> uv add sqlalchemy psycopg2-binary
o ejecutar desde el notebook como !uv add sqlalchemy

usar alchemy para conectarse a la base de datos ny_taxy
*** AQUI SE CREO EL SCHEMA EN SQL PARA CREARLO EN EL POSTGRES USANDO sqlalchemy
 SI REVISO EL PGCLI Y HAGO > \dt SE VERA LA NUEVA BASE DE DATOS yellow_taxi_data


# Extraccion, transformacion y carga de datos con Jupyter 
 Ahora hacemos carga de datos en chunks con un iterador
 > df_iter = pd.read_csv(
 >   ...
 >   iterator=True,
 >   chunksize=100000 )

#Iterador de 100mil chunks, pasa los parametro, asigna los dtypes y fechas y activa el modo iterator
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)
# instalar uv add tqdm


#Escribiendo en la base de datos utilizando tqdm para visualizar el progreso del ciclo for
> from tqdm.auto import tqdm
> for df_chunk in tqdm(df_iter):
>     df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


#vamos a descargar el notebook a un archivo .py
> uv run jupyter nbconvert --to=script notebook.ipynb
rename it
> mv notebook.py ingest_data.py
Despues ajustaremos el codigo para limpiarlo.