CREATE TABLE produtores (
    id SERIAL PRIMARY KEY, -- ID autoincremento (1, 2, 3...)
    nome_razao_social VARCHAR(255) NOT NULL,
    documento VARCHAR(18) UNIQUE NOT NULL, -- CPF ou CNPJ
    inscricao_estadual VARCHAR(20),
    tipo_vinculo VARCHAR(50), -- Proprietário, Arrendatário, etc.
    telefone VARCHAR(20),
    email VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE propriedades (
    id SERIAL PRIMARY KEY,
    produtor_id INTEGER REFERENCES produtores(id) ON DELETE CASCADE, -- Referência numérica
    nome_propriedade VARCHAR(255) NOT NULL,
    numero_car VARCHAR(100) UNIQUE, -- Cadastro Ambiental Rural
    numero_ccir VARCHAR(50),
    codigo_municipio CHAR(7),
    codigo_uf CHAR(2),
    area_total_ha NUMERIC(12, 2) NOT NULL,
    area_preservacao_ha NUMERIC(12, 2) DEFAULT 0,
    area_infraestrutura_ha NUMERIC(12, 2) DEFAULT 0,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    CONSTRAINT check_areas CHECK (area_total_ha >= (area_preservacao_ha + area_infraestrutura_ha))
);

CREATE TABLE talhoes (
    id SERIAL PRIMARY KEY,
    propriedade_id INTEGER REFERENCES propriedades(id) ON DELETE CASCADE, -- Referência numérica
    identificacao VARCHAR(50), 
    area_cultivavel_ha NUMERIC(12, 2) NOT NULL,
    cultura VARCHAR(100) NOT NULL,
    tipo_solo VARCHAR(50) 
);

CREATE TABLE safras (
    id SERIAL PRIMARY KEY,
    talhao_id INTEGER REFERENCES talhoes(id), -- Referência numérica
    variedade VARCHAR(100),
    data_plantio_estimada DATE,
    data_colheita_estimada DATE,
    status VARCHAR(20) DEFAULT 'Planejado', 
    expectativa_producao NUMERIC(12, 2) 
);