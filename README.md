# 📜 Paystubs Automation API  

Automatización de la generación y gestión de **paystubs** (recibos de pago). Esta API permite la creación y envío automatizado de comprobantes de pago, optimizando procesos administrativos sin necesidad de una base de datos.  

## 🛠️ Tecnologías utilizadas  
- 🐍 **Python** + **Flask** (Backend)  
- 🐳 **Docker** (Contenedores)  

## ✅ Requisitos previos  
Asegúrate de tener instalado en tu sistema:  
- [ ] **Docker**   

## 🚀 Instalación  
Clona el repositorio y entra en la carpeta del proyecto:  

```bash
  git clone https://github.com/FoxtrotCN/paystubs-automation.git
  cd paystubs_automation
```

#### 1 - Renombra el archivo .env-test a .env:

```bash
  mv .env-test .env
```

## 🐳 Levantar la API con Docker
Para construir la imagen y ejecutar el contenedor con Docker:

#### 1 - Construye la imagen de Docker
```bash
  docker build -t paystubs-api .
```

#### 2 - Ejecuta el contenedor
```bash
    docker run -d -p 5000:5000 paystubs-api
```
Esto ejecutará el contenedor de la API

## 📡 Uso de la API
Ejemplo de solicitud para procesar un archivo CSV usando cURL:

```bash
    curl --data-binary @data.csv -X POST "http://127.0.0.1:5000/process?country=do&credentials=USER+PWD&company=atdev"
```

#### Nota:
Asegúrate de ejecutar este comando en la consola adecuada según tu sistema operativo:

##### - Mac OS/Linux: Usa la terminal y navega hasta el directorio donde se encuentra el archivo data.csv.

#### - Windows: Usa PowerShell o Git Bash, y navega hasta el directorio donde se encuentra el archivo data.csv.

Además, reemplaza USER+PWD en el parámetro credentials con los valores de las variables de entorno:

```bash
    API_USER='atdevadmin'
    API_PASSWORD='atdevadmin123'
```

Por ejemplo, el valor de credentials debería ser:

```bash
    credentials=atdevadmin+atdevadmin123
```

# Happy Coding! 🚀
© 2025 Fernando Cedeño. Todos los derechos reservados.


