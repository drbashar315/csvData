import csv,re,sys

class csvData():
    def __init__(self,fn):
        self.filename = fn
        canopen = False
        try:
            f = open(fn,'r')
            f.close()
            canopen = True
        except Exception as e:
            print('Could not open ' , fn)
        self.canopen = canopen
        if self.canopen:
            self.col_delimiter = ','
            self.row_delimiter = '\n'
            self.totalRows = 0
            self.originalFields = []
            self.filteredFields = []
            self.mismatchRows = []
            self.f = None
            self.getFields()
    def getReader(self):
        self.f = open(self.filename,'r',newline=self.row_delimiter)
        reader = csv.reader(self.f,delimiter=self.col_delimiter)
        return reader
    def getFields(self):
        reader = self.getReader()
        for row in reader:
            #print(row)
            self.originalFields = row
            break
        self.f.close()
        for field in self.originalFields:
            s = field.lower().strip()
            s = s.replace(' ','_')
            s = re.sub(r'[^0-9a-z_]', '', s)
            #print(field, s)
            self.filteredFields.append(s)
    
    def checkShape(self):
        #return True if num of cols is the same in all rows, False otherwise
        #save the result as a class var called self.mismatchRows
        #count the num of rows total-> self.totalRows
        #run 2 unit tests - one which there is a mismatch and one where there is not
        #use getReader method

if __name__ == '__main__':
    import sys
    
    #print(sys.argv)
    if len(sys.argv) == 2:
        #set the default behavior of the script when run from the cmd line
        c = csvData(sys.argv[1])
        if c.canopen:
            #print(c.filename)
            print(c.originalFields)
            print(c.filteredFields)
            #c.guessTypes()
    else:
        print('Use: >python csvData.py [csvfilename.csv]')


















