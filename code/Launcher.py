import sys 
import os
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
from rich.progress import Progress
from rich.console import Console
import argparse
import Node as Node
from Node import reset
# Estos módulos no se deben modificar a menos de que quieras mejorar el codigo de la libreria

def no_args():
    # 1- Verificar Archivos
    Node.check()

    # 2- Avisar Sobre beta 2
    Node.Warning()

    # 3- Iniciar App
    Node.run()
    
def main():
        console = Console()
        print = console.print
        parser = argparse.ArgumentParser(
            description="Script que maneja argumentos de línea de comandos: --reset y --version."
        )
        parser.add_argument(
            "--reset", 
            action="store_true", 
            help="Restablece Server App de Fábrica"
        )
        parser.add_argument(
            "--version", 
            action="store_true", 
            help="Imprime la versión del programa.\n"
        )
        
        args = parser.parse_args()
    
        if args.reset:
            reset.reset()
    
        if args.version:
            print("\n[underline red]Versión del programa:[/underline red]\n[green]Server App For Windows v1.0 - Beta 1[/green]\n")
    
        # Si no se proporcionan argumentos, mostrar la ayuda
        if not (args.reset or args.version):
            parser.print_help()
            no_args()
if __name__ == "__main__":
    main()