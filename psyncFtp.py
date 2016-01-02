from ftplib import FTP
import ftplib
import hashlib

h = '192.168.1.76'
targetDir = '/volume1/video/Movies'
dest = '/video/movies'

def login(h, password):
	ftp = FTP(h, timeout=900)
	ftp.login('willsam100', password)
	return ftp

def copyMovies(movies):
	for movie in movies:
		speed = copyFile(ftp, targetDir, movie)
		print movie + ' copied at ' + str(speed)[:5] + ' MB/s'

def copyFile(ftp, targetDir, sourceFileName):
	destFileName = os.path.basename(sourceFileName)
	if isFolder(ftp, sourceFileName):
		print 'Skipping folder ' + destFileName
		return 0.0	
	start = now()
	with open(os.path.join(targetDir, destFileName), 'wb') as f:
		ftp.retrbinary('RETR %s' % sourceFileName, f.write)
	return computeSpeed(ftp, start, sourceFileName)

def getTargetMovies(ftp, dest):
	files = ftp.nlst(dest)
	movies = []
	for f in files:
		name, ext = os.path.splitext(f)
		if ext != '':
			movies.append(f)
	return movies

def now():
	return datetime.datetime.now()

def computeSpeed(ftp, start, filename):
	end = now()
	size = ftp.size(filename) / 1000 / 1000
	return size / (end - start).total_seconds()

def isFolder(ftp, path):
	try:
		ftp.size(path)
		return False
	except ftplib.error_perm:
		return True
