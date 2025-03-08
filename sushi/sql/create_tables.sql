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

CREATE TABLE ad_platforms (
    id SERIAL PRIMARY KEY,
    organization_id INT REFERENCES organizations(id) ON DELETE CASCADE,
    ad_platform_name VARCHAR(255) NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    access_token_expiry TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE ad_platforms
ADD CONSTRAINT unique_organization_ad_platform
UNIQUE (organization_id, ad_platform_name);

CREATE INDEX idx_ad_platforms_organization_id 
ON ad_platforms (organization_id);


CREATE TABLE ad_accounts (
    account_id VARCHAR(100) PRIMARY KEY,  -- Set account_id as the primary key
    platform VARCHAR(50) NOT NULL,        -- Facebook, Google, LinkedIn, etc.
    name VARCHAR(255) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    timezone VARCHAR(50),
    spend_cap NUMERIC(12,2),              -- PostgreSQL uses NUMERIC instead of DECIMAL
    created_at TIMESTAMP DEFAULT NOW(),
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,  -- foreign key
    CONSTRAINT unique_account_per_org UNIQUE (account_id, organization_id) 
);

-- Add an index on organization_id for faster lookups
CREATE INDEX idx_organization_id ON ad_accounts (organization_id);


CREATE TABLE shopify_connections (
    id SERIAL PRIMARY KEY,
    shopify_store TEXT NOT NULL UNIQUE,
    access_token TEXT NOT NULL,
    organization_id INT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_organization FOREIGN KEY (organization_id) 
    REFERENCES organizations(organization_id) ON DELETE SET NULL
);