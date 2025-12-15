#!/bin/bash

# Define o local da venv
VENV_DIR="venv"

echo "======================================================="
echo " CONFIGURANDO AMBIENTE VIRTUAL (VENV)"
echo "======================================================="

# 1. Cria a Venv se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] Criando pasta '$VENV_DIR'..."
    python3 -m venv $VENV_DIR
else
    echo "[1/4] Pasta '$VENV_DIR' já existe."
fi

# 2. Ativa a Venv (apenas para o contexto deste script)
source $VENV_DIR/bin/activate
echo "[2/4] Ambiente ativado. Atualizando pip..."
pip install --upgrade pip

# 3. Garante que os arquivos requirements existam e tenham o básico
# (Como você acabou de reestruturar, eles podem estar vazios)

# --- Backend Requirements ---
if [ ! -s "backend/requirements.txt" ]; then
    echo "      -> Populando backend/requirements.txt com bibliotecas padrão..."
    echo "paho-mqtt" >> backend/requirements.txt
    echo "sqlalchemy" >> backend/requirements.txt
    echo "psycopg2-binary" >> backend/requirements.txt
    echo "python-dotenv" >> backend/requirements.txt
fi

# --- Firmware Tools Requirements (Ferramentas para o PC controlar o ESP) ---
if [ ! -s "firmware/requirements.txt" ]; then
    echo "      -> Populando firmware/requirements.txt com ferramentas ESP..."
    echo "esptool" >> firmware/requirements.txt
    echo "mpremote" >> firmware/requirements.txt
    echo "ampy" >> firmware/requirements.txt
fi

# 4. Instala todas as dependências
echo "[3/4] Instalando dependências do BACKEND..."
pip install -r backend/requirements.txt

echo "[4/4] Instalando ferramentas do FIRMWARE..."
pip install -r firmware/requirements.txt

echo "======================================================="
echo " SUCESSO! Ambiente configurado."
echo "======================================================="
echo " Para ativar a venv no seu terminal, rode:"
echo " source $VENV_DIR/bin/activate"
echo "======================================================="