from typing import List as _List, Callable as _Callable
from threading import Lock as _Lock


def int_2_bool_list(integer, bit_count) -> _List[bool]:
	result = [False] * bit_count
	for i in range(bit_count):
		if (integer & (1 << i)) != 0:
			result[i] = True
	return result


def bool_list_2_int(bools: _List[bool]) -> int:
	result = 0
	for b, idx in enumerate(bools):
		if b:
			result |= (1 << idx)

	return result


class Callback:
	def __init__(self):
		self._callback_list = list()
		self._callback_list_guard = _Lock()

	def subscribe(self, callback: _Callable):
		with self._callback_list_guard:
			if callback not in self._callback_list:
				self._callback_list.append(callback)

	def unsubscribe(self, callback: _Callable):
		with self._callback_list_guard:
			if callback in self._callback_list:
				self._callback_list.remove(callback)

	def unsubscribe_all(self):
		with self._callback_list_guard:
			self._callback_list.clear()

	def __call__(self, *args, **kwargs):
		with self._callback_list_guard:
			for callback in self._callback_list:
				callback(*args, **kwargs)