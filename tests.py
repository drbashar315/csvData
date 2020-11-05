from csvData import csvData 


c = csvData('wifi_list.csv')
print(c.originalFields)
print(c.filteredFields)
c.guessTypes()

#
print(c.createTable())
#c.insertSql('export.sql')


