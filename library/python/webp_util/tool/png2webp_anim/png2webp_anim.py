import dataclasses
import operator
import sys

from functools import partial
from pathlib import Path
from typing import Any

from PIL import Image

from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QItemSelectionModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QHeaderView,
    QMenu,
)
from PySide2.QtGui import (
    QColor, QPixmap,
)

from webp_util.core import (
    config,
    pipe as p,
)
from webp_util.core.config import (
    DataList,
)
from webp_util.gui import (
    appearance,
    basic_table,
    log,
)
from webp_util.tool.png2webp_anim.png2webp_anim_ui import Ui_MainWindow

APP_NAME = 'PNGを合せてWebPアニメを作る'
__version__ = '0.2.0'


@dataclasses.dataclass
class ImageData(basic_table.RowData):
    path: str = ''
    duration: int = 100

    @classmethod
    def toHeaderList(cls) -> list[str]:
        return ['画像', '尺(ミリ秒)']


@dataclasses.dataclass
class ConfigData(config.Data):
    dst_path: str = ''
    is_loop: bool = True
    is_lossless: bool = True
    quality: int = 80


@dataclasses.dataclass
class AppData(config.Data):
    config: ConfigData = dataclasses.field(default_factory=ConfigData)
    images: DataList = dataclasses.field(default_factory=lambda: DataList(ImageData))


IMAGE_DIR = config.ROOT_PATH.joinpath('data', 'images')
ERROR_IMAGE_PATH = IMAGE_DIR.joinpath('error.png')
NOT_FOUND_IMAGE_PATH = IMAGE_DIR.joinpath('not_found.png')


def get_pixmap(path: Path) -> QPixmap:
    if not path.is_file():
        path = NOT_FOUND_IMAGE_PATH
    image = QPixmap(str(path))
    if image.isNull():
        image = QPixmap(str(ERROR_IMAGE_PATH))
    return image.scaled(80, 45, Qt.KeepAspectRatio, Qt.FastTransformation)


class Model(basic_table.Model):

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if index.isValid():
            if role == Qt.DisplayRole:
                if index.column() == 0:
                    return Path(dataclasses.astuple(self._data[index.row()])[index.column()]).name
                return dataclasses.astuple(self._data[index.row()])[index.column()]

            if role == Qt.EditRole:
                return dataclasses.astuple(self._data[index.row()])[index.column()]

            if role == Qt.DecorationRole:
                if index.column() == 0:
                    return p.pipe(
                        self._data[index.row()],
                        dataclasses.astuple,
                        operator.itemgetter(index.column()),
                        Path,
                        get_pixmap,
                    )

            if role == Qt.ToolTipRole:
                if index.column() == 0:
                    return dataclasses.astuple(self._data[index.row()])[index.column()]
                else:
                    return None

            if role == Qt.TextAlignmentRole:
                if index.column() == 1:
                    # 横と縦の同時指定に失敗したので、
                    # C++で書いてる人のマネてintでくくったら成功した.なぜ？？？
                    return int(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    return int(Qt.AlignLeft | Qt.AlignVCenter)

    def setData(self, index: QModelIndex, value, role: int = Qt.DisplayRole) -> bool:
        if index.column() == 1:
            try:
                v = int(value)
                if v < 1:
                    return False
            except ValueError:
                return False

        return super().setData(index, value, role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            if index.column() == 1:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        return Qt.NoItemFlags


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('%s  其ノ%s' % (APP_NAME, __version__))
        # self.setWindowFlags(
        #     Qt.Window
        #     | Qt.WindowCloseButtonHint
        #     | Qt.WindowStaysOnTopHint
        # )
        self.resize(600, 700)
        self.setAcceptDrops(True)

        # spliter
        self.ui.splitter.setStretchFactor(0, 3)
        self.ui.splitter.setStretchFactor(1, 1)

        # style sheet
        self.ui.webpButton.setStyleSheet(appearance.ex_stylesheet)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        self.template_dir = config.ROOT_PATH.joinpath('data', 'template', APP_NAME)

        # table
        v = self.ui.tableView
        v.setModel(Model(ImageData))

        hh = v.horizontalHeader()
        hh.setStretchLastSection(False)
        hh.setSectionResizeMode(0, QHeaderView.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        vh = v.verticalHeader()
        vh.setDefaultSectionSize(45)

        v.setContextMenuPolicy(Qt.CustomContextMenu)
        v.customContextMenuRequested.connect(self.contextMenu)

        # event

        self.ui.dstToolButton.clicked.connect(partial(self.toolButton_clicked, self.ui.dstLineEdit))

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.webpButton.clicked.connect(self.webp, Qt.QueuedConnection)

        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionCopy.triggered.connect(self.copy)
        self.ui.actionPaste.triggered.connect(self.paste)
        self.ui.actionDelete.triggered.connect(self.delete)
        self.ui.actionUp.triggered.connect(self.up)
        self.ui.actionDown.triggered.connect(self.down)

    def contextMenu(self, pos):
        v = self.ui.tableView
        menu = QMenu(v)
        menu.addAction(self.ui.actionCopy)
        menu.addAction(self.ui.actionPaste)
        menu.addAction(self.ui.actionDelete)
        menu.addSeparator()
        menu.addAction(self.ui.actionUp)
        menu.addAction(self.ui.actionDown)
        menu.exec_(v.mapToGlobal(pos))

    def copy(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        sel_list = sm.selectedIndexes()
        if len(sel_list) != 0:
            i: QModelIndex = sel_list[0]
            s = str(m.get_value(i.row(), i.column()))
            QApplication.clipboard().setText(s)

    def paste(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()

        s = QApplication.clipboard().text()
        for i in sm.selectedIndexes():
            if i.column() != 0:
                m.setData(i, s, Qt.EditRole)

    def delete(self):
        v = self.ui.tableView
        m = v.model()
        sm = v.selectionModel()
        for row in p.pipe(
                sm.selectedIndexes(),
                p.filter(lambda i: i.column() == 0),
                p.map(p.call.row()),
                list,
                sorted,
                reversed,
        ):
            m.removeRow(row, QModelIndex())
        sm.clearSelection()

    def up(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        data_list = []
        min_row = None
        for row in p.pipe(
                sm.selectedIndexes(),
                p.filter(lambda i: i.column() == 0),
                p.map(p.call.row()),
                list,
                sorted,
                reversed,
        ):
            if min_row is None:
                min_row = row
            min_row = min([row, min_row])
            data_list.append(m.get_row_data(row))
            m.removeRow(row, QModelIndex())
        sm.clearSelection()
        if min_row is not None:
            if min_row == 0:
                min_row = 1
            m.insert_rows_data(min_row - 1, list(reversed(data_list)))
            for i in range(len(data_list)):
                index = m.index(min_row - 1 + i, 0, QModelIndex())
                sm.select(index, QItemSelectionModel.Select)
                sm.setCurrentIndex(index, QItemSelectionModel.Select)

    def down(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        data_list = []
        max_row = None
        for row in p.pipe(
                sm.selectedIndexes(),
                p.filter(lambda i: i.column() == 0),
                p.map(p.call.row()),
                list,
                sorted,
                reversed,
        ):
            if max_row is None:
                max_row = row
            max_row = max([row, max_row])
            data_list.append(m.get_row_data(row))
            m.removeRow(row, QModelIndex())
        sm.clearSelection()
        if max_row is not None:
            m.insert_rows_data(max_row + 2 - len(data_list), list(reversed(data_list)))
            for i in range(len(data_list)):
                if max_row != m.rowCount() - 1:
                    index = m.index(max_row + 2 - len(data_list) + i, 0, QModelIndex())
                else:
                    index = m.index(max_row - i, 0, QModelIndex())
                sm.select(index, QItemSelectionModel.Select)
                sm.setCurrentIndex(index, QItemSelectionModel.Select)

    def set_config_data(self, c: ConfigData):
        self.ui.dstLineEdit.setText(c.dst_path)
        self.ui.loopCheckBox.setChecked(c.is_loop)
        self.ui.losslessheckBox.setChecked(c.is_lossless)
        self.ui.qualitySpinBox.setValue(c.quality)

    def set_data(self, a: AppData):
        self.set_config_data(a.config)
        self.ui.tableView.model().set_data(a.images)

    def get_config_data(self) -> ConfigData:
        c = ConfigData()
        c.dst_path = self.ui.dstLineEdit.text()
        c.is_loop = self.ui.loopCheckBox.isChecked()
        c.is_lossless = self.ui.losslessheckBox.isChecked()
        c.quality = self.ui.qualitySpinBox.value()
        return c

    def get_data(self) -> AppData:
        a = AppData()
        a.config = self.get_config_data()
        a.images.set_list(self.ui.tableView.model().to_list())
        return a

    def load_config(self) -> None:
        c = ConfigData()
        if self.config_file.is_file():
            c.load(self.config_file)
        self.set_config_data(c)

    def save_config(self) -> None:
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        c = self.get_config_data()
        c.save(self.config_file)

    def new(self):
        self.set_data(AppData())
        self.clearLog()
        self.add2log('New')

    def open(self) -> None:
        dir_path = Path(self.ui.dstLineEdit.text()).parent
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            str(dir_path),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            if file_path.is_file():
                a = self.get_data()
                a.load(file_path)
                self.set_data(a)
                self.clearLog()
                self.add2log('Open: %s' % str(file_path))

    def save(self) -> None:
        dir_path = Path(self.ui.dstLineEdit.text()).parent
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            str(dir_path),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            a = self.get_data()
            a.save(file_path)
            self.clearLog()
            self.add2log('Save: %s' % str(file_path))

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)

    def clearLog(self):
        self.ui.logTextEdit.clear()

    def toolButton_clicked(self, w) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Select',
            w.text(),
            'WebP(*.webp)',
        )
        if path != '':
            w.setText(path)

    def dragEnterEvent(self, e):
        mimeData = e.mimeData()

        # for mimetype in mimeData.formats():
        #     print('MIMEType:', mimetype)

        if mimeData.hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.clearLog()
        for path in p.pipe(
                e.mimeData().urls(),
                p.map(p.call.toLocalFile()),
                p.map(Path),
                p.filter(p.call.is_file()),
                p.filter(lambda f: f.name.endswith('.png')),
                p.map(str),
                p.map(p.call.replace('\\', '/')),
                list,
                sorted,
        ):
            m: Model = self.ui.tableView.model()
            d = ImageData(path=path)
            m.add_row_data(d)
            self.add2log('add: %s' % path)

    def webp(self) -> None:
        self.clearLog()

        data = self.get_data()

        # dst directory check
        dst_text = data.config.dst_path.strip()
        dst_file: Path = Path(dst_text)
        if dst_text != '':
            self.add2log('出力先: %s' % str(dst_file))
        else:
            self.add2log('[ERROR]出力先が設定されていません。', log.ERROR_COLOR)
            return

        self.add2log('')  # new line

        # 処理開始
        # self.add2log('処理中(前準備)')
        self.add2log('')  # new line

        data = self.get_data()
        if len(data.images) > 1:
            lst = p.pipe(
                data.images,
                p.map(p.get.path),
                p.map(Path),
                list
            )
            durations = p.pipe(
                data.images,
                p.map(p.get.duration),
                list
            )
            images = list(map(lambda file: Image.open(file), lst))

            # dir
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            # save
            images[0].save(
                str(dst_file),
                'webp',
                lossless=data.config.is_lossless,
                quality=data.config.quality,
                save_all=True,
                append_images=images[1:],
                duration=durations,
                loop=0 if data.config.is_loop else 1  # ループ回数を指定 0は無限
            )
        else:
            self.add2log('[ERROR]アニメーションには複数の画像が必要です。', log.ERROR_COLOR)
            return
        # end
        self.add2log('Done!')


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
