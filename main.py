if __name__ == "__main__":
    import json
    import requests
    import openpyxl
    from configparser import ConfigParser
    from getpaymentdata import getPaymentData

    CONFIG_PATH = 'config.txt'

    config = ConfigParser()
    config.read(CONFIG_PATH)
    production_mode = config['general']['production']
    payment_type = config['general']['type']
    assert payment_type == 'digital' or payment_type == 'physical' or payment_type == 'multi'

    url = "https://sandbox.checkbook.io/v3/check/" + payment_type
    if production_mode == 'enabled':
        url = "https://www.checkbook.io/v3/check/" + payment_type

    api_key = input("Enter API key: ")
    secret_key = input("Enter secret key: ")

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "2015a4a352444886a5dc97094ad54eef" + ":" + "EWir8BmgUhbo70fYJZW94OSoYfEON8"
        }


    make_batch = getPaymentData(CONFIG_PATH)

    # send payments
    succeeded = []
    failed = []
    for payment_batch in make_batch:
        for payment in payment_batch[0]:
            payload = json.dumps(payment[0])
            response = requests.request("POST", url, data=payload, headers=headers)
            if response:
                succeeded.append(payment[1])
            else:
                failed.append(payment[1])
        failed += payment_batch[1]

    # if outcome column chosen, fill with sent/failed
    if config[payment_type]['successful']:
        xfile = openpyxl.load_workbook(config['general']['path'])
        sheet = xfile.get_sheet_by_name('Sheet1')
        sheet['A1'] = 'hello world'
        for i in succeeded:
            coord = config[payment_type]['successful'] + str(i)
            sheet[coord] = 'sent'
        for i in failed:
            coord = config[payment_type]['successful'] + str(i)
            sheet[coord] = 'failed'
        xfile.save(config['general']['path'])
