# import requests

# url = "https://demo.checkbook.io/v3/check/digital"

# payload = '''{
#     \"recipient\":\"testing@checkbook.io\",
#     \"name\":\"Widgets Inc.\",
#     \"amount\":5,
#     \"remittance_advice\":[{
#         \"amount\":5.55,
#         \"date\":\"2020-05-13\"
#         }]
#     }'''
# headers = {
#     'accept': "application/json",
#     'content-type': "application/json"
#     }

# response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)

from getpaymentdata import getPaymentData

payload = '''{
    \"recipient\":\"testing@checkbook.io\",
    \"name\":\"Widgets Inc.\",
    \"amount\":5,
    \"remittance_advice\":[{
        \"amount\":5.55,
        \"date\":\"2020-05-13\"
        }]
    }'''

print(payload)

make_batch = getPaymentData('config.txt')

for payment_batch in make_batch:
    for payment in payment_batch[0]:
        print(payment)