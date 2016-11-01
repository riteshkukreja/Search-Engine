import json
from datetime import datetime
import threading

class logger:
	logs = {'count': 0, 'logs': []}
	lock = threading.Lock()
	maxLogs = 10

	def warn(self, str):
		logger.lock.acquire()
		if len(logger.logs['logs']) >= logger.maxLogs:
			logger.logs['logs'].pop(0)

		obj = {'time': datetime.now().strftime("%I:%M%p on %B %d, %Y"), 'message': str, 'type': 'warning', 'code': 100}
		logger.logs['logs'].append(obj)
		logger.logs['count'] += 1

		print obj
		logger.lock.release()

	def error(self, str):
		logger.lock.acquire()
		if len(logger.logs['logs']) >= logger.maxLogs:
			logger.logs['logs'].pop(0)

		obj = {'time': datetime.now().strftime("%I:%M%p on %B %d, %Y"), 'message': str, 'type': 'error', 'code': 200}
		logger.logs['logs'].append(obj)
		logger.logs['count'] += 1

		print obj
		logger.lock.release()

	def alert(self, str):
		logger.lock.acquire()
		if len(logger.logs['logs']) >= logger.maxLogs:
			logger.logs['logs'].pop(0)

		obj = {'time': datetime.now().strftime("%I:%M%p on %B %d, %Y"), 'message': str, 'type': 'alert', 'code': 300}
		logger.logs['logs'].append(obj)
		logger.logs['count'] += 1

		print obj
		logger.lock.release()

	def log(self, str):
		logger.lock.acquire()
		if len(logger.logs['logs']) >= logger.maxLogs:
			logger.logs['logs'].pop(0)
			
		obj = {'time': datetime.now().strftime("%I:%M%p on %B %d, %Y"), 'message': str, 'type': 'log', 'code': 400}
		logger.logs['logs'].append(obj)
		logger.logs['count'] += 1
		
		print obj
		logger.lock.release()

	def getLogs(self):
		return logger.logs

	def clear(self):
		logger.lock.acquire()
		logger.logs = {'count': 0, 'logs': []}
		logger.lock.release()