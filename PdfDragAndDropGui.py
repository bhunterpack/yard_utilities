import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget,
    QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyPDF2 import PdfMerger

class PDFDropList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith('.pdf'):
                    self.addItem(file_path)
            event.accept()
        else:
            event.ignore()

class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger - Drag and Drop")
        self.resize(500, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.drop_list = PDFDropList()
        self.layout.addWidget(self.drop_list)

        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.clicked.connect(self.merge_pdfs)
        self.layout.addWidget(self.merge_button)

        self.clear_button = QPushButton("Clear List")
        self.clear_button.clicked.connect(self.drop_list.clear)
        self.layout.addWidget(self.clear_button)

    def merge_pdfs(self):
         if self.drop_list.count() == 0:
             QMessageBox.warning(self, "No Files", "Please drag and drop some PDFs first")
             return

         files = [self.drop_list.item(i).text() for i in range(self.drop_list.count())]

         save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "merged.pdf", "PDF Files (*.pdf)")

         if save_path:
             merger = PdfMerger()
             try:
                 for file in files:
                     merger.append(file)
                 merger.write(save_path)
                 merger.close()
                 QMessageBox.information(self, "Success", f"Merged PDF saved to:\n{save_path}")
             except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to merge PDFs:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())