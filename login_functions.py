'''
Contains functions for log in features
'''
from connection import *
def get_pw_user(user_id):
    '''
        Get password of the user
        Args: 
            user id
        Return:
            password of the user
    '''
    #get password
    cursor.execute(
            """
            SELECT pwd 
            FROM users
            WHERE uid = ?;
            """, (user_id,))
    result = cursor.fetchone()
    if result is None:
        return None
    return result[0]

def get_pw_artist(user_id):
    '''
        Get password of the user
        Args: 
            user id
        Return:
            password of the user
    '''
    #get password
    cursor.execute(
            """
            SELECT pwd 
            FROM artists
            WHERE aid = ?;
            """, (user_id,))

    result = cursor.fetchone()
    if result is None:
        return None
    return result[0]
    

def check_pw(user_id, input_pwd):
    '''
        Check if the input password is correct
        Args:
            user_id
            input_pwd: password input by the user
        Return:
            correct_pwd: 
                correct_pwd[0] is true if it matches the user password else false
                correct_pwd[1] is true if it matches the artist password else false
    '''
    correct_pwd = [False,False]
    if input_pwd == get_pw_user(user_id):
        correct_pwd[0] = True
    if input_pwd == get_pw_artist(user_id):
        correct_pwd[1] = True
    return correct_pwd

    
def check_uid(uid):
    '''
        Check if uid is unique or not
        Args: 
            uid: user id
        Return:
            True if unique, else False
    '''
    cursor.execute(
            """
            SELECT *
            FROM users
            WHERE uid = ?;
            """, (uid,))
    if cursor.fetchone() != None:
        return False
    return True


def register(user_id, name, pwd):
    '''
        Create a new user_id then input the new user to the database
        Args:
            name: the name the user input 
            pwd: the password the user input
        Return:
            None
    '''
    if not check_uid(user_id):
        #raise message not unique
        return False
    #input the user to the database

    cursor.execute(
        """
        INSERT INTO users(uid, name, pwd)
        VALUES (?,?,?);
        """, (user_id, name, pwd))
    connection.commit()
    return True
