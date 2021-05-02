from xmlrpc import client

url = 'https://hpo-odoo-online-technical-training-dev-test1-2477170.dev.odoo.com'
db = 'hpo-odoo-online-technical-training-dev-test1-2477170'
username= 'admin'
password = 'admin'

common = client.ServerProxy("{}/xmlrpc/2/common".format(url))
print(common.version()) #{'server_version': '13.0+e', 'server_version_info': [13, 0, 0, 'final', 0, 'e'], 'server_serie': '13.0', 'protocol_version': 1}


uid = common.authenticate(db, username, password, {})
print(uid) #2

models = client.ServerProxy("{}/xmlrpc/2/object".format(url))

model_access = models.execute_kw(db, uid, password, 
                                'sale.order', 'check_access_rights',
                                ['write'], {'raise_exception': False})
print(model_access) #True

draft_quotes = models.execute_kw(db, uid, password, 
                                'sale.order', 'search', 
                                [[['state', '=', 'draft']]])
print(draft_quotes) #[3, 5, 2, 1]

if_confirmed = models.execute_kw(db, uid, password,
                                'sale.order', 'action_confirm',
                                [draft_quotes])
print(if_confirmed) #True


