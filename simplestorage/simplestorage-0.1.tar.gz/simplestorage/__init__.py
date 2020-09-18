from .interface import StorageInterface

interface_session = StorageInterface()


def ls(uri: str):
    return interface_session.ls(uri=uri)


def save(data: bytes, uri: str):
    return interface_session.save(data=data, uri=uri)
