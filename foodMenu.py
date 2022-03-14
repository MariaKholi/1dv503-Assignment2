# Programming Assignment2 by Maria Kholi 
# the name of this project: Food Menu

import mysql.connector as mysql
from mysql.connector import errorcode
import datetime

# mysql connection
cnx = mysql.connect(host="localhost",user="root",password="root")

DB_NAME = 'foodStore'
mycursor = cnx.cursor()

#creating a new DB with name foodStore
def create_database(cursor, DB_NAME): 
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print('{} created'.format(DB_NAME))
    except mysql.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# connecting to foodStore DB
def connect_to_db(DB_NAME):
    try:
        mycursor.execute("USE {}".format(DB_NAME))
        print('connecting to {}'.format(DB_NAME))
    except mysql.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(mycursor, DB_NAME)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)


# creating the table food which the owner can use to entre the data of his items
def create_table_food(cursor):
    try:
        cursor.execute("CREATE TABLE Food (foodid INT NOT NULL AUTO_INCREMENT,\
            category_name VARCHAR(255) NOT NULL,\
            price INT(10) NOT NULL,\
            food_name VARCHAR(255) NOT NULL UNIQUE,\
            PRIMARY KEY (foodid))")

        print('Food_table has been created')

    except mysql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Food_table already exists.")
        else:
            print(err.msg)

# creating the table sale which the customer can use to entre the data of the purshase
def create_table_sale(cursor):
    try:
        cursor.execute("CREATE TABLE Sale (saleid INT NOT NULL AUTO_INCREMENT,\
            customer VARCHAR(255),\
            quantity INT(10),\
            total_price INT(10),\
            date_of_sale datetime,\
            PRIMARY KEY (saleid))")
        print('Sale_table has been created')
    except mysql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Sale_table already exists.")
        else:
            print(err.msg)

# creating a table of the customer purchase details
def create_table_sale_detail(cursor):
    try:
        cursor.execute("CREATE TABLE Sale_detail (detailid INT NOT NULL AUTO_INCREMENT,\
            saleid INT NOT NULL,\
            foodid  INT NOT NULL,\
            quantity INT(10),\
            PRIMARY KEY (detailid),\
            FOREIGN KEY (saleid) REFERENCES Sale(saleid),\
            FOREIGN KEY (foodid) REFERENCES Food(foodid))")
        print('Sale_detail_table has been created')
    except mysql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Sale_detail_table already exists.")
        else:
            print(err.msg)

# add some data to the DB to to create a list for the customer
def some_dummy_list_of_food(cursor):
    try:
        # using replace so that the list does not deplicate itself
        foodSql = "REPLACE INTO Food (`category_name`, `price`, `food_name` ) VALUES ('Fruits', 5, 'Apple'), ('Vegetables', 6, 'Tomato'), ('Meat', 12, 'Chicken')"

        cursor.execute(foodSql)
       
        cnx.commit()
       
        print('dummy-Menu List has been created')
    except:
        print('dummy list Exist already')

def manage_choices(cursor):
    choose = 0
    while not choose:
        print("Select one of the Options : ")
        print(" press 1 : Loggin as Admin")
        print(" press 2 : Loggin as Customer")
        print(" press 3 : Show the menu of food")
        choice = int(input("Enter your choice:"))

        if choice == 1:
            insert_foodlists(cursor)

        if choice == 2:
            purchase_food(cursor)

        if choice == 3:
            show_menu(cursor)

def show_menu(cursor):
    cursor.execute('select food_name, price from Food')
    menu = cursor.fetchall()
    print('--------Our products--------')
    print ("{:<8} {:<10}".format('Product','Price (kr)'))
    for x in menu:
        print ("{:<8} {:<10}".format('------','------'))
        print ("{:<8} {:<10}".format(x[0],x[1]))
    print('---------------------------')

def show_list_for_admin(cursor):
    cursor.execute('select * from Food')
    menu = cursor.fetchall()
    print('--------Food list--------')
    print ("{:<8} {:<10} {:<15} {:<15}".format('ID', 'Category','Product','Price (kr)'))
    for x in menu:
        print ("{:<8} {:<10} {:<15} {:<15}".format('------','------', '------', '------'))
        print ("{:<8} {:<10} {:<15} {:<15}".format(x[0], x[1], x[2], x[3]))
    print('---------------------------')

# the admin of the store can add more food lists
def insert_foodlists(cursor):
    password = input('Enter the password please: ')
    choose = 0
    if password == 'Admin':
        while not choose:
            print(" press 1 : Add an item to the list")
            print(" Press 2 : Update the list")
            print(" Press 3 : Return to the main Menu")
            print(" Press 4 : Show the list")
            print(" Print 5 : Show purchase information")
            choice = int(input("Enter your choice:"))

            if choice == 1:
                try:
                    category_name = input('Enter a category name (Fruits, Vegetables, Meat, etc.): ')
                    food_name = input('Enter the food_name: ')
                    price = int(input('Enter the food price: '))
                    sql = "INSERT INTO Food (`category_name`, `price`, `food_name` ) VALUES (%s,%s,%s)"
                    values = (category_name, price, food_name)
                    cursor.execute(sql, values)
                    cnx.commit()
                    print('*** a new item has been successfully added to the list ***')
                    
                except:
                    print("Something went Wrong! could not add ")

            elif choice == 2:
                try:
                    Id = input("Enter the id to update food menu: ")
                    food_name = input("Enter the updated food name: ")
                    category_name = input('Enter the updated category name: ')
                    price = int(input("Enter updated price: "))
                    query = """update Food set category_name='%s', price='%s', food_name='%s' where foodid='%s'"""
                    cursor.execute(query%(category_name, price, food_name, Id))
                    cnx.commit()
                    print(' *** Your list has been updated ***')
                except mysql.Error as err:
                     print(err.msg)
            elif choice == 3:
                manage_choices(cursor)

            elif choice == 4:
                show_list_for_admin(cursor)
            elif choice == 5:
                show_purchase_list(cursor)
    
    

def sending_order(cursor, name):
    food_name = input("Enter the name of the product: ") 
    customer = name 
   
    
    try:
       
        # defining the query if food_name exist in the table or not
        cursor.execute('SELECT foodid, price FROM Food WHERE food_name=%s', (food_name,))
        product = cursor.fetchall()

        if product:
            quantity = input("How many {}s would you like to buy?: ".format(food_name))
            #Calculate the total price
            price = int(product[0][1])
            total_price = int(quantity)*price
            
            #INSERT INTO Sale
            insert_query = 'INSERT INTO Sale (`customer`, `total_price`, `quantity`, `date_of_sale`) VALUES (%s, %s, %s, %s) '
            
            cursor.execute(insert_query, (customer, total_price, quantity, datetime.datetime.now()))
            
            #Fetch last inserted id
            purchaseid = cursor.lastrowid
            
            #INSERT data INTO Sale_Detail
            insert_query = 'INSERT INTO Sale_detail (`saleid`, `foodid`, `quantity`) VALUES (%s, %s, %s) '
            
            cursor.execute(insert_query, (purchaseid, product[0][0], quantity))
            cnx.commit()
                
            print("Your order has been sent successfully")
            print('You have ordered {} {}'.format(quantity, food_name))
            print('To pay: {} kr'.format(total_price))
         
        else:
            print('Foodname does not exist in DB')

    except mysql.Error as err:
        print(err.msg)

# managing the purchase for the customer
def purchase_food(cursor):
    name = input('Enter your name please:')
    print('*** WELCOME {}, choose something from our store: ***'.format(name))

    try:
        show_menu(cursor)
        print('Please add food to your basket! ')
        sending_order(cursor, name)
        
        choice = input('Do you want to continue your purshase (Y/N): ')
        if choice == 'Y' or choice == 'y':
            print('Please add food to your basket! ')
            sending_order(cursor, name)
        elif choice == 'N' or choice == 'n':
            manage_choices(cursor)

    except Exception as e:
        print("status:FAILURE")
        print(e)

# showing the sale lists if the user is Admin
def show_purchase_list(cursor):

    sql = "SELECT Sale.customer, Sale.total_price, Sale_detail.foodid from Sale INNER JOIN Sale_detail ON Sale.saleid = Sale_detail.saleid;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print('--------Purchase list--------')
    print ("{:<8} {:<10} {:<15}".format('Name','Food-ID','Price(kr)'))
    for x in result:
        print ("{:<8} {:<10} {:<15}".format('------','------', '------'))
        print ("{:<8} {:<10} {:<15}".format(x[0], x[1], x[2]))

connect_to_db(DB_NAME)
create_table_food(mycursor)
create_table_sale(mycursor)
create_table_sale_detail(mycursor)
some_dummy_list_of_food(mycursor)
manage_choices(mycursor)

mycursor.close()
cnx.close()