# docker-workshp
workshop codespaces


# Preparar el ambiente manualmente

## 1. Run Network para conectar los contenedores
docker network create pg-network

## 2. Run Postgres
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

## 3. Run PgAdmin para visualizacion de los datos
docker run -it --rm \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4

## 4. Dependencias de uv
  Asegurarse que en el uv.lock y pyproject.toml esten todas las dependencias que debemos usar:
    "click>=8.5.0" # para correr el pipeline pasandole parametros al cli
    "pandas>=3.0.5" # extracion y lectura de los datos
    "psycopg2-binary>=2.9.12"
    "pyarrow>=25.0.1"
    "sqlalchemy>=2.0.52" # insertar los datos en la base de datos
    "tqdm>=4.70.0" # visualizacion de la carga de datos al ejecutar el data_ingest.py manualmente

## 5. Build images
  Solo se necesita una imagen para este proceso, a pesar que creamos varias con diferentes objetivos
  > docker build -t taxi_ingest:v001 .
  En el Dockerfile se definen las carpetas directorio, los archivos a usar e importar para dependencias

## 6. Volume
  Con un docker-compose.yaml file definimos los valores de nuestros contenedores:
    - Servicios que se ejecutan, se les define:
      name
      image
      parametros
      volumen mapping (source:destination)
      puertos
    - Volumenes a usar



### Connect pgAdmin to PostgreSQL para visualizacion de los datos cargados

You should now be able to load pgAdmin on a web browser by browsing to http://localhost:8085. 

Open browser and go to http://localhost:8085
Login with email: admin@admin.com, password: root
Right-click "Servers" → Register → Server
Configure:
General tab: Name: Local Docker
Connection tab:
Host: pgdatabase (the container name)
Port: 5432
Username: root
Password: root
Save





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


# Dockerize pipeline

ejecutar el pipeline desde el Dockerfile


## Ejecutar el data_ingest.py manualmente ya con el Docker-compose.yaml creado
Construiir el dockerfile actualizado
> docker build -t taxi_ingest:v001

docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips_2021_2 \
    --year=2021 \
    --month=2 \
    --chunksize=100000







# Step by step:
Crear carpetas del proyecto
## inicializar el proyecto python con uv (.toml)
uv init
## definir version de python en uv

## instalar dependencias principales en uv
uv add click pandas psycopg2-binary pyarrow sqlalchemy tqdm
### instalar dependencias DEV
uv add --dev jupyter pgcli

**Esto actualiza el uv.lock

## crear el ingest_data.py
descarga
lectura
conversion de types
Conectarse a PostgreSQL
crear tabla
insertar
*Usa click para parametrizar la llamada del pipeline

## docker-compose.yaml
Define servicios de postgres y pgadmin
imagen postgres:18
imagen dpage:pgadmin4
variables de pgdatabase y pgadmin
puertos
volume mapping

## levantar contenedores
docker compose up -d
** crea en automatico el docker network con nombre predeterminado
** contenedores
** volumenes

## Validar conexion de Postgres y website de PgAdmin4

> docker ps
docker exec pipeline-pgdatabase-1 pg_isready -U root -d ny_taxi
http://localhost:8085


## Crear el Dockerfile para empaquetar el pipeline

## construir la imagen del pipeline
> docker build -t taxi_ingest:v001 .

## Ejecutar el pipeline desde el Docker contenedor
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-password=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_2 \
  --year=2021 \
  --month=2 \
  --chunksize=100000