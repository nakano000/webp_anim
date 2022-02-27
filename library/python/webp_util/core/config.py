import json
import dataclasses
from pathlib import Path

ROOT_PATH: Path = Path(__file__).joinpath('..', '..', '..', '..', '..').resolve()
LAUNCHER_CONFIG_FILE: Path = ROOT_PATH.joinpath('data', 'app', 'launcher.json')
PYTHONW_EXE_PATH: Path = ROOT_PATH.joinpath(
    json.loads(LAUNCHER_CONFIG_FILE.read_text())['program']
)
CONFIG_DIR: Path = ROOT_PATH.joinpath('config')


class DataList(list):
    def __init__(self, cls):
        super().__init__()
        self._data_cls = cls

    def new_data(self):
        return self._data_cls()

    def set(self, lst: list):
        self.clear()
        for i in lst:
            data = self._data_cls()
            data.set(i)
            self.append(data)

    def set_list(self, lst: list):
        self.clear()
        for i in lst:
            self.append(i)

    def to_list(self) -> list:
        lst = []
        for i in self:
            lst.append(i)
        return lst

    def to_list_of_dict(self) -> list:
        lst = []
        for i in self:
            lst.append(dataclasses.asdict(i))
        return lst


@dataclasses.dataclass
class DataInterface:
    def set(self, dct):
        base = dataclasses.asdict(self)
        for k in base.keys():
            if k in dct:
                if isinstance(getattr(self, k), DataInterface):
                    getattr(self, k).set(dct[k])
                elif isinstance(getattr(self, k), DataList):
                    getattr(self, k).set(dct[k])
                else:
                    setattr(self, k, dct[k])

    def as_dict(self) -> dict:
        dct = dataclasses.asdict(self)
        for k in dct.keys():
            if isinstance(getattr(self, k), DataList):
                dct[k] = getattr(self, k).to_list_of_dict()
        return dct


@dataclasses.dataclass
class Data(DataInterface):
    def load(self, path: Path) -> None:
        dct = json.loads(path.read_text())
        self.set(dct)

    def save(self, path: Path) -> None:
        path.write_text(
            json.dumps(self.as_dict(), indent=2),
            encoding='utf-8',
        )


if __name__ == '__main__':
    print(ROOT_PATH)
    print(LAUNCHER_CONFIG_FILE)
    print(LAUNCHER_CONFIG_FILE.read_text())
    print(PYTHONW_EXE_PATH)
    print(CONFIG_DIR)


    @dataclasses.dataclass
    class D(DataInterface):
        a: int = 10


    dl = DataList(D)
    print(dl)
    dl.set(
        [
            {'a': 10},
            {'a': 20},
            {'a': 30},
        ]
    )
    print(dl)
