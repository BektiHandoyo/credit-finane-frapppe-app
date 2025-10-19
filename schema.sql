CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    role VARCHAR(50) CHECK (role IN ('customer', 'front_office', 'analyst', 'finance'))
);

CREATE TABLE credit_applications (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES users(id),
    amount_requested DECIMAL(12,2),
    status VARCHAR(50) DEFAULT 'pending',
    risk_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE risk_assessments (
    id SERIAL PRIMARY KEY,
    application_id INT REFERENCES credit_applications(id) ON DELETE CASCADE,
    analyst_id INT REFERENCES users(id),
    risk_score DECIMAL(5,2),
    result VARCHAR(50),
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disbursement_requests (
    id SERIAL PRIMARY KEY,
    application_id INT REFERENCES credit_applications(id) ON DELETE CASCADE,
    requested_by INT REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'requested',
    amount DECIMAL(12,2),
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    disbursement_id INT REFERENCES disbursement_requests(id),
    finance_officer_id INT REFERENCES users(id),
    customer_id INT REFERENCES users(id),
    amount DECIMAL(12,2),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE process_logs (
    id SERIAL PRIMARY KEY,
    application_id INT REFERENCES credit_applications(id),
    activity_name VARCHAR(255),
    performed_by INT REFERENCES users(id),
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
