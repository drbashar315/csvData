import csv,re,sys,datetime,pymysql

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
            self.types = {}
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
    def createTable(self):
        sql = ''
        for field in self.filteredFields:
            sql+=field
        '''
        # use the filtered fieldnames
        # return sql string
        CREATE TABLE IF NOT EXISTS `conlontj_wifi` (
          `id` int(5) NOT NULL,
          `MAC` varchar(50) NOT NULL,
          `SSID` varchar(50) NOT NULL,
          `AuthMode` varchar(100) NOT NULL,
          `FirstSeen` datetime NOT NULL,
          `Channel` int(3) NOT NULL,
          `RSSI` int(5) NOT NULL,
          `CurrentLatitude` decimal(11,8) NOT NULL,
          `CurrentLongitude` decimal(11,8) NOT NULL,
          `AltitudeMeters` decimal(7,2) NOT NULL,
          `Type` varchar(50) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

        '''
        return sql
    def insertSql(self,filename):
        sql = ''
        #saves all INSERT queries to a .sql file
    def guessTypes(self):
        n =0 
        while n < len(self.originalFields):#iterate over cols
            gt = {'date':0,'datetime':0,'varchar':0,'int':0,'decimal':0}
            gl = {'m':1,'d':1,'vl':1,'il':1}
            reader = self.getReader()
            i=0
            for row in reader:
                if i > 0:
                    r = row[n].strip()
                    hasVote = False
                    try:
                        fdt = datetime.datetime.strptime(r, "%Y-%m-%d %H:%M:%S")
                        gt['datetime'] += 1
                        hasVote = True
                    except ValueError as e:
                        pass
                    try:
                        fdt = datetime.datetime.strptime(r, "%Y/%m/%d %H:%M:%S")
                        gt['datetime'] += 1
                        hasVote = True
                    except ValueError as e:
                        pass
                    try:
                        fdt = datetime.datetime.strptime(r, "%Y/%m/%d")
                        gt['date'] += 1
                        hasVote = True
                    except ValueError as e:
                        pass
                    try:
                        fdt = datetime.datetime.strptime(r, "%Y-%m-%d")
                        gt['date'] += 1
                        hasVote = True
                    except ValueError as e:
                        pass
                    # 34.345345
                    # -23e23
                    if r.count('.') == 1:
                        parts = r.split('.')
                        intok = False
                        try:
                            int(parts[0])
                            int(parts[1])
                            intok = True
                            gt['decimal'] += 1
                            hasVote = True
                        except ValueError as e:
                            pass
                        if intok:
                            if len(r) > gl['m']:#max logic
                                gl['m'] = len(r)
                            if len(parts[1]) > gl['d']:
                                gl['d'] = len(parts[1])
                    try:
                        int(r)
                        gt['int'] += 1
                        hasVote = True
                        if len(r) > gl['il']:
                            gl['il'] = len(r)
                    except ValueError as e:
                        pass
                    if hasVote == False:
                        gt['varchar'] += 1
                        if len(r) > gl['vl']:
                            gl['vl'] = len(r)
                i+=1
            typekey = ''
            tm = 0
            for t, count in gt.items():
                if count > tm:
                    tm = count
                    typekey = t
            if typekey == 'date' or typekey == 'datetime':
                self.types[n] = typekey
            elif typekey == 'varchar':
                self.types[n] = typekey + '('+str(gl['vl'])+')'
            elif typekey == 'int':
                self.types[n] = typekey + '('+str(gl['il'])+')'
            elif typekey == 'decimal':
                self.types[n] = typekey + '('+str(gl['m'])+','+str(gl['d'])+')'
            else:
                self.types[n] = typekey + 'varchar(255)'
            
            print(self.filteredFields[n],self.types[n])
            print(gt)
            n+=1
    def checkShape(self):
        #return True if num of cols is the same in all rows, False otherwise
        #save the result as a class var called self.mismatchRows
        #count the num of rows total-> self.totalRows
        #run 2 unit tests - one which there is a mismatch and one where there is not
        #use getReader method
        pass
    def getCursor0(self):
        conn = pymysql.connect(host='mysql.clarksonmsda.org', 
        port=3306, 
        user='ia626',
        passwd='ia626clarkson', 
        db='ia626', autocommit=True) #setup our credentials
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return cur
    def getCursor1(self,host,port,user,passwd,db):
        conn = pymysql.connect(host=host, 
        port=port, 
        user=user,
        passwd=passwd, 
        db=db, autocommit=True) #setup our credentials
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return cur
    def getCursor2(self):
        import config
        conn = pymysql.connect(host=config.DB['host'], 
        port=config.DB['port'], 
        user=config.DB['user'],
        passwd=config.DB['passwd'], 
        db=config.DB['db'], autocommit=True) #setup our credentials
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return cur
        
if __name__ == '__main__':#if script is being run as a CLI script
    import sys
    
    #print(sys.argv)
    if len(sys.argv) == 2:
        #set the default behavior of the script when run from the cmd line
        c = csvData(sys.argv[1])
        if c.canopen:
            print(c.filename)
            print(c.originalFields)
            print(c.filteredFields)
            c.guessTypes()
    else:
        print('Use: >python csvData.py [csvfilename.csv]')


















