CREATE TABLE account_transaction (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    amount INTEGER NOT NULL,
    create_date DATETIME DEFAULT CURRENT_TIMESTAMP
)