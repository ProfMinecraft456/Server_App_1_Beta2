import sys
import os
import shutil
import zipfile
import time
import subprocess
from rich.progress import Progress
import tarfile
import psutil
import socket
import json
from PySide6.QtWidgets import (
                                QApplication, QWidget, QVBoxLayout, QPushButton,
                                QLabel, QTextEdit, QHBoxLayout, QStackedWidget,
                                QTabWidget, QListWidget, QFileDialog, QMessageBox, 
                                QInputDialog, QListWidgetItem
                            )
from PySide6.QtGui import QColor, QPalette, QIcon, QPixmap
from PySide6.QtCore import Qt, QTimer
import pygame  # Importar pygame para reproducir sonidos
from rich.console import Console

def check():
    # Lista de archivos y directorios a verificar
    files_to_check = [
        "icons/app.png",
        "icons/applogo.png", "icons/back.png", "icons/cpu.png", "icons/delete.png",
        "icons/edition.png",  "icons/file.png", "icons/fileexplorer.png",  "icons/folder.png",
        "icons/home.png", "icons/ip.png",  "icons/jsonfile.png", "icons/letsgo.png",
        "icons/network.png", "icons/newfile.png", "icons/newfolder.png", "icons/next.png",
        "icons/performance.png", "icons/port.png", "icons/prop.png", "icons/ram.png",
        "icons/rename.png", "icons/restart.png", "icons/save.png", "icons/server.png", 
        "icons/start.png", "icons/stop.png", "icons/txtfile.png", "icons/version.png",
        "icons/zipfile.png", "settings/serverappsetting.json", "sounds/startup.wav", "styles/styles.css"
    ]

    # Función para verificar la existencia de los archivos
    def check_files(files):
        missing_files = []
        with Progress() as progress:
            task = progress.add_task("[cyan]Verificando archivos...\r", total=len(files))
            for file in files:
                time.sleep(0.025)  # Retardo de 1 segundo entre cada verificación
                if not os.path.exists(file):
                    missing_files.append(file)
                progress.update(task, advance=1)
        return missing_files

    # Función principal
    def main():
        console = Console()
        missing_files = check_files(files_to_check)

        if missing_files:
            console.print("[bold red]Faltan los siguientes componentes:[/bold red]")
            for file in missing_files:
                console.print(f"- {file}")
            console.print("[bold red]La aplicación no puede continuar. Saliendo...[/bold red]")
            sys.exit(0)
        else:
            console.print("[bold green]Todos los componentes están presentes.[/bold green]")

    if not __name__ == "__main__":
        main()

def Warning():
    global app
    class AlertWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setStyleSheet(self.get_material_you_style())  # Aplicar el estilo Material You
            self.show_alert()

        def show_alert(self):
            # Crear un cuadro de mensaje de advertencia
            alert_box = QMessageBox(self)
            alert_box.setIcon(QMessageBox.Warning)  # Icono de advertencia
            alert_box.setWindowTitle("Alerta")      # Título de la ventana

            # Establecer el ícono de la aplicación
            app_icon = QIcon("icons/applogo.png")  # Ruta al ícono
            alert_box.setWindowIcon(app_icon)       # Asignar el ícono a la ventana

            # Mensaje detallado
            alert_message = (
                "Alerta:\n\n"
                "Esta es la segunda beta de programa de administracion de servidor. Optimizada para cualquier uso\nEsta App se encuentra en pleno desarrollo. Se Han mejorado caracteristicas de su version anterior (1.0 - Beta 1).\n\nPor favor, reporta cualquier inconveniente.\n\n"
                "Nombre:\n"
                "Server App for Windows v1.0 - Beta 2"
            )
            alert_box.setText(alert_message)  # Mensaje completo

            # Botones personalizados
            yes_button = alert_box.addButton("Sí, deseo ejecutar", QMessageBox.YesRole)  # Botón "Sí"
            no_button = alert_box.addButton("No, prefiero salir", QMessageBox.NoRole)   # Botón "No"

            # Aplicar estilo a los botones
            yes_button.setStyleSheet("""
                QPushButton {
                    background-color: #7AB2D3;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #4A628A;
                }
            """)
            no_button.setStyleSheet("""
                QPushButton {
                    background-color: #B9E5E8;
                    color: #4A628A;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #DFF2EB;
                }
            """)

            # Mostrar el cuadro de mensaje
            alert_box.exec()

            # Verificar qué botón se presionó
            if alert_box.clickedButton() == no_button:
                print("Saliendo del programa...")
                sys.exit(0)  # Salir del programa

        def get_material_you_style(self):
            """Define el estilo Material You con la paleta de colores proporcionada"""
            return """
                QWidget {
                    background-color: #DFF2EB;
                    color: #4A628A;
                    font-family: Verdana, sans-serif;
                    font-size: 12px;
                }
                QMessageBox {
                    background-color: #DFF2EB;
                    border: 2px solid #B9E5E8;
                    border-radius: 10px;
                }
                QMessageBox QLabel {
                    color: #4A628A;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #7AB2D3;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #4A628A;
                }
            """
        
    app = QApplication(sys.argv)
    window = AlertWindow()

def run():
    global app
    # Ruta al archivo de configuración local (en la carpeta settings del proyecto)
    SETTINGS_DIR = "settings"  # Carpeta settings dentro del proyecto
    LOCAL_CONFIG_PATH = os.path.join(SETTINGS_DIR, "serverappsetting.json")

    def load_local_config():
        """Cargar la configuración local (appdir)."""
        if not os.path.exists(SETTINGS_DIR):
            os.makedirs(SETTINGS_DIR)  # Crear la carpeta settings si no existe

        if os.path.exists(LOCAL_CONFIG_PATH):
            try:
                with open(LOCAL_CONFIG_PATH, "r") as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error al cargar la configuración local: {e}")
        # Si no existe el archivo, devolver un diccionario con appdir en null
        return {"appdir": None}

    def save_local_config(config):
        """Guardar la configuración local (appdir)."""
        try:
            with open(LOCAL_CONFIG_PATH, "w") as file:
                json.dump(config, file, indent=4)
        except Exception as e:
            print(f"Error al guardar la configuración local: {e}")

    def load_server_config(appdir):
        """Cargar la configuración del servidor desde el directorio seleccionado."""
        server_settings_dir = os.path.join(appdir, "settings")  # Carpeta settings dentro del directorio seleccionado
        server_config_path = os.path.join(server_settings_dir, "serverconfig.json")

        if os.path.exists(server_config_path):
            try:
                with open(server_config_path, "r") as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error al cargar la configuración del servidor: {e}")
        # Si no existe el archivo, devolver valores por defecto
        return {
            "serverPath": appdir,
            "serverVersion": None,
            "serverIp": None,
            "serverPort": None,
            "serverEdition": "Bedrock",
            "serverExec": "bedrock_server.exe"
        }

    def save_server_config(appdir, config):
        """Guardar la configuración del servidor en el directorio seleccionado."""
        server_settings_dir = os.path.join(appdir, "settings")  # Carpeta settings dentro del directorio seleccionado
        if not os.path.exists(server_settings_dir):
            os.makedirs(server_settings_dir)  # Crear la carpeta settings si no existe

        server_config_path = os.path.join(server_settings_dir, "serverconfig.json")
        try:
            with open(server_config_path, "w") as file:
                json.dump(config, file, indent=4)
        except Exception as e:
            print(f"Error al guardar la configuración del servidor: {e}")

    class WelcomeScreen(QWidget):
        def __init__(self, stacked_widget):
            super().__init__()
            self.stacked_widget = stacked_widget
            self.init_ui()

        def init_ui(self):
            # Layout principal
            layout = QVBoxLayout()

            # Logo de la aplicación
            logo_label = QLabel(self)
            pixmap = QPixmap("icons/applogo.png")  # Cargar el logo
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

            # Mensaje de bienvenida
            welcome_label = QLabel("Bienvenido a Server App for Minecraft Bedrock")
            welcome_label.setObjectName("welcome_label")  # Nombre para el selector CSS
            welcome_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(welcome_label)

            # Botón para continuar
            self.vamos_button = QPushButton("Vamos")
            self.vamos_button.setObjectName("vamos_button")  # Nombre para el selector CSS
            self.vamos_button.clicked.connect(self.go_to_tab_screen)
            layout.addWidget(self.vamos_button)

            # Configurar la pantalla de bienvenida
            self.setLayout(layout)

        def go_to_tab_screen(self):
            """Cambiar a la pantalla de pestañas."""
            self.stacked_widget.setCurrentIndex(1)  # Cambiar al índice 1 (TabScreen)

    class TabScreen(QWidget):
        def __init__(self, default_directory):
            super().__init__()
            self.server_process = None  # Proceso del servidor
            self.history = [default_directory]  # Historial de rutas para navegación
            self.history_index = 0  # Índice actual en el historial
            self.default_directory = default_directory  # Directorio predeterminado

            # Cargar configuración del servidor
            self.settings = load_server_config(default_directory)
            self.init_ui()

        def init_ui(self):
            # Layout principal
            layout = QVBoxLayout()

            # Crear un QTabWidget con pestañas horizontales
            self.tab_widget = QTabWidget()
            self.tab_widget.setObjectName("tab_widget")  # Nombre para el selector CSS
            self.tab_widget.setTabPosition(QTabWidget.North)  # Pestañas en la parte superior

            # Asignar un nombre de objeto al QTabBar
            self.tab_widget.tabBar().setObjectName("tab_bar")  # Nombre para el selector CSS

            # Pestaña 1: Inicio
            self.home_tab = QWidget()
            home_layout = QVBoxLayout()

            # Botones de control del servidor
            control_layout = QHBoxLayout()

            self.start_button = QPushButton(QIcon("icons/start.png"), "Iniciar")
            self.start_button.setObjectName("start_button")
            self.start_button.clicked.connect(self.start_server)
            control_layout.addWidget(self.start_button)

            self.stop_button = QPushButton(QIcon("icons/stop.png"), "Detener")
            self.stop_button.setObjectName("stop_button")
            self.stop_button.clicked.connect(self.stop_server)
            self.stop_button.setEnabled(False)  # Deshabilitar inicialmente
            control_layout.addWidget(self.stop_button)

            self.restart_button = QPushButton(QIcon("icons/restart.png"), "Reiniciar")
            self.restart_button.setObjectName("restart_button")
            self.restart_button.clicked.connect(self.restart_server)
            self.restart_button.setEnabled(False)  # Deshabilitar inicialmente
            control_layout.addWidget(self.restart_button)

            home_layout.addLayout(control_layout)

            # Información del servidor
            info_layout = QVBoxLayout()
            
            self.title_label = QLabel("Informacion del servidor")
            self.title_label.setObjectName("title_label")
            info_layout.addWidget(self.title_label)

            self.ip_label = QLabel(f"IP del servidor: {self.settings['serverIp']}")
            self.ip_label.setObjectName("ip_label")
            info_layout.addWidget(self.ip_label)

            self.port_label = QLabel(f"Puerto: {self.settings['serverPort']}")
            self.port_label.setObjectName("port_label")
            info_layout.addWidget(self.port_label)

            self.edition_label = QLabel(f"Edición: {self.settings['serverEdition']}")
            self.edition_label.setObjectName("edition_label")
            info_layout.addWidget(self.edition_label)

            self.version_label = QLabel(f"Versión: {self.settings['serverVersion']}")
            self.version_label.setObjectName("version_label")
            info_layout.addWidget(self.version_label)

            self.path_label = QLabel(f"Ruta del servidor: {self.settings['serverPath']}")
            self.path_label.setObjectName("path_label")
            info_layout.addWidget(self.path_label)

            home_layout.addLayout(info_layout)

            # Rendimiento del servidor
            performance_layout = QVBoxLayout()
            
            self.title_label = QLabel("Rendimiento")
            self.title_label.setObjectName("title_label")
            performance_layout.addWidget(self.title_label)

            self.cpu_label = QLabel("Uso de CPU: 0%")
            self.cpu_label.setObjectName("cpu_label")
            performance_layout.addWidget(self.cpu_label)

            self.ram_label = QLabel("Uso de RAM: 0 MB")
            self.ram_label.setObjectName("ram_label")
            performance_layout.addWidget(self.ram_label)

            self.network_label = QLabel("Uso de red: 0 KB/s")
            self.network_label.setObjectName("network_label")
            performance_layout.addWidget(self.network_label)

            home_layout.addLayout(performance_layout)

            # Configurar la pestaña de inicio
            self.home_tab.setLayout(home_layout)
            self.tab_widget.addTab(self.home_tab, QIcon("icons/home.png"), "Inicio")

            # Pestaña 2: Archivos
            self.files_tab = QWidget()
            files_layout = QVBoxLayout()
            self.setup_files_tab(files_layout)
            self.files_tab.setLayout(files_layout)
            self.tab_widget.addTab(self.files_tab, QIcon("icons/fileexplorer.png"), "Archivos")

            # Añadir el QTabWidget al layout principal
            layout.addWidget(self.tab_widget)

            # Configurar la pantalla de pestañas
            self.setLayout(layout)

            # Temporizador para actualizar el rendimiento
            self.performance_timer = QTimer()
            self.performance_timer.timeout.connect(self.update_performance)
            self.performance_timer.start(1000)  # Actualizar cada segundo

            # Cargar información inicial
            self.load_server_info()

            # Listar archivos en el directorio predeterminado
            self.list_files(self.default_directory)

        def load_server_info(self):
            """Cargar la información del servidor."""
            # Obtener la IP local
            self.settings["serverIp"] = self.get_local_ip()
            self.ip_label.setText(f"IP del servidor: {self.settings['serverIp']}")

            # Obtener el puerto del archivo server.properties
            self.settings["serverPort"] = self.get_server_port()
            self.port_label.setText(f"Puerto: {self.settings['serverPort']}")

            # Obtener la ruta del servidor
            self.settings["serverPath"] = self.default_directory
            self.path_label.setText(f"Ruta del servidor: {self.settings['serverPath']}")

            # Obtener la versión del servidor
            self.get_server_version()

            # Guardar la configuración actualizada
            save_server_config(self.default_directory, self.settings)

        def get_local_ip(self):
            """Obtener la IP local."""
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)

        def get_server_port(self):
            """Obtener el puerto del archivo server.properties."""
            try:
                with open(os.path.join(self.default_directory, "server.properties"), "r") as file:
                    for line in file:
                        if line.startswith("server-port="):
                            return line.split("=")[1].strip()
            except Exception as e:
                print(f"Error al leer server.properties: {e}")
            return "N/A"

        def get_server_version(self):
            """Obtener la versión del servidor desde la salida de bedrock_server.exe."""
            try:
                # Ejecutar el servidor en modo de captura de salida
                process = subprocess.Popen(
                    [os.path.join(self.default_directory, "bedrock_server.exe")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=self.default_directory
                )

                # Leer la salida línea por línea
                for line in process.stdout:
                    if "Version:" in line:
                        version = line.split("Version:")[1].strip()
                        self.settings["serverVersion"] = version
                        self.version_label.setText(f"Versión: {version}")
                        process.terminate()  # Detener el proceso después de obtener la versión
                        break
            except Exception as e:
                print(f"Error al obtener la versión del servidor: {e}")
                self.settings["serverVersion"] = "N/A"
                self.version_label.setText("Versión: N/A")

            # Guardar la configuración actualizada
            save_server_config(self.default_directory, self.settings)

        def start_server(self):
            """Iniciar el servidor."""
            try:
                self.server_process = subprocess.Popen(
                    [os.path.join(self.default_directory, "bedrock_server.exe")],
                    cwd=self.default_directory
                )
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.restart_button.setEnabled(True)
            except Exception as e:
                print(f"Error al iniciar el servidor: {e}")

        def stop_server(self):
            """Detener el servidor."""
            if self.server_process:
                self.server_process.terminate()
                self.server_process = None
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.restart_button.setEnabled(False)

        def restart_server(self):
            """Reiniciar el servidor."""
            self.stop_server()
            self.start_server()

        def update_performance(self):
            """Actualizar el rendimiento del servidor."""
            if self.server_process:
                pid = self.server_process.pid
                process = psutil.Process(pid)

                # Uso de CPU
                cpu_percent = process.cpu_percent()
                self.cpu_label.setText(f"Uso de CPU: {cpu_percent}%")

                # Uso de RAM
                ram_usage = process.memory_info().rss / (1024 * 1024)  # Convertir a MB
                self.ram_label.setText(f"Uso de RAM: {ram_usage:.2f} MB")

                # Uso de red
                network_usage = process.io_counters().read_bytes + process.io_counters().write_bytes
                network_usage /= 1024  # Convertir a KB
                self.network_label.setText(f"Uso de red: {network_usage:.2f} KB/s")

        def setup_files_tab(self, layout):
            """Configurar la pestaña de archivos."""
            # Botones de navegación y acciones
            button_layout = QHBoxLayout()

            # Botón para retroceder
            self.back_button = QPushButton(QIcon("icons/back.png"), "")
            self.back_button.setObjectName("back_button")
            self.back_button.clicked.connect(self.navigate_back)
            button_layout.addWidget(self.back_button)

            # Botón para avanzar
            self.forward_button = QPushButton(QIcon("icons/next.png"), "")
            self.forward_button.setObjectName("forward_button")
            self.forward_button.clicked.connect(self.navigate_forward)
            button_layout.addWidget(self.forward_button)

            layout.addLayout(button_layout)

            # Lista de archivos y carpetas
            self.file_list = QListWidget()
            self.file_list.setObjectName("file_list")
            self.file_list.itemDoubleClicked.connect(self.open_item)
            layout.addWidget(self.file_list)

            # Botones de acciones
            action_layout = QHBoxLayout()

            # Botón para crear carpeta
            self.create_folder_button = QPushButton(QIcon("icons/newfolder.png"), "Crear Carpeta")
            self.create_folder_button.setObjectName("create_folder_button")
            self.create_folder_button.clicked.connect(self.create_folder)
            action_layout.addWidget(self.create_folder_button)

            # Botón para crear archivo
            self.create_file_button = QPushButton(QIcon("icons/file.png"), "Crear Archivo")
            self.create_file_button.setObjectName("create_file_button")
            self.create_file_button.clicked.connect(self.create_file)
            action_layout.addWidget(self.create_file_button)

            # Botón para cambiar nombre
            self.rename_button = QPushButton(QIcon("icons/rename.png"), "Cambiar Nombre")
            self.rename_button.setObjectName("rename_button")
            self.rename_button.clicked.connect(self.rename_item)
            action_layout.addWidget(self.rename_button)

            # Botón para eliminar
            self.delete_button = QPushButton(QIcon("icons/delete.png"), "Eliminar")
            self.delete_button.setObjectName("delete_button")
            self.delete_button.clicked.connect(self.delete_item)
            action_layout.addWidget(self.delete_button)

            # Botón para comprimir
            self.compress_button = QPushButton(QIcon("icons/zipfile.png"), "Comprimir")
            self.compress_button.setObjectName("compress_button")
            self.compress_button.clicked.connect(self.compress_item)
            action_layout.addWidget(self.compress_button)

            layout.addLayout(action_layout)

            # Ruta actual
            self.current_path_label = QLabel("Ruta actual: ")
            self.current_path_label.setObjectName("current_path_label")
            layout.addWidget(self.current_path_label)

            # Actualizar botones de navegación
            self.update_navigation_buttons()

        def list_files(self, path):
            """Listar archivos y carpetas en el directorio especificado."""
            self.file_list.clear()
            try:
                # Obtener la lista de archivos y carpetas
                items = os.listdir(path)
                # Separar carpetas y archivos
                folders = [item for item in items if os.path.isdir(os.path.join(path, item))]
                files = [item for item in items if os.path.isfile(os.path.join(path, item))]

                # Ordenar alfabéticamente
                folders.sort()
                files.sort()

                # Mostrar carpetas primero
                for folder in folders:
                    item_path = os.path.join(path, folder)
                    list_item = QListWidgetItem(folder)
                    list_item.setIcon(QIcon("icons/folder.png"))
                    self.file_list.addItem(list_item)

                # Mostrar archivos después
                for file in files:
                    item_path = os.path.join(path, file)
                    list_item = QListWidgetItem(file)

                    # Asignar íconos según la extensión del archivo
                    if file.endswith(".zip") or file.endswith(".tar.gz"):
                        list_item.setIcon(QIcon("icons/zipfile.png"))
                    elif file.endswith(".json"):
                        list_item.setIcon(QIcon("icons/jsonfile.png"))
                    elif file.endswith(".txt"):
                        list_item.setIcon(QIcon("icons/txtfile.png"))
                    elif file.endswith(".exe"):
                        list_item.setIcon(QIcon("icons/app.png"))
                    elif file.endswith(".properties"):
                        list_item.setIcon(QIcon("icons/prop.png"))
                    else:
                        list_item.setIcon(QIcon("icons/file.png"))  # Ícono por defecto

                    self.file_list.addItem(list_item)

                self.current_path = path
                self.current_path_label.setText(f"Ruta actual: {self.current_path}")
            except Exception as e:
                self.file_list.addItem(f"Error: {e}")

        def update_history(self, path):
            """Actualizar el historial de navegación."""
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(path)
            self.history_index += 1
            self.update_navigation_buttons()

        def navigate_back(self):
            """Navegar hacia atrás en el historial."""
            if self.history_index > 0:
                self.history_index -= 1
                self.list_files(self.history[self.history_index])
                self.update_navigation_buttons()

        def navigate_forward(self):
            """Navegar hacia adelante en el historial."""
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.list_files(self.history[self.history_index])
                self.update_navigation_buttons()

        def update_navigation_buttons(self):
            """Actualizar el estado de los botones de navegación."""
            self.back_button.setEnabled(self.history_index > 0)
            self.forward_button.setEnabled(self.history_index < len(self.history) - 1)

        def open_item(self, item):
            """Abrir un archivo o carpeta."""
            item_name = item.text()
            item_path = os.path.join(self.current_path, item_name)
            if os.path.isdir(item_path):
                self.update_history(item_path)
                self.list_files(item_path)
            else:
                self.open_file(item_path)

        def open_file(self, file_path):
            """Abrir un archivo según su formato."""
            try:
                if file_path.endswith(".txt") or file_path.endswith(".properties") or file_path.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        self.show_editor(file_path, content)
                elif file_path.endswith(".exe"):
                    os.startfile(file_path)  # Abrir archivo ejecutable
                elif file_path.endswith(".zip"):
                    self.extract_zip(file_path)
                elif file_path.endswith(".tar.gz"):
                    self.extract_tar_gz(file_path)
                else:
                    QMessageBox.information(self, "Abrir Archivo", f"No se puede abrir el archivo: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo: {e}")

        def show_editor(self, file_path, content):
            """Mostrar un editor de texto para archivos .txt, .json y .properties."""
            self.editor_window = QWidget()
            self.editor_window.setWindowTitle(f"Editor - {os.path.basename(file_path)}")
            self.editor_window.setGeometry(100, 100, 800, 600)
            self.editor_window.setWindowIcon(QIcon("icons/applogo.png"))  # Ícono de la aplicación

            # Layout principal del editor
            editor_layout = QVBoxLayout()

            # Área de texto para editar el contenido
            self.editor_text_edit = QTextEdit()
            self.editor_text_edit.setObjectName("editor_text_edit")
            self.editor_text_edit.setPlainText(content)
            editor_layout.addWidget(self.editor_text_edit)

            # Botón de guardado
            save_button = QPushButton(QIcon("icons/save.png"), "Guardar")
            save_button.setObjectName("save_button")
            save_button.clicked.connect(lambda: self.save_file(file_path))
            editor_layout.addWidget(save_button)

            # Configurar la ventana del editor
            self.editor_window.setLayout(editor_layout)
            self.editor_window.show()

        def save_file(self, file_path):
            """Guardar el contenido editado en el archivo."""
            try:
                content = self.editor_text_edit.toPlainText()
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                QMessageBox.information(self, "Guardar", "Archivo guardado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {e}")

        def create_folder(self):
            """Crear una nueva carpeta."""
            folder_name, ok = QInputDialog.getText(self, "Crear Carpeta", "Nombre de la carpeta:")
            if ok and folder_name:
                try:
                    os.mkdir(os.path.join(self.current_path, folder_name))
                    self.list_files(self.current_path)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo crear la carpeta: {e}")

        def create_file(self):
            """Crear un nuevo archivo."""
            file_name, ok = QInputDialog.getText(self, "Crear Archivo", "Nombre del archivo:")
            if ok and file_name:
                try:
                    with open(os.path.join(self.current_path, file_name), "w") as file:
                        file.write("")  # Crear archivo vacío
                    self.list_files(self.current_path)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo crear el archivo: {e}")

        def rename_item(self):
            """Cambiar el nombre de un archivo o carpeta."""
            selected_item = self.file_list.currentItem()
            if selected_item:
                old_name = selected_item.text()
                new_name, ok = QInputDialog.getText(self, "Cambiar Nombre", "Nuevo nombre:", text=old_name)
                if ok and new_name:
                    try:
                        os.rename(
                            os.path.join(self.current_path, old_name),
                            os.path.join(self.current_path, new_name)
                        )
                        self.list_files(self.current_path)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"No se pudo cambiar el nombre: {e}")

        def delete_item(self):
            """Eliminar un archivo o carpeta."""
            selected_item = self.file_list.currentItem()
            if selected_item:
                item_name = selected_item.text()
                confirm = QMessageBox.question(
                    self, "Eliminar", f"¿Estás seguro de eliminar '{item_name}'?", QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.Yes:
                    try:
                        item_path = os.path.join(self.current_path, item_name)
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)  # Eliminar carpeta
                        else:
                            os.remove(item_path)  # Eliminar archivo
                        self.list_files(self.current_path)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"No se pudo eliminar: {e}")

        def compress_item(self):
            """Comprimir un archivo o carpeta."""
            selected_item = self.file_list.currentItem()
            if selected_item:
                item_name = selected_item.text()
                item_path = os.path.join(self.current_path, item_name)
                try:
                    if os.path.isdir(item_path):
                        shutil.make_archive(item_path, "zip", item_path)
                    else:
                        with zipfile.ZipFile(f"{item_path}.zip", "w") as zipf:
                            zipf.write(item_path, os.path.basename(item_path))
                    self.list_files(self.current_path)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo comprimir: {e}")

        def extract_zip(self, file_path):
            """Extraer un archivo ZIP."""
            extract_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Extracción")
            if extract_path:
                try:
                    with zipfile.ZipFile(file_path, "r") as zip_ref:
                        zip_ref.extractall(extract_path)
                    QMessageBox.information(self, "Extraer ZIP", "Extracción completada.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo extraer el archivo ZIP: {e}")

        def extract_tar_gz(self, file_path):
            """Extraer un archivo TAR.GZ."""
            extract_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Extracción")
            if extract_path:
                try:
                    with tarfile.open(file_path, "r:gz") as tar_ref:
                        tar_ref.extractall(extract_path)
                    QMessageBox.information(self, "Extraer TAR.GZ", "Extracción completada.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo extraer el archivo TAR.GZ: {e}")

    class ServerApp(QWidget):
        def __init__(self, default_directory):
            super().__init__()

            # Definir la paleta de colores
            self.setup_palette()

            # Configurar el QStackedWidget para manejar múltiples pantallas
            self.stacked_widget = QStackedWidget()

            # Pantalla de bienvenida
            self.welcome_screen = WelcomeScreen(self.stacked_widget)
            self.stacked_widget.addWidget(self.welcome_screen)

            # Pantalla de pestañas
            self.tab_screen = TabScreen(default_directory)
            self.stacked_widget.addWidget(self.tab_screen)

            # Configurar el layout principal
            layout = QVBoxLayout()
            layout.addWidget(self.stacked_widget)
            self.setLayout(layout)

            # Configurar la ventana principal
            self.setWindowTitle("Server App for Minecraft Bedrock")
            self.setGeometry(100, 100, 800, 600)
            self.setWindowIcon(QIcon("icons/applogo.png"))

        def setup_palette(self):
            # Colores de la paleta
            color1 = QColor("#DFF2EB")  # Fondo
            color2 = QColor("#B9E5E8")  # Botones
            color3 = QColor("#7AB2D3")  # Resaltado
            color4 = QColor("#4A628A")  # Texto

            # Crear una paleta personalizada
            palette = QPalette()
            palette.setColor(QPalette.Window, color1)
            palette.setColor(QPalette.WindowText, color4)
            palette.setColor(QPalette.Button, color2)
            palette.setColor(QPalette.ButtonText, color4)
            palette.setColor(QPalette.Highlight, color3)
            palette.setColor(QPalette.HighlightedText, Qt.white)

            # Aplicar la paleta a la aplicación
            QApplication.setPalette(palette)

    if not __name__ == "__main__":
        # Mostrar barra de progreso antes de iniciar la aplicación
        with Progress() as progress:
            task = progress.add_task("[cyan]Iniciando aplicación...\r", total=100)
            while not progress.finished:
                for i in range(10):
                    time.sleep(0.00125)  # Simular un retraso
                    progress.update(task, advance=1)


        # Cargar la configuración local
        local_config = load_local_config()
        appdir = local_config.get("appdir")

        # Si no hay un directorio seleccionado, pedir al usuario que seleccione uno
        if not appdir:
            appdir = QFileDialog.getExistingDirectory(
                None, "Seleccionar Directorio del Servidor"
            )
            if not appdir:
                print("No se seleccionó ningún directorio. Saliendo...")
                sys.exit()

            # Guardar la ruta seleccionada en la configuración local
            local_config["appdir"] = appdir
            save_local_config(local_config)

    # Cargar la configuración del servidor desde el directorio seleccionado
    server_config = load_server_config(appdir)

    # Guardar la configuración del servidor (esto creará el archivo si no existe)
    save_server_config(appdir, server_config)

    

    # Cargar estilos desde el archivo CSS
    with open("styles/styles.css", "r") as f:
        app.setStyleSheet(f.read())

    # Inicializar pygame para reproducir sonidos
    pygame.mixer.init()
    # Cargar y reproducir el sonido de inicio
    try:
        pygame.mixer.music.load("sounds/startup.wav")
        pygame.mixer.music.play()
    except Exception as e:
        print(f"No se pudo reproducir el sonido: {e}")

    # Crear y mostrar la ventana principal
    window = ServerApp(appdir)
    window.show()

    # Ejecutar la aplicación
    sys.exit(app.exec())
# Codigo final