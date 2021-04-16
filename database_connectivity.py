import mysql.connector
def ComResAjout(command,reservation):
    mydb=mysql.connector.connect(
        host="localhost",
        user="oussama",
        password="michiamoOUSSAMA",
        database="rasadatabase",auth_plugin='mysql_native_password'
    )
    mycursor=mydb.cursor()
    sql2='INSERT INTO CLIENTS(command,reservation) VALUES ("{0}","{1}");'.format(command,reservation)
    mycursor.execute(sql2)
    mydb.commit()
    print(mycursor.rowcount,"record inserted.")
    return mycursor.lastrowid

def modification(modification,code):
    mydb=mysql.connector.connect(
        host="localhost",
        user="oussama",
        password="michiamoOUSSAMA",
        database="rasadatabase",auth_plugin='mysql_native_password'
    )
    mycursor=mydb.cursor()
    sql='UPDATE CLIENTS SET  modification= "{0}" WHERE id="{1}"'.format(modification,code)
    mycursor.execute(sql)
    mydb.commit()
    return

def cancel(code):
    mydb=mysql.connector.connect(
        host="localhost",
        user="oussama",
        password="michiamoOUSSAMA",
        database="rasadatabase",auth_plugin='mysql_native_password'
    )
    mycursor=mydb.cursor()
    sql='DELETE from CLIENTS WHERE id="{0}"'.format(code)
    mycursor.execute(sql)
    mydb.commit()
    return

def bill(code):
    mydb=mysql.connector.connect(
        host="localhost",
        user="oussama",
        password="michiamoOUSSAMA",
        database="rasadatabase",auth_plugin='mysql_native_password'
    )
    mycursor=mydb.cursor()
    sql='select Price from CLIENTS WHERE id="{0}"'.format(code)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult[0][0]

if __name__== "__main__":
    ComResAjout("example","example")
