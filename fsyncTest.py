import unittest
from ftplib import FTP
from utils import Utils
from mock import MagicMock
import mock
from fsync import Transfer
import datetime
import os

util = Utils()

class TestTransfer(unittest.TestCase):

	def test_getFiles_allItems(self):
		allMovies = ['/home/sam/movie/transformers.mp4', '/home/sam/movie/walking.mp4']
		ftpMock = FTP('')
		ftpMock.nlst = MagicMock(return_value=allMovies)
		util = Utils()
		util.isHidden = MagicMock(return_value=False)

		source = '/home/sam/movie'
		transfer = Transfer(ftpMock, util, None)
		result = transfer.getFiles(source)

		ftpMock.nlst.assert_called_with(source)
		self.assertTrue(allMovies[0] in  result)
		self.assertTrue(allMovies[1] in result)


	def test_getTargetMovies_filterHiddenItems(self):
		allMovies = ['/home/sam/movie/.AppleDouble']
		ftpMock = FTP('')
		ftpMock.nlst = MagicMock(return_value=allMovies)
		util = Utils()
		util.isHidden = MagicMock(return_value=True)

		source = '/home/sam/movie'
		transfer = Transfer(ftpMock, util, None)
		result = transfer.getFiles(source)

		ftpMock.nlst.assert_called_with(source)
		self.assertTrue(allMovies[0] not in  result)
		self.assertEqual(0, len(result))

	def test_sync_files(self):
		sourceFiles = ['/movie/transformers.mp4']
		target = '/users/willsam100/Desktop/'
		ftpMock = FTP('')
		ftpMock.retrbinary = MagicMock()

		now = util.now()
		targetFile = util.join(target, util.basename(sourceFiles[0]))
		self.__cleanUp__(targetFile)
		
		utilMock = Utils();
		utilMock.splitDirectoriesAndFiles = MagicMock(return_value=([], sourceFiles))
		utilMock.exists = MagicMock(return_value=False)
		utilMock.computeSpeed = MagicMock(return_value=40)
		utilMock.now = MagicMock(return_value=now)

		transfer = Transfer(ftpMock, utilMock, target)
		transfer.sync(sourceFiles)

		utilMock.splitDirectoriesAndFiles.assert_called_with(ftpMock, sourceFiles)
		utilMock.exists.assert_called_with(targetFile)
		ftpMock.retrbinary.assert_called_with('RETR ' + sourceFiles[0], mock.ANY)
		self.assertTrue(util.exists(targetFile))
		self.__cleanUp__(targetFile)
		utilMock.computeSpeed.assert_called_with(now, targetFile)

	def test_sync_directories(self):
		sourceFiles = ['/movie/transformers', '/movie/transformers/transformers.mp4']
		target = '/users/willsam100/Desktop/'
		ftpMock = FTP('')
		ftpMock.retrbinary = MagicMock()
		ftpMock.nlst = MagicMock(return_value=[])

		now = util.now()
		targetDir = util.join(target, util.basename(sourceFiles[0]))
		targetFile = util.join(targetDir, util.basename(sourceFiles[1]))
		self.__cleanUp__(targetDir)
		
		utilMock = Utils();
		def splitDirectoriesAndFiles(*args):
			def secondCall_splitDirectoriesAndFiles(*args):
				return ([], sourceFiles[1:])
			utilMock.splitDirectoriesAndFiles.side_effect = secondCall_splitDirectoriesAndFiles
			return ([sourceFiles[0]], [])

		utilMock.splitDirectoriesAndFiles = MagicMock(side_effect=splitDirectoriesAndFiles)
		utilMock.exists = MagicMock(return_value=False)
		utilMock.computeSpeed = MagicMock(return_value=40)
		utilMock.now = MagicMock(return_value=now)

		transfer = Transfer(ftpMock, utilMock, target)
		transfer.sync(sourceFiles)

		
		utilMock.splitDirectoriesAndFiles.call_args_list == (mock.call(ftpMock, targetDir), mock.call(ftpMock, targetFile))
		utilMock.splitDirectoriesAndFiles.assert_called_with(ftpMock, [])
		utilMock.exists.call_args_list == [mock.call(targetDir), mock.call(targetFile)]
		ftpMock.retrbinary.assert_called_with('RETR ' + sourceFiles[1], mock.ANY)
		self.assertTrue(util.exists(targetFile))
		self.__cleanUp__(targetDir)
		utilMock.computeSpeed.assert_called_with(now, targetFile)


	def __cleanUp__(self, root):
		if util.exists(root) and os.path.isdir(root):
			for filename in os.listdir(root):
				os.remove(util.join(root, filename))
			os.rmdir(root)
		
		if util.exists(root):
			os.remove(root)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestTransfer)
	unittest.TextTestRunner(verbosity=2).run(suite)




