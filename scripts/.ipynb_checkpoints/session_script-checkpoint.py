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
                                'academy.session', 'check_access_rights',
                                ['write'], {'raise_exception': False})
print(model_access) #False - we need to add access for our admin user // True once admin user added to security group

courses = models.execute_kw(db, uid, password,
                           'academy.course', 'search_read',
                           [[['level', 'in', ['intermediate', 'beginner']]]])
print(courses) #"""[{'id': 1, 'name': 'ERP 101', 'description': 'Learn ERP Systems', 'level': 'beginner', 'active': True, 'base_price': 0.0, 'additional_fee': 10.0, 'total_price': 0.0, 'session_ids': [], 'display_name': 'ERP 101', 'create_uid': [1, 'System'], 'create_date': '2021-05-02 20:04:53', 'write_uid': [1, 'System'], 'write_date': '2021-05-02 20:04:53', '__last_update': '2021-05-02 20:04:53'}, {'id': 2, 'name': 'Accounting 200', 'description': 'Intermediate accounting course', 'level': 'intermediate', 'active': True, 'base_price': 0.0, 'additional_fee': 10.0, 'total_price': 0.0, 'session_ids': [], 'display_name': 'Accounting 200', 'create_uid': [1, 'System'], 'create_date': '2021-05-02 20:04:53', 'write_uid': [1, 'System'], 'write_date': '2021-05-02 20:04:53', '__last_update': '2021-05-02 20:04:53'}]"""

course = models.execute_kw(db, uid, password,
                          'academy.course', 'search',
                          [[['name', '=', 'Accounting 200']]])
print(course) #[2]

session_fields = models.execute_kw(db, uid, password,
                                  'academy.session', 'fields_get',
                                  [], {'attributes': ['string', 'type', 'required']})
print(session_fields) # """{'course_id': {'type': 'many2one', 'required': True, 'string': 'Course'}, 'name': {'type': 'char', 'required': False, 'string': 'Title'}, 'instructor_id': {'type': 'many2one', 'required': False, 'string': 'Instructor'}, 'student_ids': {'type': 'many2many', 'required': False, 'string': 'Students'}, 'start_date': {'type': 'date', 'required': False, 'string': 'Start Date'}, 'duration': {'type': 'integer', 'required': False, 'string': 'Session Days'}, 'end_date': {'type': 'date', 'required': False, 'string': 'End Date'}, 'state': {'type': 'selection', 'required': True, 'string': 'States'}, 'total_price': {'type': 'float', 'required': False, 'string': 'Total Price'}, 'id': {'type': 'integer', 'required': False, 'string': 'ID'}, 'display_name': {'type': 'char', 'required': False, 'string': 'Display Name'}, 'create_uid': {'type': 'many2one', 'required': False, 'string': 'Created by'}, 'create_date': {'type': 'datetime', 'required': False, 'string': 'Created on'}, 'write_uid': {'type': 'many2one', 'required': False, 'string': 'Last Updated by'}, 'write_date': {'type': 'datetime', 'required': False, 'string': 'Last Updated on'}, '__last_update': {'type': 'datetime', 'required': False, 'string': 'Last Modified on'}}"""

new_session = models.execute(db, uid, password,
                            'academy.session', 'create',
                            [
                                {
                                    'course_id': course[0],
                                    'state': 'open',
                                    'duration': 5,
                                }
                            ])
print(new_session) #[1] - This has created a new session in the db (verified by going to our db -> odoo academy -> sessions

