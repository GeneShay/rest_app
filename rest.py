import json, collections, pymysql, web
from bson import json_util

urls = (

    '/user', 'Users',
    '/user/(.*)', 'User'
)
app = web.application(urls, globals())


class User:
    connection = pymysql.connect(host='genetestrds.cg2mxphbjirw.us-west-1.rds.amazonaws.com', port=3306,
                                     user='GeneTest', password='TestPassword', db='TestDB')
    def GET(self, user):
        sql = "SELECT * FROM users WHERE uuid = '%s'" % user
        cursor = self.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        field_names = json_print(rows, cursor)
        cursor.close()
        self.connection.close()
        return field_names + '\n'

    def DELETE(self, uuid):
        print uuid
        sql = "DELETE FROM users WHERE uuid = '%s'" % uuid
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return 'User with nickname "%s" is removed\n' % uuid

    def PUT(self, uuid):
        data = json.loads(web.data())
        fn, ln, email = data["first_name"], data["last_name"], data["email"]
        sql = "UPDATE users SET first_name = '%s', last_name = '%s', email = '%s' WHERE uuid = '%s'" % (fn, ln, email, uuid)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return 'User with nickname "%s" is updated\n' % uuid

class Users:
    connection = pymysql.connect(host='genetestrds.cg2mxphbjirw.us-west-1.rds.amazonaws.com', port=3306,
                                 user='GeneTest', password='TestPassword', db='TestDB')    
    def GET(self):
        sql = "SELECT * FROM users"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        field_names = json_print(rows, cursor)
        cursor.close()
        self.connection.close()
        return field_names + '\n'

    def POST(self):
        data = json.loads(web.data())
        uuid, fn, ln, email = data["uuid"], data["first_name"], data["last_name"], data["email"]
        user_check = 'SELECT * FROM users WHERE  uuid = "%s"' %uuid
        add_user = 'INSERT INTO users (uuid, first_name, last_name, email, data) ' \
                   'VALUES ("%s", "%s", "%s","%s", now())' % (uuid, fn, ln, email)
        cursor = self.connection.cursor()
        cursor.execute(user_check)
        rows = cursor.fetchall()

        print rows
        if not rows:

            cursor.execute(add_user)
            self.connection.commit()
            cursor.close()
            self.connection.close()
            
            return 'User "%s" created\n' % uuid
        else:
            cursor.close()
            self.connection.close()
            return 'User with uuid "%s" exists\n' %uuid



def json_print(rows, cursor):
        field_names = [i[0] for i in cursor.description]
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d[ field_names[0] ] = row[0]
            d[ field_names[1] ] = row[1]
            d[ field_names[2] ] = row[2]
            d[ field_names[3] ] = row[3]
            d[ field_names[4] ] = row[4]
            d[ field_names[5] ] = row[5]
            objects_list.append(d)
        json_string = json.dumps( objects_list, default=json_util.default )
        return json_string + '\n'
if __name__ == "__main__":
    app.run()
