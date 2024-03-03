import os
import vdf
import json
from pathlib import Path


class VdfFile:
    def __init__(self, vdf_path: str, binary=False, create_if_not_exists=False):
        self.vdf_path = vdf_path
        self.binary = binary
        self.data = self.load_vdf(create_if_not_exists)

    def load_vdf(self, create_if_not_exists=False):
        if not os.path.exists(self.vdf_path):
            Path(self.vdf_path).touch()

        if self.binary:
            with open(self.vdf_path, 'rb') as f:
                return vdf.binary_loads(f.read(), mapper=vdf.VDFDict)
        else:
            with open(self.vdf_path, 'r') as f:
                return vdf.loads(f.read(), mapper=vdf.VDFDict)

    def save(self):
        if self.binary:
            with open(self.vdf_path, 'wb') as f:
                f.write(vdf.binary_dumps(self.data))
        else:
            with open(self.vdf_path, 'w+') as f:
                vdf.dump(self.data, f, pretty=True)

    def pretty_print(self):
        if self.data is not None:
            # we do not want to modify the original contents, so we reload the file again
            duplicate = self.load_vdf()
            if 'shortcuts' in self.data:
                for index in duplicate['shortcuts']:
                    entry = duplicate['shortcuts'][index]
                    if 'appid' in entry:
                        dup_appid = int(entry['appid'])
                        del entry['appid']
                        # convert to unsigned app id, what the user expects
                        entry['appid'] = dup_appid + 2**32
            print('original', self.data)
            # because VDFDict is a subclass of dict, we can use the json module to pretty print it
            return json.dumps(duplicate, indent=4, sort_keys=True)
        else:
            return 'No data available'
