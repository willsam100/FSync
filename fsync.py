from utils import Utils
import os
import datetime
import sys

class Transfer():
	def __init__(self, ftp, util, target, depth=''):
		self.ftp = ftp
		self.util = util
		self.target = target
		self.depth = ''

	def sync(self, inputFiles):
		sourceDirectories, sourceFiles = self.util.splitDirectoriesAndFiles(self.ftp, inputFiles)
		print self.depth + 'Found ' + str(len(sourceFiles)) + ' file(s) to copy'
		self.__copyFiles__(sourceFiles)

		for directory in sourceDirectories:
			print self.depth + 'copying directory ' + directory
			name = self.util.basename(directory)
			if not self.util.isMacOsApp(directory):
				transfer = Transfer(self.ftp, self.util, os.path.join(self.target, name), self.depth + '-')
				if not self.util.exists(transfer.target):
					os.makedirs(transfer.target)
				transfer.sync(transfer.getFiles(directory))

	def getFiles(self, source):
		allFiles = self.ftp.nlst(source)
		files = []
		for filename in allFiles:
			if not self.util.isHidden(filename):
				files.append(filename)
		return files

	def __copyFiles__(self, files):
		for filename in files:
			if self.util.exists(self.__targetFile__(filename)) and self.util.isSameSize(self.ftp, filename, self.__targetFile__(filename)):
				print self.depth + 'Skipping existing file: ' + self.util.basename(filename)
			else:
				speed = self.__copyFile__(filename, self.__targetFile__(filename))
				print self.depth + self.util.basename(filename) + ' copied at ' + str(speed)[:5] + ' MB/s'

	def __copyFile__(self, filename, targetFile):
		start = self.util.now()
		with open(targetFile, 'wb') as openFileHandle:
			self.ftp.retrbinary('RETR %s' % filename, openFileHandle.write)
		return self.util.computeSpeed(start, targetFile)

	def __targetFile__(self, filename):
		return self.util.join(self.target, self.util.basename(filename))

if __name__ == '__main__':

	args = sys.argv[1:]
	if len(args) != 3:
		print 'Must supply source, target, password'
		sys.exit(0)

	host = '192.168.1.175'
	util = Utils()
	password = args[2]
	ftp = util.login(host, password)
	transfer = Transfer(ftp, uitl, args[1])
	psync.sync(transfer.getFiles(args[0]))

	


