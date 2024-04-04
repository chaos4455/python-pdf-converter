import sys
import os
import multiprocessing
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class PDFConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 400)
        self.setWindowTitle('PDF Converter')

        layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('Clique no botão "Carregar Arquivo" para selecionar um PDF')
        layout.addWidget(self.label)

        self.button = QPushButton("Carregar Arquivo")
        self.button.clicked.connect(self.load_file)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def load_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecionar Arquivo PDF", "", "Arquivos PDF (*.pdf)")

        if file_path:
            self.convert_pdf(file_path)

    def convert_pdf(self, file_path):
        output_dir = 'C:/pdfsconvertidos/'
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, os.path.basename(file_path))
        output_file = output_file.replace('.pdf', '_converted.pdf')

        # Verifica se o Ghostscript está instalado e acessível no sistema
        if not is_ghostscript_installed():
            self.label.setText('Ghostscript não encontrado. Certifique-se de que o Ghostscript está instalado.')
            return

        # Obtém o número de processadores lógicos disponíveis
        num_processors = multiprocessing.cpu_count()
        # Calcula o número de threads a serem utilizadas com base no limite de 90% de uso de CPU
        num_threads = int(num_processors * 0.9)

        # Comando Ghostscript para a conversão do PDF com melhor compactação e qualidade
        gs_command = [
            'gswin64c',  # Caminho para o executável do Ghostscript (versão 64 bits)
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/ebook',  # Melhor qualidade de saída
            '-dEmbedAllFonts=true',
            '-dSubsetFonts=true',
            '-dColorImageDownsampleType=/Bicubic',
            '-dColorImageResolution=150',
            '-dGrayImageDownsampleType=/Bicubic',
            '-dGrayImageResolution=150',
            '-dMonoImageDownsampleType=/Bicubic',
            '-dMonoImageResolution=150',
            '-dNumRenderingThreads=' + str(num_threads),
            '-dNumCopies=1',
            '-o',
            output_file,
            file_path
        ]

        # Executa o comando Ghostscript
        try:
            subprocess.run(gs_command, check=True)
            self.label.setText(f'Arquivo convertido salvo em:\n{output_file}')
        except subprocess.CalledProcessError as e:
            error_message = str(e)
            self.label.setText(f'Erro ao converter o arquivo PDF:\n{error_message}')

def is_ghostscript_installed():
    # Verifica se o Ghostscript está instalado e acessível no sistema
    try:
        subprocess.run(['gswin64c', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = PDFConverter()
    window.show()

    sys.exit(app.exec_())
