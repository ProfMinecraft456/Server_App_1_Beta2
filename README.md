# **Server App For Windows - Beta 2**
"Server App For Windows" es una aplicación en **Python** para administrar servidores de **Minecraft Bedrock**, optimizada para **dispositivos Windows modestos**. En esta **Beta 2**, se han implementado mejoras clave que optimizan aún más la experiencia del usuario.

## **Requisitos del sistema**
- **CPU:** Intel Core i3-2120 / AMD Ryzen 3 3200  
- **RAM:** 2GB o superior  
- **Almacenamiento:** 1GB - 2GB (SSD recomendado)  
- **OS:** Windows 10 1703 / Windows Server 2016  
- **Red:** Conectividad de **10Mbps** para estabilidad  
- **No requiere privilegios administrativos**  

## **Uso de la aplicación**
La aplicación presenta una interfaz sencilla con botones en el explorador para realizar las siguientes acciones:
- **Iniciar**: Ejecuta el servidor `bedrock_server.exe`.  
- **Detener**: Finaliza el servidor en ejecución.  
- **Reiniciar**: Detiene y vuelve a iniciar el servidor.  
- Visualizar detalles como: IP local, configuración del puerto en el archivo `server.properties`, y rendimiento del servidor.  

## **Funcionamiento de comandos**
La ejecución de la aplicación puede realizarse de dos maneras:  
1. **Doble clic sobre el archivo `Launcher.exe` para iniciar normalmente**.  
2. A través de comandos en la terminal:  
   - `Launcher.exe --reset`: Restablece la aplicación a su versión de fábrica.  
   - `Launcher.exe --version`: Muestra la versión del programa.  

⚠️ **Nota importante:**  
Los módulos en el archivo principal `Launcher.py` **no deben ser modificados** excepto para agregar nuevas funcionalidades o mejorar el código. Estos módulos son esenciales para el funcionamiento de una librería local personalizada llamada **Node**, la cual está diseñada para reducir significativamente el peso de la aplicación. **Node** depende de los módulos integrados y no está disponible en `pip` ni integrada en Python.

## **Ubicación de archivos**
- **Códigos fuente:** Todos los archivos de código están en la carpeta `code`.  
- **Dependencias multimedia:** También se encuentran en la misma carpeta `code`.  

## **Novedades de Beta 2**
- **Mejoras en la precisión:** Ahora los indicadores de rendimiento para CPU, RAM y red son más confiables y precisos.  
- **Reducción significativa del tamaño de archivo:** Gracias a la optimización con la librería personalizada **Node**, el tamaño total de la aplicación se ha reducido en un **35-40%** respecto a la versión Beta 1, lo que la hace más ligera y rápida.  
- **Tiempos de carga optimizados:** Se han reducido los tiempos de carga tanto en la **verificación de archivos** como en el uso de `rich.progress`, mejorando la experiencia general del usuario.  
- **No se implementaron transiciones:** Aunque se habían considerado, las transiciones permanecen desactivadas en la Beta 2 para evitar posibles problemas de inestabilidad. Hasta la fecha, no se han recibido reportes sobre este aspecto y se decidió mantener la configuración actual para garantizar la estabilidad del programa.

## **Contribución**
Puedes contribuir al desarrollo del proyecto enviando sugerencias o mejoras de código a:  
📧 **profmcyt@hotmail.com**

## **Librerías utilizadas**
El proyecto usa las siguientes librerías:  
- `PySide6`  
- `pygame`  
- `rich`  
- `psutil`  
- **Node** (librería local personalizada, no disponible en `pip` ni integrada en Python).

```bash
pip install PySide6 pygame rich psutil