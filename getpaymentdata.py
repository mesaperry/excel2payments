def getPaymentData(config_path):
    from configparser import ConfigParser

    config = ConfigParser()
    config.read(config_path)

    payment_type = config['general']['type']
    payment_columns = config[payment_type]


    # check required fields have specified columns
    if payment_type == 'digital':
        if not payment_columns['recipient'] or \
           not payment_columns['name'] or \
           not payment_columns['amount']:
            raise ValueError('Missing specified columns for required fields')

    if payment_type == 'physical':
        if not payment_columns['recipient_line1'] or \
           not payment_columns['recipient_line2'] or \
           not payment_columns['recipient_city'] or \
           not payment_columns['recipient_state'] or \
           not payment_columns['recipient_zip'] or \
           not payment_columns['recipient_country'] or \
           not payment_columns['name'] or \
           not payment_columns['amount']:
            raise ValueError('Missing specified columns for required fields')

    if payment_type == 'multi':
        if not payment_columns['name1'] or \
           not payment_columns['recipient1'] or \
           not payment_columns['name2'] or \
           not payment_columns['recipient2'] or \
           not payment_columns['amount']:
            raise ValueError('Missing specified columns for required fields')


    # referenced from https://stackoverflow.com/questions/7261936/convert-an-excel-or-spreadsheet-column-letter-to-its-number-in-pythonic-fashion
    def col2num(col):
        num = 0
        for c in col:
            if c in string.ascii_letters:
                num = num * 26 + (ord(c.upper()) - ord('A')) + 1
        return num

    # pack field column pairs into dictionary
    


    def processLine(cells):
        print(cells)
  
    with open(config['general']['path']) as f:
        for line in f:
            processLine(line.strip('\n').split('\t'))




getPaymentData('config.txt')