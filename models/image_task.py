import json


class ImageTask:
    def __init__(self, filename, filedata, description, time):
        self.filename = filename
        self.filedata = filedata
        self.description = description
        self.time = time

    def to_json(self) -> str:
        return json.dumps({
            'filename': self.filename,
            'filedata': self.filedata.hex(),
            'description': self.description,
            'time': self.time,
        })

    @classmethod
    def from_json(cls, j: str):
        if j:
            d = json.loads(j)
            return cls(d['filename'], bytes.fromhex(d['filedata']), d['description'], d['time'])
        return None


class HandleImageTask(ImageTask):
    pass


class SaveImageTask(ImageTask):
    pass
