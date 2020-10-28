from csvData import csvData 

c = csvData('wifi_list1.csv')
print(c.filename)

c = csvData('wifi_list.csv')
print(c.originalFields)
print(c.filteredFields)