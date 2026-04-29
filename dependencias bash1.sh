# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
# - Crear archivo .env con tus credenciales de MySQL
# - Ejecutar schema.sql en MySQL

# 5. Ejecutar la aplicación
python main.py