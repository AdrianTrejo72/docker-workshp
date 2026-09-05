#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import click
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# Este diccionario define el tipo de dato de cada columna del archivo CSV.
# Usar tipos explícitos evita conversiones inesperadas durante la ingestión.
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}
# Estas columnas contienen fechas y serán convertidas automáticamente por pandas.
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# Click convierte los argumentos de la terminal en parámetros de esta función.
# Así podemos reutilizar el pipeline para distintos meses, bases de datos y tablas.
@click.command()
@click.option('--year', default=2021, type=int)
@click.option('--month', default=1, type=int)
@click.option('--pg-user', default='root')
@click.option('--pg-password', default='root')
@click.option('--pg-host', default='localhost')
@click.option('--pg-db', default='ny_taxi')
@click.option('--pg-port', default=5432, type=int)
@click.option('--chunksize', default=100000, type=int)
@click.option('--target-table', default='yellow_taxi_data')
def run(year, month, pg_user, pg_password, pg_host, pg_db, pg_port, chunksize, target_table):

    # Construimos la URL del archivo a partir del año y el mes recibidos.
    # :02d mantiene el mes con dos dígitos, por ejemplo 01, 02 o 12.
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    # Creamos la conexión con PostgreSQL usando SQLAlchemy.
    # La conexión se reutilizará para cargar todos los fragmentos del archivo.
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')


    # Leemos el CSV por fragmentos en lugar de cargarlo completo en memoria.
    # Esto es importante en pipelines de datos porque los archivos pueden ser grandes.
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )
    
    # El primer fragmento crea la tabla y los siguientes agregan sus filas.
    # `first` controla que `replace` se ejecute una sola vez.
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            # head(0) conserva las columnas, pero no inserta ninguna fila.
            # to_sql usa esa estructura para crear la tabla en PostgreSQL.
            df_chunk.head(0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace'
            )
            first = False

        # Insertamos el fragmento actual en la tabla existente.
        df_chunk.to_sql(
            name=target_table,
            con=engine, 
            if_exists='append'
        )

    # Este bloque solo llama a run() cuando ejecutamos este archivo directamente.
    # Si otro módulo lo importa, el pipeline no se ejecuta de forma automática.
if __name__ == '__main__':
    run()