CREATE TABLE IF NOT EXISTS file (
    id BIGINT UNSIGNED,
    filename VARCHAR(1000),
    last_updated_on VARCHAR(20),
    url TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS insurer (
    id BIGINT UNSIGNED,
    reporting_entity_name VARCHAR(500),
    reporting_entity_type VARCHAR(500),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS code (
    id BIGINT UNSIGNED,
    billing_code_type_version VARCHAR(20),
    billing_code VARCHAR(14),
    billing_code_type ENUM("CPT","HCPCS","ICD","MS-DRG","R-DRG","S-DRG","APS-DRG","AP-DRG","APR-DRG","APC","NDC","HIPPS","LOCAL","EAPG","CDT","RC","CSTM-ALL"),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS price_metadata (
    id BIGINT UNSIGNED,
    billing_class ENUM("professional", "institutional") COLLATE utf8mb4_general_ci,
--    negotiated_type ENUM("negotiated", "derived", "fee schedule", "percentage", "per diem") COLLATE utf8mb4_general_ci,
    service_code JSON,
    expiration_date VARCHAR(20),
    additional_information TEXT,
    billing_code_modifier JSON,
    PRIMARY KEY (id)
);

-- Theory: for a given insurer/code/price there is a unique rate, or a
-- small number of rates

CREATE TABLE IF NOT EXISTS rate (
    id BIGINT UNSIGNED,
    insurer_id BIGINT UNSIGNED,
    code_id BIGINT UNSIGNED,
    price_metadata_id BIGINT UNSIGNED,
    negotiated_rate DECIMAL(9,2),
    PRIMARY KEY (id),
    FOREIGN KEY (code_id) REFERENCES code(id),
    FOREIGN KEY (insurer_id) REFERENCES insurer(id),
    FOREIGN KEY (price_metadata_id) REFERENCES price_metadata(id)
);

-- Bookkeeping table

CREATE TABLE IF NOT EXISTS file_rate (
    file_id BIGINT UNSIGNED,
    rate_id BIGINT UNSIGNED,
    PRIMARY KEY (file_id, rate_id),
    FOREIGN KEY (file_id) REFERENCES file(id),
    FOREIGN KEY (rate_id) REFERENCES rate(id)
);

-- There may be many providers associated with each rate

CREATE TABLE IF NOT EXISTS npi_rate (
    rate_id BIGINT UNSIGNED,
    npi INT UNSIGNED,
    PRIMARY KEY (npi, rate_id),
    FOREIGN KEY (rate_id) REFERENCES rate(id)
);