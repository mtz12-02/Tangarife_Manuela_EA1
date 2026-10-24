
import psycopg


def obtener_conexion():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="autos_colombia",
        user="postgres",
        password="Manuelatz12@$"
    )

import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    return psycopg.connect(
        host="localhost",
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "autos_colombia"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )