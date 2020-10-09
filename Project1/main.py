import sqlite3
from sqlite3 import Error


# comment ctrl k + ctrl c
# uncomment ctrl k + ctrl u

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    # finally:
    #    if conn:
    #        conn.close()
    return conn


def create_table(conn, create_table):
    try:
        c = conn.cursor()
        c.execute(create_table)
        conn.commit()
    except Error as e:
        print(e)


def readfile(name):
    try:
        f = open(name, "r")
    except Error as e:
        print(e)
    return f

def insert_into_table( conn , f,cmd, which):
    c=conn.cursor()
    for x in f:
        x=x.strip("\n")
        x = x.replace("'", "")
        x = x.replace(" ","")
        y = x.split(",")

        a=None
        if which=="E":
            x = x.replace("'", "")
            y = x.split(",")
            z = y[5] + ',' + y[6] + ',' + y[7]
            a = (y[0], y[1], y[2], y[3], y[4], z, y[8], int(y[9]), y[10], int(y[11]))
            c.execute(cmd, a)
        else:
            c.execute(cmd,y)

    conn.commit()
def quries(conn):
    c=conn.cursor()
    
    cmd=None
    try:
        print("1.Enter a department name, and retrieve all the names and salaries of all employees who work in that department\n"
              "2.Enter an employee last name and first name and retrieve a list of projects names/hours per week that the employee works on.\n"
              "3.Enter a department name and retrieve the total of all employee salaries who work in the department.\n"
              "4.For each department, retrieve the department name and the number (count) of employees who work in that department. Order the result by number of employees in descending order.\n"
              "5.For each employee who is a supervisor, retrieve the employee first and last name and the number (count) of employees that are supervised. Order the result in descending order.\n"
              )

        cmd=input("Enter the command: ")
        inp=int(cmd)
        if inp==1:
            name=input("Enter Department name: ")
            cmd='''SELECT EMPLOYEE.Fname,EMPLOYEE.Lname,EMPLOYEE.Address
                 FROM EMPLOYEE,DEPARTMENT
                 WHERE Dname=\''''+name+'''\' AND DEPARTMENT.Dnumber=EMPLOYEE.Dno;'''

        elif(inp==2):
            name=input("Enter First Name: ")
            lname=input("Enter Last Name: ")
            cmd='''SELECT P.Pname, W.Hours
                    FROM EMPLOYEE AS E,WORKS_ON AS W, PROJECT AS P
                    WHERE  E.Fname=\''''+name+'''\' AND E.Lname=\''''+lname+'''\' AND E.Ssn= W.Essn  AND W.Pno=P.Pnumber;
                    '''

        elif(inp==3):
            cmd='''SELECT SUM(EMPLOYEE.Salary)
                FROM EMPLOYEE,DEPARTMENT
                WHERE Dno=Dnumber;'''
            print("The total salary working on department is")

        elif(inp==4):
            cmd='''SELECT DEPARTMENT.Dname,COUNT(*)
                    FROM DEPARTMENT,EMPLOYEE
                    WHERE Dno=Dnumber
                    GROUP BY DEPARTMENT.Dnumber
                    ORDER BY COUNT(*) DESC; 
                    '''
        elif(inp==5):
            cmd='''SELECT S.Fname, S.Lname, COUNT(*)
                    FROM EMPLOYEE AS E, EMPLOYEE AS S
                    WHERE E.Super_ssn=S.Ssn
                    GROUP BY S.Ssn
                    ORDER BY COUNT(*) DESC 
                    '''

        if inp>0 and inp<6:
            c.execute(cmd)
            for item in c.fetchall():
                print(item)
    except Error as e:
        print(e)

def main():
    database = r"company.db"
    table_employee = """ CREATE TABLE IF NOT EXISTS EMPLOYEE (
                            Fname       VARCHAR[15]       NOT NULL,
                            Mint        CHAR,
                            Lname       VARCHAR[15]       NOT NULL,
                            Ssn         CHAR(9),
                            Bdate       DATE,
                            Address     VARCHAR[30],
                            Gender      CHAR              NOT NULL,
                            Salary      DECIMAL(10,2),
                            Super_ssn   CHAR(9),
                            Dno         INT               NOT NULL,
                            PRIMARY KEY(SSN)
                            );"""
    # Create Department table
    table_department = ''' CREATE TABLE IF NOT EXISTS DEPARTMENT(
                        Dname           VARCHAR[15]           NOT NULL,
                        Dnumber         INT                   NOT NULL          DEFAULT 1,
                        Mgr_ssn         CHAR(9)               NOT NULL,
                        Mgr_start_date  DATE,
                        PRIMARY KEY(Dnumber),
                        UNIQUE (Dname),
                        FOREIGN KEY(Mgr_ssn) REFERENCES EMPLOYEE(Ssn) ON DELETE SET DEFAULT ON UPDATE CASCADE 
    );'''
    table_department_loacation = ''' CREATE TABLE IF NOT EXISTS DEPT_LOCATIONS(
                                    Dnumber     INT         NOT NULL        DEFAULT 1,
                                    Dlocation   VARCHAR(15) NOT NULL,
                                    PRIMARY KEY(Dnumber,Dlocation),
                                    FOREIGN KEY(Dnumber) REFERENCES DEPARTMENT(Dnumber) ON DELETE CASCADE ON UPDATE CASCADE 
                                    );'''
    table_project='''CREATE TABLE IF NOT EXISTS PROJECT(
                    Pname       VARCHAR(15)     NOT NULL,
                    Pnumber     INT             NOT NULL,
                    Plocation   VARCHAR(15),
                    Dnum        INT             NOT NULL,
                    PRIMARY KEY(Pnumber),
                    UNIQUE (Pname),
                    FOREIGN KEY(Dnum) REFERENCES DEPARTMENT(Dnumber) ON DELETE SET DEFAULT ON UPDATE CASCADE
                    );'''
    table_workson = '''CREATE TABLE IF NOT EXISTS WORKS_ON(
                    Essn        CHAR(9)         NOT NULL,
                    Pno         INT             NOT NULL,
                    Hours       DECIMAL(3,1)    NOT NULL,
                    PRIMARY KEY(Essn,Pno),
                    FOREIGN KEY(Essn) REFERENCES EMPLOYEE(Ssn) ON DELETE SET DEFAULT ON UPDATE CASCADE,
                    FOREIGN KEY(Pno) REFERENCES PROJECT(Pnumber) ON DELETE CASCADE ON UPDATE CASCADE 
                    );'''

    # create a dababase connection
    conn = create_connection(database)

    # check for error
    if conn is not None:
        # create table
        create_table(conn, table_employee)
        create_table(conn, table_department)
        create_table(conn, table_department_loacation)
        create_table(conn, table_project)
        create_table(conn, table_workson)
    else:
        print("Error! cannot create the database connection")
    employee_file = "EMPLOYEE.txt"
    depat_file="DEPARTMENT.TXT"
    dep_loc_file="DEPT_LOCATIONS.txt"
    work_file="WORKS_ON.txt"
    proj_file="PROJECT.txt"
    employeecmd = '''INSERT or IGNORE INTO  EMPLOYEE (Fname,Mint,Lname,Ssn,Bdate,Address,Gender,Salary,Super_ssn,Dno) 
                VALUES(?,?,?,?,?,?,?,?,?,?)'''
    departmentcmd='''INSERT or IGNORE INTO DEPARTMENT (Dname,Dnumber,Mgr_ssn,Mgr_start_date) VALUES(?,?,?,?)'''
    department_loc_cmd='''INSERT or IGNORE INTO DEPT_LOCATIONS (Dnumber, Dlocation) VALUES(?,?)'''
    workcmd='''INSERT or IGNORE INTO WORKS_ON (Essn,Pno,Hours) VALUES (?,?,?)'''
    projectcmd='''INSERT OR IGNORE INTO PROJECT(Pname,Pnumber,Plocation,Dnum) VALUES (?,?,?,?)'''
    f = readfile(employee_file)
    if f is not None:
        insert_into_table(conn,f,employeecmd,"E")
    f=readfile(depat_file)
    if f is not None:
        insert_into_table(conn,f,departmentcmd,"D")
    f=readfile(dep_loc_file)
    if f is not None:
        insert_into_table(conn,f,department_loc_cmd,None)
    f=readfile(work_file)
    if f is not None:
        insert_into_table(conn,f,workcmd,None)
    f=readfile(proj_file)
    if f is not None:
        insert_into_table(conn,f,projectcmd,None)
    quries(conn)
if __name__ == '__main__':
    main()