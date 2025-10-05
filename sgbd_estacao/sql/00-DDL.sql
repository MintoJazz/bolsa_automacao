DROP DATABASE IF EXISTS sistema_estacao;

CREATE DATABASE sistema_estacao;

\c sistema_estacao;

CREATE TABLE estacao (
    id SERIAL PRIMARY KEY,
    codinome VARCHAR(200) NOT NULL,
    localidade VARCHAR(200)
)

CREATE TABLE sensor (
    id SERIAL PRIMARY KEY,
    modelo VARCHAR(200) NOT NULL,
    id_estacao INTEGER REFERENCES estacao(id) ON DELETE CASCADE
)

CREATE TABLE medicao (
    id SERIAL PRIMARY KEY,
    data_hora TIMESTAMP,
    valor REAL, -- real é uma boa escolha pra lidar com os sensores?
    id_sensor INTEGER REFERENCES sensor(id) ON DELETE CASCADE,
    id_variável INTEGER REFERENCES variavel(id) ON DELETE CASCADE
)

CREATE TABLE variavel (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL
    -- unidade de medida??
)