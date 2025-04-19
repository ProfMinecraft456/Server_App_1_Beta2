import os
import json
import time
import shutil
import sys
from rich.progress import Progress
import pygame
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QProgressBar, QLabel
)
from PySide6.QtCore import QTimer, Qt  # Importar Qt
from PySide6.QtGui import QIcon

def reset():
    # Ruta al archivo de configuración local (en la carpeta settings del proyecto)
    SETTINGS_DIR = "settings"  # Carpeta settings dentro del proyecto
    LOCAL_CONFIG_PATH = os.path.join(SETTINGS_DIR, "serverappsetting.json")

    class ResetConfigApp(QWidget):
        def __init__(self):
            super().__init__()
            self.init_ui()

        def init_ui(self):
            """Inicializar la interfaz gráfica."""
            self.setWindowTitle("Restablecimiento de configuraciones de Server App for Windows")  # Título actualizado
            self.setGeometry(100, 100, 500, 300)  # Tamaño de la ventana
            self.setWindowIcon(QIcon("icons/applogo.png"))  # Ícono de la aplicación

            # Aplicar estilos CSS integrados
            self.setStyleSheet("""
                /* Estilo para la ventana principal */
                QWidget {
                    background-color: #DFF2EB;
                    font-family: "Arial";
                    font-size: 14px;
                    color: #4A628A; /* Color de fuente único */
                }

                /* Estilo para el botón de restablecimiento */
                #reset_button {
                    background-color: #7AB2D3;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-size: 16px;
                }

                #reset_button:hover {
                    background-color: #4A628A;
                }

                /* Estilo para la barra de progreso */
                #progress_bar {
                    background-color: #B9E5E8;
                    color: white;
                    border: 1px solid #4A628A;
                    border-radius: 5px;
                    text-align: center;
                }

                #progress_bar::chunk {
                    background-color: #4A628A;
                    border-radius: 5px;
                }

                /* Estilo para el título */
                #title_label {
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }

                /* Estilo para el mensaje de estado */
                #status_label {
                    font-size: 14px;
                    margin-top: 10px;
                }
            """)

            # Layout principal
            layout = QVBoxLayout()

            # Título de la ventana
            title_label = QLabel("Restablecer Configuraciones a Fábrica de Server App For Windows")
            title_label.setObjectName("title_label")
            title_label.setAlignment(Qt.AlignCenter)  # Centrar el texto
            layout.addWidget(title_label)

            # Botón para restablecer configuraciones
            self.reset_button = QPushButton(QIcon("icons/restart.png"), "Restablecer Ahora")
            self.reset_button.setObjectName("reset_button")
            self.reset_button.clicked.connect(self.confirm_reset)
            layout.addWidget(self.reset_button)

            # Barra de progreso
            self.progress_bar = QProgressBar()
            self.progress_bar.setObjectName("progress_bar")
            self.progress_bar.setVisible(False)  # Ocultar inicialmente
            layout.addWidget(self.progress_bar)

            # Etiqueta para mostrar el estado actual
            self.status_label = QLabel("")
            self.status_label.setObjectName("status_label")
            self.status_label.setAlignment(Qt.AlignCenter)  # Centrar el texto
            layout.addWidget(self.status_label)

            # Configurar el layout
            self.setLayout(layout)

        def confirm_reset(self):
            """Mostrar un cuadro de diálogo de advertencia para confirmar el restablecimiento."""
            # Crear un cuadro de diálogo de advertencia
            warning_box = QMessageBox(self)
            warning_box.setWindowTitle("Advertencia")
            warning_box.setIcon(QMessageBox.Warning)
            warning_box.setText("¿Estás seguro de restablecer todas las configuraciones a fábrica?")
            warning_box.setInformativeText("Esta acción no se puede deshacer.")
            warning_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            warning_box.setDefaultButton(QMessageBox.No)

            # Cambiar el estilo del cuadro de diálogo
            warning_box.setStyleSheet("""
                QMessageBox {
                    background-color: #DFF2EB;
                    font-family: "Arial";
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: #4A628A;
                }
                QMessageBox QPushButton {
                    background-color: #7AB2D3;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4A628A;
                }
            """)

            # Mostrar el cuadro de diálogo y verificar la respuesta
            response = warning_box.exec()
            if response == QMessageBox.Yes:
                self.start_reset_process()

        def start_reset_process(self):
            """Iniciar el proceso de restablecimiento."""
            # Ocultar el botón y mostrar la barra de progreso
            self.reset_button.setVisible(False)
            self.progress_bar.setVisible(True)

            # Iniciar el temporizador para simular el proceso
            self.progress_bar.setValue(0)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_progress)
            self.timer.start(500)  # Actualizar cada 500 ms

        def update_progress(self):
            """Actualizar la barra de progreso y mostrar el estado actual."""
            current_value = self.progress_bar.value()

            if current_value == 0:
                self.status_label.setText("Cargando configuraciones...")
                self.progress_bar.setValue(20)
            elif current_value == 20:
                self.status_label.setText("Eliminando carpeta 'settings'...")
                self.delete_settings_folder()
                self.progress_bar.setValue(40)
            elif current_value == 40:
                self.status_label.setText("Restableciendo archivo de configuración...")
                self.reset_config_file()
                self.progress_bar.setValue(60)
            elif current_value == 60:
                self.status_label.setText("Verificando integridad del sistema...")
                self.fake_system_check()  # Función de mentiritas
                self.progress_bar.setValue(80)
            elif current_value == 80:
                self.status_label.setText("Limpiando caché...")
                self.fake_clear_cache()  # Función de mentiritas
                self.progress_bar.setValue(100)
            elif current_value == 100:
                # Detener el temporizador y mostrar mensaje de finalización
                self.timer.stop()
                self.status_label.setText("Configuraciones restablecidas correctamente.")
                QMessageBox.information(self, "Completado", "Configuraciones restablecidas correctamente.")
                self.reset_button.setVisible(True)
                self.progress_bar.setVisible(False)

        def delete_settings_folder(self):
            """Eliminar la carpeta 'settings' dentro del directorio seleccionado."""
            local_config = self.load_local_config()
            if not local_config:
                return

            appdir = local_config.get("appdir")
            if not appdir:
                QMessageBox.warning(self, "Error", "No se encontró 'appdir' en la configuración local.")
                return

            server_settings_dir = os.path.join(appdir, "settings")
            if os.path.exists(server_settings_dir):
                try:
                    shutil.rmtree(server_settings_dir)  # Borrar la carpeta y su contenido
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar la carpeta 'settings': {e}")
                    return

        def reset_config_file(self):
            """Sobrescribir el archivo JSON local con '{}'."""
            try:
                with open(LOCAL_CONFIG_PATH, "w") as file:
                    json.dump({}, file, indent=4)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo sobrescribir el archivo de configuración: {e}")

        def fake_system_check(self):
            """Función de mentiritas: Verificar integridad del sistema."""
            time.sleep(1)  # Simular un retraso

        def fake_clear_cache(self):
            """Función de mentiritas: Limpiar caché."""
            time.sleep(1)  # Simular un retraso

        def load_local_config(self):
            """Cargar la configuración local (appdir)."""
            if not os.path.exists(SETTINGS_DIR):
                QMessageBox.warning(self, "Error", "La carpeta 'settings' no existe. No hay configuraciones para restablecer.")
                return None

            if os.path.exists(LOCAL_CONFIG_PATH):
                try:
                    with open(LOCAL_CONFIG_PATH, "r") as file:
                        return json.load(file)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo cargar la configuración local: {e}")
                    return None
            else:
                QMessageBox.warning(self, "Error", f"El archivo '{LOCAL_CONFIG_PATH}' no existe. No hay configuraciones para restablecer.")
                return None

    if not __name__ == "__main__":
        # Mostrar barra de progreso antes de iniciar la aplicación
        with Progress() as progress:
            task = progress.add_task("[cyan]Iniciando aplicación...\r", total=100)
            while not progress.finished:
                for i in range(10):
                    time.sleep(0.01)  # Simular un retraso
                    progress.update(task, advance=1)

        app = QApplication(sys.argv)
        # Inicializar pygame para reproducir sonidos

        pygame.mixer.init()
        # Cargar y reproducir el sonido de inicio
        try:
            pygame.mixer.music.load("sounds/startup.wav")
            pygame.mixer.music.play()
        except Exception as e:
            print(f"No se pudo reproducir el sonido: {e}")

        window = ResetConfigApp()
        window.show()

        # Ejecutar la aplicación
        sys.exit(app.exec())