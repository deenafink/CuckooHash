import pytest
from cuckoo2 import *
import random

# function to generate random strings of size characters
# taken from homework
def randomString(size):
    ans = ""
    for i in range(size):
        c = chr(random.randint(0,25) + ord('A'))
        ans += c
        
    return ans 

# insert pytests

# test that the inserted keys are still there for a small table without duplicates
def test_stillThere():
    c = cuckooHash(2)
    
    inserted = []
    # insert 50 random strings
    for i in range(50):
        temp = randomString(25)
        data = random.randint(1, 10)
        c.insert(temp, data)     
        inserted.append((temp, data))
    
    # check that they are in the table and the data matches
    for i in range(len(inserted)):
        assert c.find(inserted[i][0]) == inserted[i][1]

# testing that the inserted items are actually in the arrays without the array needing to grow
def test_stillThereNoGrow():
    c = cuckooHash(100)
    
    inserted = []
    for i in range(1):
        temp = randomString(25)
        data = random.randint(1, 10)
        c.insert(temp, data)
        inserted.append((temp, data))
    
    for i in range(len(inserted)):
        # check that the returned key from find is the key that was inserted
        assert c.find(inserted[i][0]) == inserted[i][1] 



# inserting a lot of random keys into a cuckooHash
def test_bigTorture():
    c = cuckooHash(5)
    
    inserted = []
    
    # insert a lot of different strings
    for i in range(10000):
        for i in range(10):
            # make random keys of 25 letters to ensure there's no duplicates
            temp = randomString(25)
            data = random.randint(1, 5)
            # insert the key data pair
            c.insert(temp, data)
            # append it to the list of inserted too
            inserted.append((temp, data))
    
    # for each of the inserted
    for i in range(len(inserted)):
        # make sure that the data found is the same
        assert c.find(inserted[i][0]) == inserted[i][1]

# prove that different data types work the same to be inserted
def test_diffDataTypes():
    
    c = cuckooHash()
    
    # insert data of different types
    c.insert("INT", 7)
    c.insert("STRING", "PEEL")
    c.insert("BOOL", False)
    c.insert("FLOAT", .02)
    
    # check that they are there and that they were inserted correctly
    assert c.find("INT") == 7
    assert c.find("STRING") == "PEEL"
    assert c.find("BOOL") == False
    assert c.find("FLOAT") == .02

# test that when inserting a key that's already there, it overwrites the data
def test_insertAlreadyThere():
    
    c = cuckooHash()
    h = cuckooHash()
    
    # insert into c
    c.insert("HI", 4)
    c.insert("MY", 3)
    c.insert("Name", "FOOBAR")
    c.insert("IS", 7)
    c.insert("DEENA", 800)
    
    # now insert something already inserted
    c.insert("DEENA", 7)    
    
    # insert into h
    h.insert("HELLO", 4)
    h.insert("HELLO", 6)
    
    
    # now check to make sure that the data is the new data and that the key was overwritten
    assert c.find("DEENA") == 7
    assert h.find("HELLO") == 6


# find pytests

# prove that what you found has the right data
def test_findRightData():
    for i in range(10):
        # create a cuckoo hash of a random size
        c = cuckooHash(random.randint(1, 100))
        
        # list to store the inserted keys and data pairs
        inserted = []
        
        # use the insertHelp function that inserts a random number of strings
        insertHelp(c, inserted)
        
        # for each of the inserted keys
        for i in range(len(inserted)):
            # check that find returns the correct data
            assert c.find(inserted[i][0]) == inserted[i][1]

# test finding things that aren't there
def test_findNotThere():
    c = cuckooHash(100)
    c.insert("HI", 5)
    c.insert("LOVE", "HEART")
    
    d = cuckooHash(random.randint(1, 10000))
    d.insert("HI", 4)
    d.insert("MY", 3)
    d.insert("Name", "FOOBAR")
    d.insert("IS", 7)
    d.insert("DEENA", 800)
    
    # check that trying to delete keys that aren't there returns None
    assert d.find("FINK") == None
    assert c.find("LOVES") == None


# delete pytests

# test delete simple
def test_deleteSimple():
    d = cuckooHash()
    
    # insert into d
    d.insert("HI", 5)
    d.insert("J", 4)
    
    # delete it and check it was deleted
    d.delete("HI")
    assert d.find("HI") == None    
    

# delete with a big table and deleting the whole table
def test_deleteBig():
    # make a cuckooHash
    c = cuckooHash(4)
    
    inserted = []
    
    # use the insertHelp function that inserts a random number of strings
    insertHelp(c, inserted)
    
    # delete each key
    for i in range(len(inserted)):
        c.delete(inserted[i][0])
        
    # then make sure that those keys are None and that the number of keys is 0
    for i in range(len(inserted)):
        assert c.find(inserted[i][0]) == None
        assert len(c) == 0    
    

# test deleting things that aren't there
def test_deleteNotThere():
    
    c = cuckooHash(100)
    
    c.insert("HI", 5)
    c.insert("LOVE", "HEART")
    
    # try deleting something not there
    assert c.delete("LOVES") == False
    
    d = cuckooHash(random.randint(1, 10000))
    d.insert("HI", 4)
    d.insert("MY", 3)
    d.insert("Name", "FOOBAR")
    d.insert("IS", 7)
    d.insert("DEENA", 800)
    
    # check that trying to delete keys that aren't there returns false
    assert d.delete("FINK") == False
    

# delete from an empty list
def test_deleteEmpty():
    c = cuckooHash()
    
    assert c.delete("HELLO") == False
    assert c.delete("WORLD") == False

# general pytests

# check that the number of inserted is the same as numKeys
def test_correctNum():
    c = cuckooHash(2)
    size = random.randint(1, 1000)
    
    # insert size number of keys
    for i in range(size):
        temp = randomString(25)
        data = random.randint(1, 10)
        c.insert(temp, data)
    
    assert len(c) == size



# test that inserting the same key with different data doesn't add another to the numKeys
def test_randomLength():
    c = cuckooHash()
    
    c.insert("HI", 5)
    c.insert("HI", 3)
    
    assert len(c) == 1

   
# function to insert a random number of random key data pairs
def insertHelp(cuckoo, inserted):
    # insert random number of strings into each
    for i in range(random.randint(1, 10000)):
        # make big strings to ensure no duplicates
        temp = randomString(25)
        data = random.randint(1, 5)
        cuckoo.insert(temp, data)
        inserted.append((temp, data))


        

pytest.main(["-v", "-s", "test_cuckoo.py"])     