
class SalaryNotInRangeError(Exception):
	"""Исключение возникает из-за ошибок в зарплате.

	Атрибуты:
		salary: входная зарплата, вызвавшая ошибку
		message: объяснение ошибки
	"""
	
	def __init__(self, salary, message="Зарплата не входит в диапазон (5000, 15000)"):
		self.salary = salary
		self.message = message
		# переопределяется конструктор встроенного класса `Exception()`
		super().__init__(self.message)