def getPaymentData(config_path):

    # referenced from https://stackoverflow.com/questions/7261936/convert-an-excel-or-spreadsheet-column-letter-to-its-number-in-pythonic-fashion
    def col2num(col):
        import string
        if not col: return 0
        if col.isdigit(): return int(col)
        num = 0
        for c in col:
            if c in string.ascii_letters:
                num = num * 26 + (ord(c.upper()) - ord('A')) + 1
        return num


    import json
    from configparser import ConfigParser

    config = ConfigParser()
    config.read(config_path)

    payment_type = config['general']['type']
    payment_columns = config[payment_type]

    # check required fields are specified
    required_col = []
    if payment_type == 'digital':
        required_col = ['recipient', 'name', 'amount']
    elif payment_type == 'physical':
        required_col = ['recipient_line1', 'recipient_city', 'recipient_state', 'recipient_zip', 'name', 'amount']
    elif payment_type == 'multi':
        required_col = ['name1', 'recipient1', 'name2', 'recipient2', 'amount']

    for req in required_col:
        assert payment_columns[req]

    def processLine(cells):
        def getCell(index):
            if index == 0: return ''
            index -= 1 # change index from 1-based to 0-based
            try:
                return cells[index]
            except:
                return ''

        data = {}
        fields = []
        if payment_type == 'digital':
            fields = ['recipient', 'name', 'amount', 'number', 'description', 'account', 'attachment', 'remittance_advice']
        elif payment_type == 'physical':
            fields = ['recipient', 'name', 'amount', 'number', 'description', 'account', 'remittance_advice']
        elif payment_type == 'multi':
            fields = ['recipients', 'amount', 'number', 'description', 'account', 'attachment', 'remittance_advice']

        for field in fields:
            entry = None

            if field == 'remittance_advice':
                entry = []
                ids = payment_columns['remittance_ids'].split('\n')
                amounts = payment_columns['remittance_amounts'].split('\n')
                dates = payment_columns['remittance_dates'].split('\n')
                descs = payment_columns['remittance_descriptions'].split('\n')
                for i in range(max(len(ids), len(amounts), len(dates), len(descs))): # number of records
                    record = {}
                    if i < len(ids):
                        if getCell(col2num(ids[i])):
                            record['id'] = getCell(col2num(ids[i]))
                    if i < len(amounts):
                        if getCell(col2num(amounts[i])):
                            record['amount'] = getCell(col2num(amounts[i]))
                    if i < len(dates):
                        if getCell(col2num(dates[i])):
                            record['date'] = getCell(col2num(dates[i]))
                    if i < len(descs):
                        if getCell(col2num(descs[i])):
                            record['description'] = getCell(col2num(descs[i]))
                    if record:
                        entry.append(record)
            elif payment_type == 'physical' and field == 'recipient':
                entry = {
                    'line_1': getCell(col2num(payment_columns['recipient_line1'])),
                    'line_2': getCell(col2num(payment_columns['recipient_line2'])),
                    'city': getCell(col2num(payment_columns['recipient_city'])),
                    'state': getCell(col2num(payment_columns['recipient_state'])),
                    'zip': getCell(col2num(payment_columns['recipient_zip'])),
                    'country': getCell(col2num(payment_columns['recipient_country']))
                }
            elif payment_type == 'multi' and field == 'recipients':
                entry = [{
                    'name': getCell(col2num(payment_columns['name1'])),
                    'recipient': getCell(col2num(payment_columns['recipient1']))
                }, {
                    'name': getCell(col2num(payment_columns['name2'])),
                    'recipient': getCell(col2num(payment_columns['recipient2']))
                }]
            else:
                entry = getCell(col2num(payment_columns[field]))

            if entry:
                data[field] = entry

        # assertrequired fields are filled
        if payment_type == 'digital':
            assert data['recipient'] and \
                   data['name'] and \
                   data['amount']
        elif payment_type == 'physical':
            assert data['recipient']['line_1'] and \
                   data['recipient']['city'] and \
                   data['recipient']['state'] and \
                   data['recipient']['zip'] and \
                   data['name'] and \
                   data['amount']
        elif payment_type == 'multi':
            assert data['recipients'][0]['name'] and \
                   data['recipients'][0]['recipient'] and \
                   data['recipients'][1]['name'] and \
                   data['recipients'][1]['recipient'] and \
                   data['amount']

        return data


    with open(config['general']['path']) as f:
        start_row = 0
        end_row = 0
        if config['general']['start_row']:
            start_row = int(config['general']['start_row'])
        if config['general']['end_row']:
            end_row = int(config['general']['end_row'])

        payment_batch = []
        failed_lines = []
        i = 0
        for line in f:
            print(line)
            i += 1
            if i < start_row: continue
            try:
                payment = processLine(line.strip('\n').split('\t'))
                payment_batch.append(payment)
            except:
                failed_lines.append(line)

            if i == end_row and end_row != 0: break
            if i-start_row % int(config['general']['batch_size']) == 0 and i-start_row != 0:
                yield (payment_batch, failed_lines)
                payment_batch = []
                failed_lines = []

        if payment_batch or failed_lines: # remaining payments to send out
            yield (payment_batch, failed_lines)
