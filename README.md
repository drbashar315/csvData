# csvData


## Usage:
- clone repo
- rename config.sample.py to config.py
- change DB credential in config.py
- ```python3 csvData.py mycsvfile.csv```


## Todo:

- [ ] Scale to really large csv files (2gb maybe?)
- [ ] Get the total number of rows
- [ ] Get the headers for the csv
- [ ] Create a MySQL 'create table' code from the file 
- [ ] Guess the types and lengths (when required) of each column
- [ ] fix bad/missing data, trailing spaces


## Assumptions
* default delim is , and \n
* header in first row
* bad data will be skipped
* CSV file must be openable
* CSV data conforms to the way the python csv module parses it

##SQL types
* datetime
* date
* decimal**
* int*
* varchar*


