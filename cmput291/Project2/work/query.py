from bsddb3 import db
import sys
import datetime
import time
import re
import textwrap


def termQuery(query_data, filename):
    query_data = query_data.encode('utf-8')
    database = db.DB()
    database.open(filename)
    cur = database.cursor()
    resultSet = set()
    try:
        data = cur.get(query_data, db.DB_SET)[1].decode('utf-8')
        resultSet.add(int(data))
        while cur.next_dup():
            data = cur.get(db.DB_CURRENT)[1].decode('utf-8')
            resultSet.add(int(data))
    except:
        pass
    database.close()
    return resultSet

def termQuery_start(query_data, filename):
    encodedkey = query_data.encode('utf-8')
    database = db.DB()
    database.open(filename)
    cur = database.cursor()
    resultSet = set()
    try:
        datapair = cur.get(encodedkey, db.DB_SET_RANGE)
        data = datapair[1].decode('utf-8')
        if datapair[0].decode('utf-8').startswith(query_data):
            resultSet.add(int(data))

        while str(cur.next()[0].decode('utf-8')).startswith(query_data):
            data = cur.get(db.DB_CURRENT)[1].decode('utf-8')
            resultSet.add(int(data))
    except:
        pass
    database.close()
    return resultSet

def dateQuery(query_data, filename,cmp):
    encodedkey = query_data.encode('utf-8')
    database = db.DB()
    database.open(filename)
    cur = database.cursor()
    record = cur.next()
    result = set()
    while record:
        index = record[0].decode('utf-8')
        data = record[1].decode('utf-8')
        review_time = float(re.findall(",(\d+),\".*\",\".*\"$", data)[0])
        querytime = time.mktime(datetime.datetime.strptime(query_data, "%Y/%m/%d").timetuple())
        if cmp == '>':
            if review_time > querytime:
                result.add(index)
        else:
            if review_time < querytime:
                result.add(index)
        record = cur.next()
    database.close()
    return result

def priceQuery(query_data, filename,cmp):
    encodedkey = query_data.encode('utf-8')
    database = db.DB()
    database.open(filename)
    cur = database.cursor()
    record = cur.next()
    result = set()
    while record:
        index = record[0].decode('utf-8')
        data = record[1].decode('utf-8')
        review_price = data.split("\"")[2]
        review_price = review_price[review_price.find(',') + 1:review_price.find(',', 1)]

        if review_price != "unknown":
            actualPrice = float(review_price)

            if cmp == '>':
                if actualPrice > float(query_data):
                    result.add(index)
            else:
                if actualPrice < float(query_data):
                    result.add(index)
        record = cur.next()
    database.close()
    return result


def scoreQuery(query_data, filename, compare):
    query_data = query_data.encode('utf-8')
    database = db.DB()
    database.open(filename)
    cur = database.cursor()

    resultSet = set()
    try:
        datapair = cur.get(query_data, db.DB_SET_RANGE)
        data = datapair[1].decode('utf-8')
        currentkey = float(datapair[0].decode('utf-8'))

        if compare == ">":
            if currentkey > float(query_data):
                resultSet.add(int(data))

            while cur.next():
                datapair = cur.get(db.DB_CURRENT)
                data = datapair[1].decode('utf-8')
                currentkey = float(datapair[0].decode('utf-8'))
                if currentkey > float(query_data):
                    resultSet.add(int(data))

        elif compare == "<":
            while cur.prev():
                datapair = cur.get(db.DB_CURRENT)
                data = datapair[1].decode('utf-8')
                currentkey = float(datapair[0].decode('utf-8'))
                if currentkey < float(query_data):
                    resultSet.add(int(data))
    except:
        pass
    database.close()
    return resultSet


def start_query(query):
    result = set()
    words = query.split(" ")

    for word in words:
        if '>' in word or '<' in word:
            continue
        elif ':' in word:
            field = word.split(':')[0]
            data = word.split(':')[1]
            if data.endswith('%'):
                data = data.strip('%')
                if field == 'pterm':
                    if result.__len__() == 0:
                        result = termQuery_start(data, "pt.idx")
                    else:
                        result = result.intersection(termQuery_start(data, "pt.idx"))
                elif field == 'rterm':
                    if result.__len__() == 0:
                        result = termQuery_start(data, "rt.idx")
                    else:
                        result = result.intersection(termQuery_start(data, "rt.idx"))
            else:
                if field == 'pterm':
                    if result.__len__() == 0:
                        result = termQuery_start(data, "pt.idx")
                    else:
                        result = result.intersection(termQuery_start(data, "pt.idx"))

                elif field == 'rterm':
                    if result.__len__() == 0:
                        result = termQuery_start(data, "rt.idx")
                    else:
                        result = result.intersection(termQuery_start(data, "rt.idx"))
        else:
            if word.endswith('%'):
                word = word.strip('%')
                temp = termQuery_start(word, "pt.idx")
                temp = temp.union(termQuery_start(word, "rt.idx"))
                if result.__len__() == 0:
                    result = temp
                else:
                    result = result.intersection(temp)
            else:
                temp = termQuery(word, "pt.idx")
                temp = temp.union(termQuery(word, "rt.idx"))
                result = result.union(temp)
                if result.__len__() == 0:
                    result = temp
                else:
                    result = result.intersection(temp)

    for word in words:
        if ">" in word:
            cmp = ">"
        elif "<" in word:
            cmp = "<"
        else:
            continue

        field = word.split(cmp)[0]
        data = word.split(cmp)[1]

        if field == "score":
            if result.__len__() == 0:
                result = scoreQuery(data, "sc.idx", cmp)
            else:
                result = result.intersection(scoreQuery(data, "sc.idx", cmp))
        elif field == "price":
            if result.__len__() == 0:
                result = priceQuery(data,"rw.idx",cmp)
            else:
                for index in result.copy():
                    record = get_full_data(index)
                    review_price = record.split("\"")[2]
                    review_price = review_price[review_price.find(',') + 1:review_price.find(',', 1)]

                    if review_price == "unknown":
                        result.remove(index)
                    else:
                        actualPrice = float(review_price)
                        if float(data) >= actualPrice:
                            result.remove(index)
        elif field == "date":
            if result.__len__() == 0:
                result = dateQuery(data,'rw.idx',cmp)
            else:
                for index in result.copy():
                    record = get_full_data(index)
                    review_time = float(re.findall(",(\d+),\".*\",\".*\"$", record)[0])
                    querytime = time.mktime(datetime.datetime.strptime(data, "%Y/%m/%d").timetuple())
                    if review_time <= querytime:
                        result.remove(index)
    return result

def deal(s):
    return s.group().replace(' ', '')

def formatQuery(query):
    query = re.sub(r'\s*[<>:=]\s*', deal, query) # get rid of the space
    output = False
    if(query.find('output=full') != -1):
        output = True
        query = query.replace('output=full','')
    elif query.find('output=brief') != -1:
        output = False
        query = query.replace('output=brief', '')
    query = query.strip()
    return query,output

def get_full_data(index):
    database = db.DB()
    database.open("rw.idx")
    rw = database.get(str(index).encode('utf-8'))
    rw = rw.decode('utf-8')
    return rw

def get_brief_data(index):
    database = db.DB()
    database.open('rw.idx')
    rw = database.get(str(index).encode('utf-8'))
    rw = rw.decode('utf-8')
    review_id = rw.split(",")[0]
    product_title = rw.split("\"")[1]
    review_score  = float(re.findall(",(\d+.\d+),\d+,\".*\",\".*\"$", rw)[0])
    return review_id,review_score,product_title

def run():
    q = False
    output = False
    while not q:
        print("Please input the query!")
        query = input("> ")
        if query:
            query,output = formatQuery(query)
            query_ret = start_query(query)
            query_ret = sorted(list(query_ret))

            if output:
                for k,v in enumerate(query_ret):
                    print("review/Id: ",v)
                    print("review/fields: ",get_full_data(v))
                    print('\n')
            else:
                for k,v in enumerate(query_ret):
                    id,score,title = get_brief_data(v)
                    print("review/Id: ",v)
                    print("review/userId: ",id)
                    print("review/score: ",score)
                    print("product/title: ",title)
                    print('\n')

if __name__ == '__main__':
    run()