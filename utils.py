from ftplib import FTP
import ftplib
import os
import datetime

class Utils:
	def now(self):
		return datetime.datetime.now()

	def basename(self, filename):
		return os.path.basename(filename)

	def computeSpeed(self, start, filename):
		end = self.now()
		size = self.__size__(filename) / 1000 / 1000
		return size / (end - start).total_seconds()

	def isDirectory(self, ftp, path):
		try:
			ftp.size(path)
			return False
		except ftplib.error_perm:
			return True

	def exists(self, targetFile):
		return os.path.exists(targetFile)

	def isSameSize(self, ftp, remoteFilename, localFilename):
		remoteSize = long(ftp.size(remoteFilename))
		localSize = self.__size__(localFilename)
		if remoteSize == localSize:
			return True
		else:
			return False

	def splitDirectoriesAndFiles(self, ftp, allFiles):
		directories = []
		files = []
		for i in allFiles:
			if self.isDirectory(ftp, i):
				directories.append(i)
			else:
				files.append(i)
		return (directories, files)

	def login(self, h, password):
		ftp = FTP(h, timeout=900)
		ftp.login('willsam100', password)
		return ftp

	def isMacOsApp(self, directory):
		n, ext = os.path.splitext(directory)
		if ext == '.app':
			return True
		else:
			return False

	def __size__(self, filename):
		return long(os.path.getsize(filename))

	def isHidden(self, filename):
		return (self.util.basename(filename)[0] == '.')

	def join(self, folder, filename):
		return os.path.join(folder, filename)

class Transfer:
	def __init__(self, source=None, target=None):
		self.source = source
		self.target = target