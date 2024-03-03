import os
import vdf
from pathlib import Path


class VdfFile:
    def __init__(self, vdf_path: str, binary=False, create_if_not_exists=False):
        self.vdf_path = vdf_path
        self.data = None
        self.binary = binary
        self.load_vdf(create_if_not_exists)

    def load_vdf(self, create_if_not_exists=False):
        if not os.path.exists(self.vdf_path):
            Path(self.vdf_path).touch()

        if self.binary:
            with open(self.vdf_path, 'rb') as f:
                data = vdf.binary_loads(f.read(), mapper=vdf.VDFDict)
                self.data = data
        else:
            with open(self.vdf_path, 'r') as f:
                self.data = vdf.loads(f.read(), mapper=vdf.VDFDict)

    def save(self):
        if self.binary:
            with open(self.vdf_path, 'wb') as f:
                f.write(vdf.binary_dumps(self.data))
        else:
            with open(self.vdf_path, 'w+') as f:
                vdf.dump(self.data, f, pretty=True)
