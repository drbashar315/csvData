from csvData import csvData 


c = csvData('wifi_list.csv')
print(c.originalFields)
print(c.filteredFields)
c.guessTypes()
cur = c.getCursor1()
print(cur)

#
print(c.createTable())
#c.insertSql('export.sql')


