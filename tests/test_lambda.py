import os
import sys
sys.path.append(os.getcwd()+'/gold_poll')
from gold_poll.lambda_function import fettle, transform, group, primary, change_email, no_common_emails

incoming = [
    {
    "ID": 559,
    "Member Number": 5004,
    "Salutation": "Mr",
    "Firstname": "Julian",
    "Lastname": "Cable",
    "Address1": "X",
    "Address2": "Y",
    "Address3": "",
    "Town": "Z",
    "County": "A",
    "Postcode": "N00 0NN",
    "Country": "United Kingdom",
    "Telephone": "",
    "Mobile": "00000 000000",
    "Email": "someone@yahoo.com",
    "Comments": "",
    "Membership Type": "Family",
    "Payment Method": "Direct Debit",
    "Area": "Scotland",
    "GDPR": True,
    "Primary": True,
    "Trailer": True,
    "Edited By:": 0,
    "Edited:": "30-11-0001 00:00:00",
    "Year Of Birth": 2000,
    "Reason For Joining": "Not Known",
    "Year Joined": 2011,
    "Status": "Paid Up",
    "Interest Areas": "DB,NW"   
    },
    {
 "ID": 1219,
    "Member Number": 5004,
    "Salutation": "Mrs",
    "Firstname": "Alison",
    "Lastname": "Cable",
    "Address1": "X",
    "Address2": "Y Road",
    "Address3": "",
    "Town": "Z",
    "County": "A",
    "Postcode": "N00 0NN",
    "Country": "United Kingdom",
    "Telephone": "",
    "Mobile": "00000 333333",
    "Email": "someone@yahoo.com",
    "Comments": "",
    "Membership Type": "Family",
    "Payment Method": "Direct Debit",
    "Area": "Scotland",
    "GDPR": True,
    "Primary": False,
    "Trailer": True,
    "Edited By:": 0,
    "Edited:": "30-11-0001 00:00:00",
    "Year Of Birth": 0,
    "Reason For Joining": "Not Known",
    "Year Joined": 0,
    "Status": "Paid Up",
    "Interest Areas": "EC"       
    },
    {
    "ID": 35000,
    "Member Number": 5004,
    "Email": "someonelse@gmail.com",
    "Primary": False,
    'Interest Areas': ''
    },
];
wanted = [
  {
    "ID": 559,
    "Member Number": 5004,
    "Salutation": "Mr",
    "Firstname": "Julian",
    "Lastname": "Cable",
    "Address1": "X",
    "Address2": "Y",
    "Address3": "",
    "Town": "Z",
    "County": "A",
    "Postcode": "N00 0NN",
    "Country": "United Kingdom",
    "Telephone": "",
    "Mobile": "00000 000000",
    "Email": "someone@yahoo.com",
    "Comments": "",
    "Membership Type": "Family",
    "Payment Method": "Direct Debit",
    "Area": "Scotland",
    "GDPR": True,
    "Primary": True,
    "Trailer": True,
    "Edited By:": 0,
    "Edited:": "30-11-0001 00:00:00",
    "Year Of Birth": 2000,
    "Reason For Joining": "Not Known",
    "Year Joined": 2011,
    "Status": "Paid Up",
    "Interest Areas": ["DB","NW"]
  },
  {
    "ID": 1219,
    "Member Number": 5004,
    "Salutation": "Mrs",
    "Firstname": "Alison",
    "Lastname": "Cable",
    "Address1": "X",
    "Address2": "Y Road",
    "Address3": "",
    "Town": "Z",
    "County": "A",
    "Postcode": "N00 0NN",
    "Country": "United Kingdom",
    "Telephone": "",
    "Mobile": "00000 333333",
    "Email": "1219@oga.org.uk",
    "Comments": "",
    "Membership Type": "Family",
    "Payment Method": "Direct Debit",
    "Area": "Scotland",
    "GDPR": True,
    "Primary": False,
    "Trailer": True,
    "Edited By:": 0,
    "Edited:": "30-11-0001 00:00:00",
    "Year Of Birth": 0,
    "Reason For Joining": "Not Known",
    "Year Joined": 0,
    "Status": "Paid Up",
    "Interest Areas": ["EC"]
  },
  {
    "ID": 35000,
    "Member Number": 5004,
    "Email": "someonelse@gmail.com",
    "Primary": False,
    'Interest Areas': [],
  }
]

def test_fettle():
    assert fettle({'Interest Areas':''}) == {'Interest Areas': []}

def test_group():
    r = group(incoming)
    assert r[5004] == incoming

def test_primary():
    assert primary(incoming)['ID'] == 559

def test_change_email():
    p = primary(incoming)
    assert change_email(p, p['Email'])['Email'] == p['Email']
    assert change_email(incoming[1], p['Email'])['Email'] == "1219@oga.org.uk"
    assert change_email(incoming[2], p['Email'])['Email'] == incoming[2]['Email']

def test_no_common_emails():
    fettled = [fettle(item) for item in incoming]
    nce = no_common_emails(fettled)
    assert nce == wanted

def test_transform():
    assert transform(incoming) == wanted
