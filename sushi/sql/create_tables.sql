CREATE TABLE organization (
    id SERIAL PRIMARY KEY,          -- Auto-incrementing primary key
    name VARCHAR(100) NOT NULL    -- Organization name
);

-- Create the member table
CREATE TABLE member (
    id SERIAL PRIMARY KEY,          -- Auto-incrementing primary key
    first_name VARCHAR(100) NOT NULL, -- Member's first name
    last_name VARCHAR(100) NOT NULL,  -- Member's last name
    email VARCHAR(120) UNIQUE NOT NULL, -- Member's email (must be unique)
    jwt_token VARCHAR(255),        -- JWT token for authentication
    access VARCHAR(50) NOT NULL,   -- Access level (e.g., 'admin' or 'normal')
    organization_id INT NOT NULL,  -- Foreign key to the organization table
    CONSTRAINT fk_organization
        FOREIGN KEY (organization_id)
        REFERENCES organization(id)
        ON DELETE CASCADE           -- If the organization is deleted, delete its members
);