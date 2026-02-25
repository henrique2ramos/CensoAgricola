CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE produtores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome_razao_social VARCHAR(255) NOT NULL,
    documento VARCHAR(18) UNIQUE NOT NULL, -- CPF ou CNPJ
    inscricao_estadual VARCHAR(20),
    tipo_vinculo VARCHAR(50), -- Proprietário, Arrendatário, etc.
    telefone VARCHAR(20),
    email VARCHAR(100),
    criado_em TIMES TAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE propriedades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    produtor_id UUID REFERENCES produtores(id) ON DELETE CASCADE,
    nome_propriedade VARCHAR(255) NOT NULL,
    numero_car VARCHAR(100) UNIQUE, -- Cadastro Ambiental Rural
    numero_ccir VARCHAR(50),
    municipio VARCHAR(100),
    estado CHAR(2),
    area_total_ha NUMERIC(12, 2) NOT NULL,
    area_preservacao_ha NUMERIC(12, 2) DEFAULT 0,
    area_infraestrutura_ha NUMERIC(12, 2) DEFAULT 0,
    -- Localização geográfica simples
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    CONSTRAINT check_areas CHECK (area_total_ha >= (area_preservacao_ha + area_infraestrutura_ha))
);

CREATE TABLE talhoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    propriedade_id UUID REFERENCES propriedades(id) ON DELETE CASCADE,
    identificacao VARCHAR(50), -- Ex: "Talhão 01", "Gleba Norte"
    area_cultivavel_ha NUMERIC(12, 2) NOT NULL,
    tipo_solo VARCHAR(50) -- Arenoso, Argiloso, etc.
);

CREATE TABLE safras (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    talhao_id UUID REFERENCES talhoes(id),
    cultura VARCHAR(100) NOT NULL, -- Soja, Milho, etc.
    variedade VARCHAR(100),
    data_plantio_estimada DATE,
    data_colheita_estimada DATE,
    status VARCHAR(20) DEFAULT 'Planejado', -- Planejado, Em curso, Finalizado
    expectativa_producao NUMERIC(12, 2) -- Em sacos, kg ou toneladas
);