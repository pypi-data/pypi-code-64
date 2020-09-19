class DiskError(RuntimeError):
	pass


class SaveError(DiskError):
	pass


class LoadError(DiskError):
	pass
