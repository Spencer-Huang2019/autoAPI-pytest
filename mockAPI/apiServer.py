from flask import Flask, request, make_response
import json
from mockAPI.dbUtils import database
from mockAPI.logUtils import log

logger = log("./logFile/mockAPI_log.txt")

server = Flask(__name__)  # regard current file as a service

# This is api of register
@server.route("/spencer/api/register", methods = ["POST"])
def registerAPI():
    # get the parameters from request payload
    data = request.get_data()  # get bytes
    json_data = json.loads(data.decode("utf-8"))
    logger.msg("request payload = %s" % (json_data), "info")
    userName = json_data.get("userName")
    password = json_data.get("password")
    logger.msg("userName = %s password = %s" % (userName,password), "info")

    d = {}
    # if userName is missing
    if userName == "" or userName == None:
        d = {
            "status": "fail",
            "errorCode": 2,
            "msg": "UserName missing"
        }
        logger.msg("msg : UserName missing", "debug")

    # if password is missing
    elif password == "" or password == None:
        d = {
            "status": "fail",
            "errorCode": 3,
            "msg": "Password missing"
        }
        logger.msg("msg : Password missing", "debug")
    elif len(userName) <= 20 and len(password) <= 16:
        # connect DB
        conn = database().connect()
        cur = conn.cursor()
        query = "select name from login_user where status = 'ACTIVE'"
        cur.execute(query)
        # get the data from DB
        namelist = cur.fetchall()  # will return tuple
        logger.msg("namelist" + str(namelist), "info")

        # the flag of being found in DB about userName
        find = False
        for userTuple in namelist:
            if userName.upper() == userTuple[0].upper():
                d = {
                        "status":"fail",
                        "errorCode":1,
                        "msg":"User exist"
                    }
                find = True
                logger.msg("msg : User exist", "debug")
                break
        # if user doesn't exist, then need to insert a record into DB
        if not find:
            insert = f"insert into login_user(name, pwd, status) values('{userName}','{password}','ACTIVE')"
            logger.msg("insert = %s" % insert, "info")
            try:
                cur.execute(insert)
                conn.commit()
            except Exception as e:
                d = "Technical error"
                logger.msg("Technical error: %s" %e, "error")
                return make_response(d, 500)
            else:
                d = {
                    "status": "success",
                    "errorCode": 0,
                    "msg": "Succeed to register"
                }
                logger.msg("Succeed to register", "info")
            conn.close()
    else:
        if len(userName) > 20:
            d = {
                "status": "fail",
                "errorCode": 4,
                "msg": "Length of userName exceeds"
            }
        else:
            d = {
                "status": "fail",
                "errorCode": 5,
                "msg": "Length of password exceeds"
            }
    res = make_response(d, 200)
    return res


# This is api of login
@server.route("/spencer/api/login", methods=["POST"])
def loginAPI():
    # get data from request payload
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    userName = json_data.get("userName")
    password = json_data.get("password")

    d = {}
    # if userName or password is missing
    if userName == "" or userName == None:
        d = {
            "status": "fail",
            "errorCode": 2,
            "msg": "UserName missing"
        }
    elif password == "" or password == None:
        d = {
            "status": "fail",
            "errorCode": 3,
            "msg": "Password missing"
        }
    else:
        # connect database
        conn = database().connect()
        cur = conn.cursor()
        # get data from database
        query = "select name, pwd, status from login_user"
        cur.execute(query)
        userlist = cur.fetchall()

        find = False
        for user in userlist:
            # if user exist
            if userName.upper() == user[0].upper():
                # whether user active or not
                if user[2] == 'ACTIVE':
                    # user and pwd assert
                    if user[1] == password:
                        d = {
                            "status": "success",
                            "errorCode": 0,
                            "msg": "Succeed to login"
                        }
                    else:
                        d = {
                            "status": "fail",
                            "errorCode": 1,
                            "msg": "Incorrect password or non-exist userName"
                        }
                else:
                    d = {
                        "status": "fail",
                        "errorCode": 4,
                        "msg": "User is disabled"
                    }
                find = True
                break
        if not find:
            d = {
                "status": "fail",
                "errorCode": 1,
                "msg": "Incorrect password or non-exist userName"
            }
        conn.close()
    res = make_response(d, 200)
    return res
