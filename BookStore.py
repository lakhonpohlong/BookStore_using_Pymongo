import pymongo
import warnings
warnings.filterwarnings("ignore")

conn = myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn["bookstore"]
book_coll = db['books']
counter = db['counters']
author = db['authors']
publisher = db['publishers']

# initialising  the sequence_value
if counter.count() == 0:  # if no document found in counter collection then insert one else no need to insert
    counter.insert_one({
        '_id': 'bid',
        'sequence_value': 0})


# auto increment _id in the books collection
def getNextSequence(name):
    return counter.find_and_modify(query={'_id': name}, update={'$inc': {'sequence_value': 1}}, new=True).get(
        'sequence_value')


# author collection
data1 = {
    'author_id': 1001,
    'name': "Dr. APJ Abdul Kalam",
    'address': "New Delhi,India",
}
data2 = {
    'author_id': 1003,
    'name': "Khushwan Singh",
    'address': "Rajkot,Punjab,India",
}
if author.count() == 0:
    author.insert_one(data1)
    author.insert_one(data2)

# publisher collection
data1 = {
    'publisher_id':100,
    'pname': "O'Reilly Media",
    'location': "New Delhi,India",
}
data2 = {
    'publisher_id':101,
    'pname': "McGraw-Hill Education",
    'location': "Noida, Uttar Pradesh",
}
if publisher.count() == 0:
    publisher.insert_one(data1)
    publisher.insert_one(data2)

def alreadyExists(newID):
    doc = book_coll.find_one({'_id':  newID})
    return bool(doc)


def alreadyExistAid(newID):
    doc = author.find_one({'author_id':  newID})
    return bool(doc)


def alreadyExistPid(newID):
    doc = publisher.find_one({'publisher_id':  newID})
    return bool(doc)


def isNotBlank(mystr):
    if mystr and mystr.strip():
        return True
    else:
        return False

def disppart():
    for i in book_coll.find():
        tup=tuple(i)
        print("{:<5}{:<20}".format(*tup).title())
        print("{:<5}{:<20}".format(i['_id'], i['title']))

def addbook():

    try:
        print("\nAdding book to the bookstore")
        name = input('Book Title: ')
        isbn = input("ISBN: ")
        price = input("Price: ")
        edition = input('which Edition: ')
        dop = input('Date of Publishing: ')
        tag = input('Tag: ')
        qtty = input("Quantity: ")
        pid = input('PublisherID(Check from publishers collection): ')
        aid = input('AuthorID(Check from authors collection: ')

        for i in db.publishers.find({'publisher_id': pid}, {'publisher_id': 1}):
            pid = format(i['publisher_id'])

        for i in db.authors.find({'author_id': aid}, {'author_id': 1}):
            aid = format(i['author_id'])

        if isNotBlank(pid):
            pid = int(pid)
        if isNotBlank(qtty):
            qtty = int(qtty)
        if isNotBlank(price):
            price = int(price)
        if isNotBlank(aid):
            aid = int(aid)


        data = {
            '_id': getNextSequence("bid"),
            'title': name,
            'isbn': isbn,
            'price': price,
            'edition': edition + " Edition",
            'date_of_publish': dop,
            'tag': tag,
            'quantity': qtty,
            'publisher_id': pid,
            'author_id': aid
        }
        if isNotBlank(name) and isNotBlank(isbn) and isNotBlank(edition) and alreadyExistAid(aid) and alreadyExistPid(pid):
            db.books.insert_one(data)
            print("\nbook inserted successfully.")
        else:
            print("Either field is left blank or incompatible data or publisher_id/author_id is not correct!")

    except Exception as e:
        print(str(e))



def modifybook():
    inputid = input("Enter book id you which to modify: ")
    if isNotBlank(inputid):
        searchbook(inputid)
        try:
            inputid = int(inputid)
            if alreadyExists(inputid):
                print("\nModifying book from the bookstore")
                print("If you don't want to update any field just skip or press ENTER key from the keyboard.")
                name = input('Book Title: ')
                isbn = input("ISBN: ")
                price = input("Price: ")
                edition = input('which Edition: ')
                dop = input('Date of Publishing: ')
                tag = input('Tag: ')
                qtty = input("Quantity: ")


                if isNotBlank(name):
                    book_coll.update_one({'_id': inputid}, {'$set': {"title": name}})
                if isNotBlank(isbn):
                    book_coll.update_one({'_id': inputid}, {'$set': {"isbn": isbn}})
                if isNotBlank(price):
                    price = int(price)
                    book_coll.update_one({'_id': inputid}, {'$set': {"price": price}})
                if isNotBlank(edition):
                    book_coll.update_one({'_id': inputid}, {'$set': {"edition": edition+" Edition"}})
                if isNotBlank(dop):
                    book_coll.update_one({'_id': inputid}, {'$set': {"date_of_publish": dop}})
                if isNotBlank(tag):
                    book_coll.update_one({'_id': inputid}, {'$set': {"tag": tag}})
                if isNotBlank(qtty):
                    qtty = int(qtty)
                    book_coll.update_one({'_id': inputid}, {'$set': {"quantity": qtty}})
                print("SUCCESS: Field or field updated successfully!")
        except Exception as e:
            print(str(e))
    else:
        print("id is not entered")

def searchbook(ids):
    dash = '-' * 140

    if isNotBlank(ids):
        ids = int(ids)

        if alreadyExists(ids):
            for i in book_coll.find({'_id': ids}).limit(1):
                tup = i
                list(tup)
                print("Record found!")
                print(dash)
                print('{:7}{:35}{:10}{:10}{:15}{:18}{:12}{:10}{:14}{:11}'.format(*tup).title())
                print(dash)
                print('{:<7}{:<35}{:<10}{:<10}{:<15}{:<18}{:<12}{:<10}{:<14}{:<11}'.format(i.get("_id"),
                                                                                           i.get("title"),
                                                                                           i.get("isbn"),
                                                                                           i.get("price"),
                                                                                           i.get("edition"),
                                                                                           i.get("date_of_publish"),
                                                                                           i.get("tag"),
                                                                                           i.get("quantity"),
                                                                                           i.get("publisher_id"),
                                                                                           i.get("author_id")))
                print(dash)
        else:
            print("Record is not found!")
    else:
        print("id is not entered")

def deleterecord():
    print("Deleting record from bookstore")
    disppart()
    newID=input("Enter the book id you want to delete: ")
    if isNotBlank(newID):
        searchbook(newID)
        newID = int(newID)
        if alreadyExists(newID):
            confirm = (input(
                "Are you sure to delete record from bookstore?\nPress d to delete record or abort deletion by pressing ENTER key: "))

            if confirm == "d":
                book_coll.remove({'_id': newID})
                print("Record Deleted..!")
            else:
                return
        else:
            print("Record is not found!")
    else:
        print("id is not entered")


def disp(result):
    dash = '-' * 140
    for i in result:
        tup = i
        list(tup)
        print(dash)
        print('{:7}{:35}{:10}{:10}{:15}{:18}{:12}{:10}{:14}{:11}'.format(*tup).title())
        print(dash)
        break
    for i in book_coll.find({}):
        print('{:<7}{:<35}{:<10}{:<10}{:<15}{:<18}{:<12}{:<10}{:<14}{:<11}'.format(i.get("_id"),
                                                                                  i.get("title"),
                                                                                  i.get("isbn"),
                                                                                  i.get("price"),
                                                                                  i.get("edition"),
                                                                                  i.get("date_of_publish"),
                                                                                  i.get("tag"),
                                                                                  i.get("quantity"),
                                                                                  i.get("publisher_id"),
                                                                                  i.get("author_id")))
        print(dash)


if __name__ == '__main__':

    while True:
        results = db.books.find()
        size = 80
        multidash = '*' * size
        sdash = '*'
        mycom = "ABC Book Store  Application by Lakhon Pohlong"
        print("\n\n")
        print(multidash)
        print("{:<1}{:^78}{:>1}".format(sdash,mycom,sdash))
        print(multidash)
        print("{:<2}{:<77}{:>1}".format(sdash, "Please select the task you want to perform:", sdash))
        print("{:<79}{:>1}".format(sdash, sdash))
        print("{:<20}{:<59}{:>1}".format(sdash, "I. Insert the book:", sdash))
        print("{:<20}{:<59}{:>1}".format(sdash, "M. Modifying existing book", sdash))
        print("{:<20}{:<59}{:>1}".format(sdash, "S. Search for book from the bookstore", sdash))
        print("{:<20}{:<59}{:>1}".format(sdash, "D. Remove Existing book", sdash))
        print("{:<20}{:<59}{:>1}".format(sdash, "V. View all Record", sdash))
        print("{:<79}{:>1}".format(sdash, sdash))
        print(multidash)
        action = input("Enter selection and then press ENTER key: ").upper()
        if action not in "IMSDV" or len(action) != 1:
            print("Invalid choice")
            continue
        if action == 'I':
            addbook()
        elif action == 'M':
            modifybook()
        elif action == 'S':
            query = input("Enter the book id: ")
            searchbook(query)
        elif action == "D":
            deleterecord()
        elif action == 'V':
            disp(results)
