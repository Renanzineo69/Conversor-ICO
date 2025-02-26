import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit,
    QProgressBar, QMessageBox, QApplication, QHBoxLayout, QDesktopWidget
)
from PyQt5.QtCore import Qt
from logic.converter import ImageConverter

class ImageConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.converter = ImageConverter(self)

    def initUI(self):
        self.setWindowTitle("Conversor de Imagem para ICO")
        self.setGeometry(300, 300, 500, 300)
        self.center_window()  # Centraliza a aplicação ao iniciar

        self.setStyleSheet("""
            QWidget {
                background-color: #2C2F33;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                background-color: #23272A;
                border: 1px solid #7289DA;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #7289DA;
                color: white;
                padding: 6px;
                border-radius: 5px;
                font-weight: bold;
                max-width: 180px;
            }
            QPushButton:hover {
                background-color: #5865F2;
            }
            QProgressBar {
                background-color: #23272A;
                border: 1px solid #7289DA;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #43B581;
                width: 10px;
            }
            QMessageBox {
                background-color: #2C2F33;
                color: white;
                font-family: Arial, sans-serif;
                border: 1px solid #7289DA;
                border-radius: 8px;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #7289DA;
                color: white;
                border-radius: 5px;
                padding: 6px;
            }
            QMessageBox QPushButton:hover {
                background-color: #5865F2;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.source_label = QLabel("Imagem de Entrada:")
        self.source_input = QLineEdit()
        self.source_input.setReadOnly(True)

        # Layout para centralizar o botão de seleção da imagem
        source_button_layout = QHBoxLayout()
        self.source_button = QPushButton("Selecionar Imagem")
        source_button_layout.addStretch()
        source_button_layout.addWidget(self.source_button)
        source_button_layout.addStretch()
        self.source_button.clicked.connect(self.select_image)

        self.destination_label = QLabel("Pasta de Destino:")
        self.destination_input = QLineEdit()
        self.destination_input.setReadOnly(True)

        # Layout para centralizar o botão de seleção da pasta de destino
        destination_button_layout = QHBoxLayout()
        self.destination_button = QPushButton("Selecionar Pasta de Destino")
        destination_button_layout.addStretch()
        destination_button_layout.addWidget(self.destination_button)
        destination_button_layout.addStretch()
        self.destination_button.clicked.connect(self.select_destination_folder)

        # Layout para centralizar o botão de conversão
        convert_button_layout = QHBoxLayout()
        self.convert_button = QPushButton("Converter")
        convert_button_layout.addStretch()
        convert_button_layout.addWidget(self.convert_button)
        convert_button_layout.addStretch()
        self.convert_button.clicked.connect(self.convert_image)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.source_label)
        layout.addWidget(self.source_input)
        layout.addLayout(source_button_layout)
        layout.addWidget(self.destination_label)
        layout.addWidget(self.destination_input)
        layout.addLayout(destination_button_layout)
        layout.addLayout(convert_button_layout)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.load_destination_folder()

    def center_window(self):
        """ Centraliza a janela na tela ao iniciar """
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.webp *.svg *.raw *.tiff *.pdf *.gif *.psd *.bmp)")
        if file_path:
            self.source_input.setText(file_path)

    def select_destination_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Destino")
        if folder_path:
            self.destination_input.setText(folder_path)
            self.save_destination_folder(folder_path)

    def convert_image(self):
        source_path = self.source_input.text()
        destination_path = self.destination_input.text()
        self.progress_bar.setValue(10)
        self.converter.convert_image(source_path, destination_path)

    def update_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.show_message("Conversão Concluída", message)

    def show_message(self, title, message):
        """ Exibe um pop-up estilizado """
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2C2F33;
                color: white;
                border: 1px solid #7289DA;
                border-radius: 8px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #7289DA;
                color: white;
                border-radius: 5px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #5865F2;
            }
        """)
        msg.exec_()

    def show_error(self, title, message):
        """ Exibe um pop-up de erro estilizado """
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2C2F33;
                color: white;
                border: 1px solid #7289DA;
                border-radius: 8px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #7289DA;
                color: white;
                border-radius: 5px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #5865F2;
            }
        """)
        msg.exec_()

    def load_destination_folder(self):
        """ Carrega a última pasta de destino salva. """
        try:
            with open("destination_folder.txt", "r") as file:
                self.destination_input.setText(file.read().strip())
        except FileNotFoundError:
            pass

    def save_destination_folder(self, folder_path):
        """ Salva a pasta de destino para usos futuros. """
        with open("destination_folder.txt", "w") as file:
            file.write(folder_path)
