import os
from PIL import Image

class ImageConverter:
    def __init__(self, ui):
        self.ui = ui

    def convert_image(self, source_path, destination_path):
        """ Converte uma imagem para ICO e salva na pasta de destino. """
        if not source_path or not destination_path:
            self.ui.show_error("Erro", "Por favor, selecione uma imagem e uma pasta de destino.")
            return

        try:
            image = Image.open(source_path)
            filename = os.path.splitext(os.path.basename(source_path))[0]
            output_path = os.path.join(destination_path, f"{filename}.ico")

            image.save(output_path, format="ICO", quality=100, optimize=True)
            self.ui.update_progress(100, "Conversão concluída!")
        except Exception as e:
            self.ui.show_error("Erro na Conversão", f"Ocorreu um erro durante a conversão: {e}")
