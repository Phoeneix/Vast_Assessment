'''The file for handling any file related event'''


class FileHandler():
	'''Class for handling files'''

	def SaveIntoFile(file_name:str, content:str):
		'''Method to save data into a specific file'''

		with open(file_name, 'a') as f:
			f.write(content)
			f.close()
