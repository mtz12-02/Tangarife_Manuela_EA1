
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(10) UNIQUE NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    color VARCHAR(30)
);

CREATE TABLE celdas (
    id_celda SERIAL PRIMARY KEY,
    numero VARCHAR(10) UNIQUE NOT NULL,
    ocupada BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE movimientos (
    id_movimiento SERIAL PRIMARY KEY,
    id_vehiculo INTEGER NOT NULL
        REFERENCES vehiculos(id_vehiculo),
    id_celda INTEGER NOT NULL
        REFERENCES celdas(id_celda),
    fecha_entrada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_salida TIMESTAMP,
    CONSTRAINT salida_posterior_entrada
        CHECK (
            fecha_salida IS NULL
            OR fecha_salida >= fecha_entrada
        )
);

CREATE UNIQUE INDEX una_entrada_abierta_por_vehiculo
ON movimientos (id_vehiculo)
WHERE fecha_salida IS NULL;

CREATE UNIQUE INDEX una_ocupacion_por_celda
ON movimientos (id_celda)
WHERE fecha_salida IS NULL;

CREATE TABLE novedades (
    id_novedad SERIAL PRIMARY KEY,
    id_movimiento INTEGER NOT NULL
        REFERENCES movimientos(id_movimiento),
    fecha_novedad TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT NOT NULL
);

INSERT INTO celdas (numero)
VALUES
    ('C01'), ('C02'), ('C03'), ('C04'), ('C05'),
    ('C06'), ('C07'), ('C08'), ('C09'), ('C10')
ON CONFLICT (numero) DO NOTHING;
