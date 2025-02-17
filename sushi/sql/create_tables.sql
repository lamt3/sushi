CREATE TABLE organizations (
    organization_id SERIAL PRIMARY KEY,          
    name VARCHAR(100) NOT NULL,     
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,          
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,  
    member_type VARCHAR(50) NOT NULL,
    organization_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_organization
        FOREIGN KEY (organization_id)
        REFERENCES organizations(organization_id)
        ON DELETE CASCADE           
);