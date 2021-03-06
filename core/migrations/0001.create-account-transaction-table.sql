CREATE TABLE account_transaction (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nordigen_transaction_id VARCHAR(128) UNIQUE,
    title VARCHAR(512) NOT NULL,
    date DATE NOT NULL,
    amount INTEGER NOT NULL,
    create_date DATETIME NOT NULL,
    last_edit_date DATETIME,
    source JSON,
    CONSTRAINT UNIQUE_TRANSACTION UNIQUE (title, date)
)