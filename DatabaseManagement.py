import mysql.connector, time, os

current_time = time.localtime()
print("Execution started at " + time.strftime('%H:%M:%S GMT', current_time))
InternetFail = mysql.connector.errors.InterfaceError

# return all from a given table. will also return entries of a certain subject if needed.
def ReturnAllMethod(tbl, subject=None):
    print("ReturnAllMethod has been accessed")
    start = time.time()
    database = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected!")
    cursor = database.cursor()
    if subject is None:
        cursor.execute('''SELECT * FROM '''+tbl)
    else:
        cursor.execute('SELECT * FROM ' + tbl + ' WHERE SUBJECT = "' + subject + '"')
    data = cursor.fetchall()
    database.commit()
    cursor.close()
    finish = time.time() - start
    print("Execution took {0} seconds".format(finish))
    return data


# this function is only called when a specialist subject has been given.
def ReturnAllOthers(tbl, subject):
    print("ReturnAllOthers has been accessed")
    start = time.time()
    database = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected!")
    cursor = database.cursor()
    cursor.execute('SELECT * FROM ' + tbl + ' WHERE SUBJECT != "' + subject + '"')
    data = cursor.fetchall()
    database.commit()
    cursor.close()
    finish = time.time() - start
    print("Execution took {0} seconds".format(finish))
    return data

# a test function - allows programmer to make an amendment to the tables.
def AmendTableTestingMethod(tbl, AMENDMENT, newcol, newdef):
     print("AmendTableTestingMethod has been accessed")
     start = time.time()
     database = mysql.connector.connect(
         host="",
         user=" ",
         password="  ",
         database=""
     )

     cursor = database.cursor()
     cmnd = '''ALTER TABLE ''' + tbl + ' ' + AMENDMENT + ' ' + newcol + ' ' + newdef
     cursor.execute(cmnd)

     database.commit()
     cursor.close()
     finish = time.time() - start
     print("Execution took {0} seconds".format(finish))


# allows programmer to make a new entry in
def newUser(username, password, subject):
    print("New user protocol has been accessed")
    start = time.time()
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Server accessed")
    cursor = mydb.cursor()
    cursor.execute('''INSERT IGNORE INTO users (username, password, board) VALUES (%s,%s,%s)''', (username, password,
                                                                                                  subject))
    mydb.commit()
    cursor.close()
    finish = time.time() - start
    print("Execution took {0} seconds".format(finish))


# checks for the existence of users in the database
def testForExistence(item=None, table=None, column=None, **kwargs):
    # uses key word arguments to check if a username or password was given
    username = kwargs.get('username', None)
    password = kwargs.get('password', None)

    print("testForExistence has been accessed")
    start = time.time()
    # open connection to server
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected!")
    # opens a session to the server
    cursor = mydb.cursor()
    # if a username or password has been given
    if username and password is not None:
        # use command to search for username and password in a table
        command = f"SELECT EXISTS(SELECT * FROM {table} WHERE username = '{username}' AND password = '{password}')"
    else:
        # otherwise, search for the given entry in the given column of the given table
        command = "SELECT EXISTS(SELECT * FROM " + table + " WHERE " + column + " = '" + item + "')"
    print(command + " processing..")
    cursor.execute(command)
    # return the matching result
    investigation = cursor.fetchone()
    # if there was an entry, the server will return 1 for true
    if investigation[0] == 1:
        # save all changes and close session
        mydb.commit()
        cursor.close()
        finish = time.time() - start
        print("Success! Execution took {0} seconds".format(finish))
        # return True for successful operation
        return True
    else:
        # save all changes and close session
        mydb.commit()
        cursor.close()
        finish = time.time() - start
        print("Failure. Execution took {0} seconds".format(finish))
        # return False for unsuccessful operation
        return False


def DelMethod():
    database = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! (DelMethod)")
    cursor = database.cursor()
    sql = "DELETE FROM graph WHERE username = ' ood'"
    cursor.execute(sql)
    database.commit()
    print(cursor.rowcount, "record(s) deleted")


def RetrieveCourse(user):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Retrieving course.")
    cursor = mydb.cursor()
    cmnd = "SELECT board FROM users WHERE username = '" + user + "'"
    cursor.execute(cmnd)
    result = cursor.fetchone()[0]
    mydb.commit()
    return result


def ManageFiles(username):
    drx_name = os.path.expanduser('~/Documents/appleseed/assets/documents/') + username
    cv_name = drx_name + "/" + username + "CV.docx"
    ps_name = drx_name + "/" + username + "PS.docx"

    if not os.path.exists(drx_name):
        os.mkdir(drx_name)
        if not os.path.exists(cv_name):
            f = open(cv_name, "x")
            f.close()
            if not os.path.exists(ps_name):
                f = open(ps_name, "x")
                f.close()


def retrieveContent(specialism):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Obtaining specialism.")
    cursor = mydb.cursor()
    cmnd = "SELECT * FROM courses WHERE board = '" + specialism + "'"
    cursor.execute(cmnd)
    result = cursor.fetchall()
    mydb.commit()
    return result


def createContent():
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! let's create a new Table!")
    cursor = mydb.cursor()
    cmnd = '''CREATE TABLE choices (
            choiceID int auto_increment not null primary key,
            username VARCHAR(120) NOT NULL,
            CONSTRAINT username_keeper FOREIGN KEY(username) REFERENCES users(username),
            choice1 VARCHAR(120) NOT NULL,
            choice2 VARCHAR(120) NOT NULL,
            choice3 VARCHAR(120) NOT NULL,
            choice4 VARCHAR(120) NOT NULL,
            choice5 VARCHAR(120) NOT NULL
            );
            '''
    cursor.execute(cmnd)
    mydb.commit()


def createNewCourse():
    start = time.time()
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! lets create a new course!")
    cursor = mydb.cursor()
    name = str(input("Enter name: "))
    subject = str(input("Enter subject: "))
    host = str(input("Enter host: "))
    choice = str(input("YES or NO? Do you want a description? "))
    if choice.upper() == "YES":
        description = str(input("Enter description: "))
    else:
        description = None
    URL = str(input("Enter URL: "))

    if description is not None:
        cursor.execute('''INSERT IGNORE INTO courses (NAME, SUBJECT, HOST, DESCRIPTION, URL) VALUES (%s,%s,%s,%s,
        %s)''',(name, subject, host, description, URL))
    else:
        cursor.execute('''INSERT IGNORE INTO courses (NAME, SUBJECT, HOST, URL) VALUES (%s,%s,%s,%s)''',
                       (name, subject, host, URL))
    mydb.commit()
    cursor.close()
    finish = time.time() - start
    print("Execution took {0} seconds".format(finish))


def CustomSQLInteraction(cmd):
    start = time.time()
    database = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("CustomSQLInteraction: CONNECTED")
    cursor = database.cursor(buffered=True)
    print("EXECUTING", cmd)
    cursor.execute(cmd)
    database.commit()
    cursor.close()
    finish = time.time() - start
    print("Execution took {0} seconds".format(finish))
    return cursor.fetchall()


def GetUserDetails(username):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Retrieving course.")
    cursor = mydb.cursor()
    cmnd = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(cmnd)
    result = cursor.fetchone()
    mydb.commit()
    return result

def addGrade(un, sub, prc):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Adding entry.")
    cursor = mydb.cursor()
    # generates date for date entry as a string
    today = str(time.strftime('%Y-%m-%d'))
    print(today)
    # implements grade into server
    cursor.execute('''INSERT IGNORE INTO graph (USERNAME, SUBJECT, ENTRY, DATE) VALUES (%s,%s,%s,%s)''',(un, sub,
                                                                                                         prc, today))
    # returns grade
    result = cursor.fetchone()
    mydb.commit()
    return result

def retrieveGrades(un, sub=None):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print(f"Connected! Loading grades for {un}")
    cursor = mydb.cursor()
    if sub is not None:
        cursor.execute(f'''SELECT * FROM graph WHERE USERNAME = '{un}' AND SUBJECT = '{sub}';''')
    else:
        cursor.execute(f'''SELECT * FROM graph WHERE USERNAME = '{un}';''')
    result = cursor.fetchall()
    print(f"There were {len(result)} results.")
    mydb.commit()
    return result

def addInbox(sender, reciever, title, url):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected, adding to inbox")
    cursor = mydb.cursor()
    today = str(time.strftime('%Y-%m-%d'))
    try:
        cursor.execute('''INSERT INTO inbox (sender, sendto, title, url, date) VALUES (%s, %s, %s, %s, %s)''', (sender, reciever, title, url, today))
        mydb.commit()
        return True
    except:
        return False

def retrieveMessages(user):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Obtaining specialism.")
    cursor = mydb.cursor()
    cmnd = "SELECT * FROM inbox WHERE sendto = '" + user + ""
    cursor.execute(cmnd)
    result = cursor.fetchall()
    mydb.commit()
    return result

def EradicateGradeHistory(user):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Deleting user grades.")
    cursor = mydb.cursor()
    cmnd = "DELETE FROM graph WHERE username = '" + user + ""
    cursor.execute(cmnd)
    mydb.commit()
    return True

def EradicateInboxHistory(user):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Deleting user messages.")
    cursor = mydb.cursor()
    cmnd = "DELETE FROM inbox WHERE sender = '" + user + "'"
    cursor.execute(cmnd)
    cmnd = "DELETE FROM inbox WHERE sendto = '" + user + "'"
    cursor.execute(cmnd)
    mydb.commit()
    return True

def EradicateUserHistory(user):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Deleting user.")
    cursor = mydb.cursor()
    cmnd = "DELETE FROM users WHERE username = '" + user + "'"
    cursor.execute(cmnd)
    mydb.commit()
    return True

def UpdateDetails(detail, item, user):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! Deleting user.")
    cursor = mydb.cursor()
    cmnd = f'''UPDATE users SET {detail} = "{item}" WHERE username = '{user}';'''
    cursor.execute(cmnd)
    mydb.commit()
    return True

def addtoChoice(user, c1, c2, c3, c4, c5):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected! lets create a choice!")
    cursor = mydb.cursor()
    cursor.execute('''INSERT IGNORE INTO choices (choice1, choice2, choice3, choice4, choice5, username) VALUES (%s,%s,%s,%s,%s,%s)''', (c1, c2, c3, c4, c5, user))
    mydb.commit()
    cursor.close()

def UpdateChoices(detail, item, user):
    mydb = mysql.connector.connect(
        host="",
        user=" ",
        password="  ",
        database=""
    )
    print("Connected!")
    cursor = mydb.cursor()
    cmnd = f'''UPDATE choices SET {detail} = "{item}" WHERE username = '{user}';'''
    print(cmnd)
    cursor.execute(cmnd)
    mydb.commit()
    return True

def returnChoices(user):
    mydb = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    print("Connected! lets read a choice!")
    cursor = mydb.cursor(buffered=True)
    cursor.execute(f'''SELECT * FROM choices WHERE username = '{user}';''')
    mydb.commit()
    result = cursor.fetchone()
    cursor.close()
    return result

if __name__ == "__main__":
    finishtime = time.localtime()
    print("Execution ended at " + time.strftime('%H:%M:%S GMT', finishtime))
