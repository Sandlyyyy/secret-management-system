#!/bin/bash

echo "🚀 Setting up Secret Management System Demo on Ubuntu 22.04"

# Создаем директории
mkdir -p {backend,frontend/src,frontend/public,docker-compose/nginx,docker-compose/postgres}

# Создаем .env файл
cat > docker-compose/.env << EOF
POSTGRES_ROOT_PASSWORD=postgres_root_pass_123
KEYCLOAK_DB_PASSWORD=keycloak_db_pass_123
BACKEND_DB_PASSWORD=backend_db_pass_123
KEYCLOAK_ADMIN_PASSWORD=keycloak_admin_pass_123
KEYCLOAK_BACKEND_SECRET=backend_secret_123
OPENBAO_ROOT_TOKEN=openbao_root_token_123
JWT_SECRET=jwt_secret_key_123456789
EOF

# Создаем скрипт инициализации БД
cat > docker-compose/postgres/init-multiple-databases.sh << 'EOF'
#!/bin/bash
set -e
set -u

function create_database() {
    local database=$1
    local user=$2
    local password=$3
    echo "Creating database '$database' with user '$user'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE USER $user WITH PASSWORD '$password';
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $user;
EOSQL
}

create_database keycloak_db keycloak_user $KEYCLOAK_DB_PASSWORD
create_database secret_management backend_user $BACKEND_DB_PASSWORD
EOF

chmod +x docker-compose/postgres/init-multiple-databases.sh

echo "✅ Setup complete! Run 'docker-compose up --build' to start the system."