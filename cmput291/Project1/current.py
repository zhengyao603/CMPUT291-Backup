import sqlite3
import sys
import string
import getpass
import random
import time
from datetime import datetime


# defined function for design of login screen
def login_screen(connection, cursor):
    while 1:
        if_registered = input("Have you already have an account (Y/N)?: ")

        # registered users
        if if_registered == 'Y' or if_registered == 'y':
            global email 
            email = input("Please enter your email: ")
            password = getpass.getpass("Please enter your password: ")
            cursor.execute(''' SELECT *
                               FROM users
                               WHERE users.email = ?
                               AND users.pwd = ?;
                           ''', (email, password))
            if_login = cursor.fetchone()
            connection.commit()
            # if password and email does not match
            if not if_login:
                print("")
                print("Invalid email or password! Please try again.\n")
                continue
            print("")
            break

        # unregistered users
        elif if_registered == 'N' or if_registered == 'n':
            email = input("Please enter your email: ")
            name = input("Please enter your name: ")
            city = input("Please enter your city: ")
            gender = input("Please enter your gender (M/F): ")
            password = input("Please enter your password: ")
            print("")
            cursor.execute(''' SELECT *
                               FROM users
                               WHERE users.email = ?;
                           ''', (email,))
            if_successful = cursor.fetchone()
            connection.commit()
            # if email alread existed
            if if_successful:
                print("Error! Email already existed.\n")
                continue
            cursor.execute(''' INSERT INTO users
                               VALUES (?, ?, ?, ?, ?);
                           ''', (email, name, password, city, gender))
            connection.commit()
            break

        elif if_registered == 'Q' or if_registered == 'q':
            sys.exit(0)

        else:
            print("")
            print("Invalid input! Please note that only one character is accepted.\n")
            continue


# defined function for functionality of listing products
def list_products(connection, cursor):
    # sqlite query for finding valid products
    valid_pid = []
    product_query = ''' SELECT pid, descr, num_reviews, avg_rating, num_sales
                        FROM (SELECT products.pid, products.descr, COUNT(sales.sid) as num_sales
                              FROM products, sales
                              WHERE products.pid = sales.pid
                                    AND date('now') <= sales.edate
                              GROUP BY products.pid) 
                              left outer join
                             (SELECT products.pid, COUNT(previews.rid) as num_reviews, AVG(previews.rating) as avg_rating
                              FROM products, previews
                              WHERE products.pid = previews.pid
                              GROUP BY products.pid) using (pid)
                              ORDER BY num_sales DESC;
                    '''
    # print the desired products
    cursor.execute(product_query)
    result1 = cursor.fetchall()
    connection.commit()
    for row in result1:
        print(row)
        valid_pid.append(row[0])

    if len(valid_pid) == 0:
        print("No product is related to active sales!")
        return

    # ask for user input
    while 1:
        print("")
        choice = input('Choose a product to manipulate: ')
        if choice in valid_pid or choice in valid_pid:
            break

    while 1:
        print('\nOptions:\na: Write product review')
        print('b: List all reviews of the product')
        print('c: List all active sales associated to the product\n')
        option = input('Make an option: ')

        if option == 'a' or option == 'A':
            # write product review
            text = input('Please providing your review text: ')
            while 1:
                rating = input('Please providing your rating: ')
                try:
                    int(rating)
                except:
                    print("Error, the rating should be integer! Check again.")
                else:
                    if int(rating) < 1 or int(rating) > 5:
                        print('Error, the rating should be 1~5! Check again.')
                        continue
                    break
            # select all rids
            all_rid = 'select rid from previews'
            cursor.execute(all_rid)
            result2 = cursor.fetchall()
            connection.commit()
            rid_list = []
            for i in result2:
                rid_list.append(i[0])
            # generate a random unqiue rid
            while 1:
                temp_rid = random.randint(0, 100)
                if temp_rid not in rid_list:
                    rid_list.append(temp_rid)
                    break
                continue
            # insert new user comment
            cur_time = time.strftime('%Y-%m-%d', time.localtime())
            insert_preview = '''insert into previews(rid,pid,reviewer,rating,rtext,rdate) VALUES
                                (?,?,?,?,?,?)
                             '''
            cursor.execute(insert_preview, (temp_rid, choice, email, rating, text, cur_time))
            connection.commit()
            break

        elif option == 'b' or option == 'B':
            # list all reviews of products
            cursor.execute('SELECT * FROM previews WHERE pid = ?;',(choice,))
            all_reviews = cursor.fetchall()
            print('Here are the reviews of this product')
            for row in all_reviews:
                print(row)
            break

        elif option == 'c' or option == 'C':
            # list all active sales
            sids_list = []
            active_sale_query = ''' SELECT sid, edate
                                    FROM products p left outer join sales s using (pid)
                                    WHERE date('now') <= edate and pid = ?
                                    ORDER BY edate;
                                '''
            cursor.execute(active_sale_query,(choice,))
            listout = cursor.fetchall()
            connection.commit()

            for i in listout:
                sids_list.append(i[0])
            follow_up(connection, cursor, sids_list)
            break

        else:
            print("")
            print("Invalid input! Please note that only one character is accepted.")
            continue

    print("")


# helper function for sorting sids
def sort_sids(sid):
    return sid[1]


# defined function for functionality of searching sales
def search_sales(connection, cursor):
    keyword = input('Please provide the keywords(e.g keyword1,keyword2): ')
    words = keyword.split(',')
    tempdic = {}
    # query for finding number of existence of certain key words
    result = '''SELECT sid, (ifnull(num_1, 0) + ifnull(num_2, 0)) as total_num
                FROM (SELECT sales.sid, sales.descr, (length(sales.descr) - length(replace(lower(sales.descr), ?, "")))/? as num_1
                      FROM sales
                      WHERE sales.edate >= date('now') AND sales.descr LIKE ?)
                      left outer join
                     (SELECT sales.sid, products.pid, products.descr, (length(products.descr) - length(replace(lower(products.descr), ?, "")))/? as num_2
                      FROM sales, products
                      WHERE sales.edate >= date('now') AND sales.pid = products.pid AND products.descr LIKE ?) using (sid)
                ORDER BY total_num DESC;
            '''
    # find total number of existence of all input key words for certain sale
    for i in words:
        i = i.lower().strip()
        cursor.execute(result,(i, len(i), '%'+i+'%', i, len(i), '%'+i+'%'))
        fetch = cursor.fetchall()
        
        for each_fetch in fetch:
            if each_fetch[0] not in tempdic:
                tempdic[each_fetch[0]] = each_fetch[1]
            else:
                tempdic[each_fetch[0]] = tempdic[each_fetch[0]] + each_fetch[1]
    # order the sales by decreasing order or number of existence of key word
    sids_keys = []
    for key in tempdic.keys():
        sids_keys.append((key, tempdic[key]))
    sids_keys.sort(key = sort_sids, reverse = True)
    sids = []

    for sid in sids_keys:
        sids.append(sid[0])

    # if there is no matching sale
    if len(sids) == 0:
        print("No matching sale!")
        print("")
        return

    follow_up(connection, cursor, sids)


# defined function for functionality of 1-2 follow up
def follow_up(connection, cursor, sids):
    for sid in sids:
        # cursor.execute('''
        #                ''')
        print(sid)
    print("")

    while 1:
        choice = input("Choose a certain sale for detailed information: ")

        if choice not in sids:
            continue
        else:
            # find detailed information of selected sale
            cursor.execute('''SELECT sid, lister, ifnull(num_review, 0), ifnull(avg_rating, 0), descr, edate, cond, ifnull(max_bid, 0), rprice
                              FROM (SELECT sales.sid, sales.lister, sales.descr, sales.edate, sales.cond, sales.rprice
                              FROM sales
                              WHERE sales.sid = ?)
                              left outer join
                             (SELECT reviews.reviewee, COUNT(reviews.reviewer) as num_review, AVG(reviews.rating) as avg_rating
                              FROM reviews
                              GROUP BY reviews.reviewee) on lister = reviewee
                              left outer join
                             (SELECT bids.sid, MAX(bids.amount) as max_bid
                              FROM bids
                              GROUP BY bids.sid) using(sid)
                           ''', (choice,))
            result1 = cursor.fetchall()
            connection.commit()

            # find information of product that is related to the sale(if any)
            cursor.execute(''' SELECT s.sid, p.pid, p.descr, ifnull(count(r.reviewer), 0), ifnull(avg(r.rating), 0)
                               FROM sales s left outer join products p on s.pid = p.pid
                                    left outer join previews r on p.pid = r.pid
                               WHERE s.sid = ? 
                                    ''', (choice,))
            result2 = cursor.fetchall()
            connection.commit()

            print("\nsid|lister|num_review|avg_rating|descr|edate|cond|max_bid/rprice")
            # if there is no bid -> print reserved price, if there is bid -> print max bid
            for i in range(len(result1[0])):
                if i == 7 and result1[0][7] == 0:
                    print(result1[0][8])
                    break
                elif i == 7 and result1[0][7] != 0:
                    print(result1[0][7])
                    break
                print(result1[0][i], end = '|')
            print("")

            # if the sale is related to product, print information of product
            print("pdescr|num_preview|avg_prating/text")
            if not result2:
                pirnt('this sales is not related to a product')
            else:
                print("%s|%s|%s" %(result2[0][2], result2[0][3], result2[0][4]))
            break


    while 1:
        print('\nOptions:\na: Place a bid')
        print('b: List all active sales of seller')
        print('c: List all reviews of seller\n')
        option = input('Make an option: ')

        if option == 'a' or option == 'A':
            # find max bid of current sale
            cursor.execute(''' SELECT ifnull(max(bids.amount), 0) as max_bid, ifnull(sales.rprice, 0)
                               FROM sales left outer join bids using (sid)
                               WHERE sales.sid = ?
                               GROUP BY sales.sid, sales.rprice;
                           ''',(choice,))
            output = cursor.fetchone()
            print(output)
            maxbid = output[0]
            rprice = output[1]

            fflag = 1
            # ask for user bid
            while fflag == 1:
                fflag = 0
                money = input('Please provide the bid amount: ')
                try:
                    float(money)
                except:
                    print('Error, input type must be integer!')
                    fflag = 1
                else:
                    # if there is no bid and there is a reserved price
                    if maxbid == 0 and rprice != 0:
                        if float(money) <= rprice:
                            print('Error, you cannot bid an amount lower than reserved price!')
                            fflag = 1
                    # if there is no bid and there is no reserved price
                    elif maxbid == 0 and rprice == 0:
                        if float(money) <= 0:
                            print('Error, you cannot bid an amount lower than 0!')
                            fflag = 1
                    # if there is bid
                    elif maxbid != 0:
                        if float(money) <= maxbid:
                            print('Error, you cannot bid an amount lower than current bid!')
                            fflag = 1
            print("")

            # generate an unique bid, note B1!=B01
            cursor.execute('select bid from bids')
            result = cursor.fetchall()
            connection.commit()
            bid_list = []
            for i in result:
                bid_list.append(i[0])

            while 1:
                bid_i = random.randint(0, 100)
                bid = 'B' + str(bid_i)
                if bid not in bid_list:
                    bid_list.append(sid)
                    break
                else:
                    continue

            insertt = '''
                        INSERT INTO bids(bid,bidder,sid,bdate,amount) VALUES
                        (?,?,?,?,?);
                    '''

            # insert data into database
            ttime = datetime.now()
            cursor.execute(insertt,(bid,email,choice,ttime,money))
            connection.commit()
            break
        
        elif option == 'b' or option == 'B':
            # find lister of current sale
            cursor.execute('SELECT sales.lister FROM sales WHERE sales.sid = ?', (choice,))
            lister = cursor.fetchone()[0]
            connection.commit()
            # find all active sales of lister
            cursor.execute(''' SELECT sales.sid
                               FROM sales
                               WHERE sales.lister = ?
                                     AND date('now') <= sales.edate
                               ORDER BY sales.edate
                           ''', (lister,))
            result3 = cursor.fetchall()
            connection.commit()
            sub_sids = []
            for sale in result3:
                sub_sids.append(sale[0])
            follow_up(connection, cursor, sub_sids)
            break

        elif option == 'c' or optiion == 'C':
            # find lister of current sale
            cursor.execute('SELECT sales.lister FROM sales WHERE sales.sid = ?', (choice,))
            lister = cursor.fetchone()[0]
            print(lister)
            connection.commit()
            # list all reviews of the lister
            cursor.execute(''' SELECT reviews.reviewer, reviews.reviewee, reviews.rating,
                                      reviews.rtext, reviews.rdate
                               FROM users, reviews
                               WHERE users.email = ?
                                     AND users.email = reviews.reviewee
                           ''', (lister,))
            result4 = cursor.fetchall()
            connection.commit()
            for review in result4:
                print(review)
            break

        else:
            print("")
            print("Invalid input! Please note that only one character is accepted.")
            continue


# defined function for functionality of posting sales
def post_sales(connection, cursor):
    cur_time = datetime.now()
    flag = 1
    pro_id = input('Please provide your product ID(optional): ')
    sale_end1 = input('Please provide a future sale end date and time(e.g. 2020-03-06 20:00): ')
    
    # catch valid inputs
    while flag:
        try:
            date_list = sale_end1.split(' ')[0]
            date_list = date_list.split('-')

            date_list = list(map(int,date_list))
            time_list = sale_end1.split(' ')[1]
            time_list = time_list.split(':')
            time_list = list(map(int,time_list))
            sale_end = datetime(date_list[0],date_list[1],date_list[2],time_list[0],time_list[1])
        except:
            sale_end1 = input('Error, please input the valid date: ')
            flag = 1
        else:
            flag = 0
            if sale_end < cur_time:
                sale_end1 = input('Error, please input the valid date: ')
                flag = 1

    while 1:
        sale_descr = input('Please provide your sale description: ')
        if sale_descr:
            break
    while 1:
        condition = input('Please provide your condition: ')
        if condition:
            break
    reserve = input('Please provide your reservied price(optiolnal): ')
    
    
    # generate a unique sid
    cursor.execute('select sid from sales')
    result = cursor.fetchall()
    connection.commit()
    sid_list = []
    for i in result:
        sid_list.append(i[0])
    while 1:
        sid_i = random.randint(0, 100)
        sid = 's' + str(sid_i)
        if sid not in sid_list:
            sid_list.append(sid)
            break
        else:
            continue

    # insert data into database
    ins = ''' INSERT INTO sales(sid, lister,pid,edate,descr,cond,rprice)
              VALUES (?,?,?,?,?,?,?);'''

    cursor.execute(ins,(sid,email,pro_id,sale_end,sale_descr,condition,reserve))
    connection.commit()
    print("")


# defined function for functionality of searching users
def search_users(connection, cursor):
    valid_user = []
    # find all users relate to the input keyword
    keyword = input("Please enter a keyword: ")
    cursor.execute(''' SELECT users.email, users.name, users.city
                       FROM users
                       WHERE users.email LIKE ?
                             OR users.name LIKE ?
                   ''', ('%' + keyword + '%', '%' + keyword + '%'))
    result1 = cursor.fetchall()
    connection.commit()
    for row in result1:
        print(row)
        valid_user.append(row[0])

    # if there is no matching user
    if len(valid_user) == 0:
        print("No matching user!")
        print("")
        return

    while 1:
        print("")
        choice = input('Choose a user to perform actions: ')
        if choice in valid_user or choice in valid_user:
            break

    while 1:
        print('\nOptions:\na: Write user review')
        print('b: List all active listings of the user')
        print('c: List all reviews of the users\n')
        option = input('Make an option: ')

        if option == 'a' or option == 'A':
            # check if the user already had review on target user
            cursor.execute(''' SELECT *
                               FROM reviews
                               WHERE reviews.reviewer = ? AND reviews.reviewee = ?
                           ''', (email, choice))
            if_reviewed = cursor.fetchone()
            connection.commit()
            if if_reviewed:
                print("You have already reviewed that user.")
                break

            # write user review
            text = input('Please providing your review text: ')
            while 1:
                rating = input('Please providing your rating: ')
                try:
                    int(rating)
                except:
                    print("Error, the rating should be integer! Check again.")
                else:
                    if int(rating) < 1 or int(rating) > 5:
                        print('Error, the rating should be 1~5! Check again.')
                        continue
                    break

            # write the review into database
            cur_time = time.strftime('%Y-%m-%d', time.localtime())
            insert_review = '''insert into reviews(reviewer,reviewee,rating,rtext,rdate) VALUES
                                (?,?,?,?,?)
                             '''
            cursor.execute(insert_review, (email, choice, rating, text, cur_time))
            connection.commit()
            break

        elif option == 'b' or option == 'B':
            # list all active listings of the user
            cursor.execute(''' SELECT sales.sid
                               FROM users, sales
                               WHERE users.email = ?
                                     AND users.email = sales.lister
                                     AND date('now') <= sales.edate
                               ORDER BY sales.edate
                           ''', (choice,))
            result2 = cursor.fetchall()
            connection.commit()
            sids = []
            for sale in result2:
                sids.append(sale[0])
            follow_up(connection, cursor, sids)
            break

        elif option == 'c' or option == 'C':
            # list all reviews of the users
            cursor.execute(''' SELECT reviews.reviewer, reviews.reviewee, reviews.rating,
                                      reviews.rtext, reviews.rdate
                               FROM users, reviews
                               WHERE users.email = ?
                                     AND users.email = reviews.reviewee
                           ''', (choice,))
            result3 = cursor.fetchall()
            connection.commit()
            for review in result3:
                print(review)
            break

        else:
            print("")
            print("Invalid input! Please note that only one character is accepted.")
            continue

    print("")


# main function
def main():
    # Read the name of database
    if len(sys.argv) != 2:
        print("Invalid argument! One command line argument is required")
        sys.exit(0)
    # Connect to the database
    database = str(sys.argv[1])
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("PRAGMA case_sensitive_like=OFF;")
    connection.commit()

    login_screen(connection, cursor)
    print("Login successfully.")
    print("")

    while 1:
        print("For the following possible operations")
        print("Choose which one you want to perform")
        print("1. List products")
        print("2. Search for sales")
        print("3. Post a sale")
        print("4. Search for users")
        print("5. Logout and quit the program\n")
        print("For the certain operation you want to perform", end = ',')
        option = input("input the operation number(1-5): ")
        print("")
        if option == '1':
            list_products(connection, cursor)
            continue

        elif option == '2':
            search_sales(connection, cursor)
            continue

        elif option == '3':
            post_sales(connection, cursor)
            continue

        elif option == '4':
            search_users(connection, cursor)
            continue

        elif option == '5':
            if_sure = input("Are you sure you want to logout? (Y/N): ")
            if if_sure == 'y' or if_sure == 'Y':
                print("Logout successfully.\n")
                break
            else:
                continue

        else:
            print("Invalid input! Please try again.")
            print("Please note that only one single digit input is accepted.\n")
            continue

        connection.close()

main()