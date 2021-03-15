# importing required modules
import os
import PyPDF2
from shutil import copyfile

# directory of verified pdf files
DIRECTORY_VERIFIRED = 'verificados'

# function to get sealCode and sealCodeWithDigit
def getSealCode(rootFiles):
	# search .zip file inside directory
	print('> finding seal zip file...')

	for file in rootFiles:
		if '.zip' in file:
			sealFile = file
			break

	# extract seal code from zipped seal file
	sealCode = sealFile.replace(".zip", "")
	sealCodeWithDigit = '{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}-{}'.format(*sealCode)

	print('  > sealCode:', sealCode)
	print('  > sealCodeWithDigit:', sealCodeWithDigit)

	return sealCode, sealCodeWithDigit

# get all .pdf files from root directory
def getPdfFiles(rootFiles):
	print('\n> listing pdf files...')

	pdfFiles = []
	for file in rootFiles:
		if '.pdf' in file:
			pdfFiles.append(file)
			print('  > pdf file:', file)

	# get pdfs that match with seal code
	print('\n> finding pdf matchs with seal code...')
	return pdfFiles

# get pdf that matches with sealCode
def getPdfMatchesSealCode(pdfFiles, sealCode, sealCodeWithDigit):
	pdfFoundList = []

	for pdf in pdfFiles:
		filePath = os.path.join(rootDir, pdf)

		pdfFileObj = open(filePath, 'rb')
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
		pageObj = pdfReader.getPage(0)

		content = pageObj.extractText().split('\n')

		for line in content:
			if line == sealCode or line == sealCodeWithDigit:
				pdfFoundList.append(pdf)
				break
		
		pdfFileObj.close()

	for pdf in pdfFoundList:
		print('  > match found:', pdf)

	return pdfFoundList

# copy verified pdfs to directory verified
def copyVerifiedPdfs(rootDir, pdfFileList):
	# create directory of verifired pdf files
	if not os.path.exists(DIRECTORY_VERIFIRED):
	    os.makedirs(DIRECTORY_VERIFIRED)

	# copy pdf verifired files to directory
	print('\n> coyping pdf files to verifired directory...')

	countFileAmount = 0

	for pdf in pdfFileList:
		destPath = os.path.join(rootDir, pdf)
		sourcePath = os.path.join(DIRECTORY_VERIFIRED, pdf)

		if not os.path.exists(sourcePath):
			copyfile(destPath , sourcePath)
			print('  > copied:', pdf)
			countFileAmount += 1

	return countFileAmount

# get file root directory
rootDir = os.path.dirname(os.path.abspath(__file__))

# get files from root directory
rootFiles = os.listdir(rootDir)

sealCode, sealCodeWithDigit = getSealCode(rootFiles)
pdfFiles = getPdfFiles(rootFiles)
pdfMatches = getPdfMatchesSealCode(pdfFiles, sealCode, sealCodeWithDigit)
totalCopiedFiles = copyVerifiedPdfs(rootDir, pdfMatches)

print('\n> all done successfully ({} copied files)'.format(totalCopiedFiles))
