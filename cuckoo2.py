#"I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity policy of the course syllabus and the academic integrity policy of the CS department.”

from BitHash import BitHash
from BitHash import ResetBitHash
import pytest
import random

# Link class with key data pairs
class Link(object):
    def __init__(self, k, d):
        self.key  = k
        self.data = d
    
    # string method returns the key and data
    def __str__(self):
        return (str(self.key) , str(self.data))
     
        
class cuckooHash(object):
    def __init__(self, size = 100):
        
        # raise exception if tries to make a table of anything under 1
        if size < 1:
            raise Exception("Sorry, no numbers below zero") 
        
        # size of the cuckoo hash tables
        self.__size = size
        
        # first array
        self.__cuckooArray = [None] * size
        
        # second array
        self.__secondArray = [None] * size
        
        # how many keys are inserted in the cuckooHash
        self.__numKeys = 0
        
        # store the hash functions
        self.__hashNum = 1
        self.__hashNum2 = 2
    
    # return current number of keys in table    
    def __len__(self): return self.__numKeys
    
    # return what size the tables are currently
    def getCurSize(self):
        return self.__size
    
    # get the current hash functions
    def getHash(self):
        return self.__hashNum, self.__hashNum2
    
    # get all of the already inserted keys and re-insert them into bigger tables
    def grow(self):
        
        # list to store all the keys in the tables
        dataPairs = []
        
        # loop through all the buckets
        for i in range(self.__size):
            # if there is something in the first add it to the list
            if self.__cuckooArray[i]:
                tempK = self.__cuckooArray[i].key
                tempD = self.__cuckooArray[i].data
                dataPairs.append((tempK, tempD))
                
            # if there is something the second add it to the list
            if self.__secondArray[i]:
                tempK = self.__secondArray[i].key
                tempD = self.__secondArray[i].data
                dataPairs.append((tempK, tempD))                
                
        # loop until all of the keys are inserted
        # grows and tries to insert. if can't insert all, grows again
        while True:
            # the new size is double the old size
            newSize = self.__size * 2

            # new tables with newSize
            new1 = [None] * newSize
            new2 = [None] * newSize 
            
            # make the new size the real size
            self.__size = newSize               
            
            # how many keys were inserted
            newNumKeys = 0
            
            # for each of the keys in the list of keys from the og cuckooHash
            for i in range(len(dataPairs)):
                # call insertF with the newly created tables, the key, the data, the two hash functions, and the size of the tables
                # Insert f should return true if inserted, false if not
                if insertF(new1, new2, dataPairs[i][0], dataPairs[i][1], self.__hashNum, self.__hashNum2, self.__size):
                    # if inserted correctly, increment the keys
                    newNumKeys += 1
            
            # stop this loop if the length of inserted keys is the same as there was keys in the cuckooHash going into grow
            if newNumKeys == len(dataPairs):
                break
            
        # make the arrays the new ones
        self.__cuckooArray = new1
        self.__secondArray = new2
        
    
    # private wrapper method for find
    # returns tuple of bucket, l, and which table
    def __findLink(self, k): 
        
        # hash in order to identify the bucket where the key might be in either table
        bucket = BitHash(k, self.__hashNum) % self.__size
        bucket2 = BitHash(k, self.__hashNum2) % self.__size
        
        # l is the link it would be in the first table
        l = self.__cuckooArray[bucket]
        # if the bucket is full and the key matches k, return the bucket, the link, which table
        if l and self.__cuckooArray[bucket].key == k: return bucket, l, 1
        
        # l2 is the link it would be in the second table
        l2 = self.__secondArray[bucket2]
        # if the bucket is full and the key matches k, return the bucket, the link, which table
        if l2 and l2.key == k: return bucket2, l2, 2
        
        # return None if the key can't be found     
        return None, None, None       
    
    # return the data associated with the key k
    # calls wrapper method __findLink()
    def find(self, k):
        bucket, l, table = self.__findLink(k)
        # if it was found, return the data, if not, return none
        if l:
            return l.data
        else:
            return None
        
    def insert(self, k, d):
                   
        # count for loop
        M = 0
        
        # loop at most M times
        while M <= 100:
            # create a new link with k and d
            l = Link(k, d)            
                     
            # hash it, get the position in first table
            pos = BitHash(k, self.__hashNum) % self.__size            
            
            # if the position is empty insert it
            if self.__cuckooArray[pos] is None:
                self.__cuckooArray[pos] = l
                # increment numKeys
                self.__numKeys += 1
                return True
            
            # if key was already there, overwrite the data and don't update numKeys
            if self.__cuckooArray[pos].key == k:
                self.__cuckooArray[pos] = l
                return True
            
            # swap what was in the position with l
            self.__cuckooArray[pos], l = l, self.__cuckooArray[pos]
            
            # now make k and d the key and data of the evicted link
            k = l.key
            d = l.data
            
            # hash where is should be in the second table
            pos = BitHash(k, self.__hashNum2) % self.__size
            
            # if the spot is empty insert it
            if self.__secondArray[pos] is None:
                self.__secondArray[pos] = l
                # increment numKeys
                self.__numKeys += 1
                return True
            
            # if key was already there, overwrite the data and don't update numKeys
            if self.__secondArray[pos].key == k:
                self.__secondArray[pos] = l 
                return True
            
            # swap what was in the position with l
            self.__secondArray[pos], l = l, self.__secondArray[pos]
            # now make k and d the key and data of the evicted link
            k = l.key
            d = l.data
            
            # increment the loop
            M += 1
        
        # if fall out because was looping too many times, resetBitHash and grow the table
        ResetBitHash()
        self.grow()
        
        # now insert by calling insert recursively
        self.insert(k, d) 
    
    
    # delete a key (k) data pair from the cuckooHash
    def delete(self, k):
        
        # find the position it should be in with the first hash
        pos1 = BitHash(k, self.__hashNum) % self.__size
        # find the position it should be in with the second hash
        pos2 = BitHash(k, self.__hashNum2) % self.__size

       
        # if the key is in the first array
        if self.__cuckooArray[pos1]:
            if self.__cuckooArray[pos1].key == k:
                # delete it
                self.__cuckooArray[pos1] = None
                # decrement the number of keys in the table
                self.__numKeys -= 1
                return True
            
        # if the key is in the second array
        if self.__secondArray[pos2]:
            if self.__secondArray[pos2].key == k:
                # delete it
                self.__secondArray[pos2] = None
                # decrement the number of keys in the table
                self.__numKeys -= 1
                return True
        
        # if the key wasn't found, return False, nothing was deleted
        return False    
    
    # print both arrays
    def totalPrint(self):
        print("first          |         second")
        
        # check both arrays at each position
        for i in range(self.__size):
            if self.__cuckooArray[i] and self.__secondArray[i]:
                print(i,  ": ", self.__cuckooArray[i].key, self.__cuckooArray[i].data,  "   ", self.__secondArray[i].key, self.__secondArray[i].data)
             
            # if only in the first  
            elif self.__cuckooArray[i] and not self.__secondArray[i]:
                print(i,  ": ", self.__cuckooArray[i].key, self.__cuckooArray[i].data, "   None")
            
            # if only in the second
            elif self.__secondArray[i] and not self.__cuckooArray[i]:
                print(i, ":  None        ", self.__secondArray[i].key, self.__secondArray[i].data) 
            
            # if both are empty
            else:
                print(i, ": ", "None          ", None)
                
    
# function to use within grow, to insert the key data pairs into new arrays
def insertF(new1, new2, k, d, hash1, hash2, size):
    
    # keep track if the key was inserted successfully
    inserted = False
    # counting how many times go through loop
    limit = 0
    
    # while the key wasn't inserted and haven't reached the limit yet
    while inserted == False and limit < 100:
        # create a new link with the data and key
        l = Link(k, d)        
        # hash the key
        pos = BitHash(k, hash1) % size
        
        # if the position in the first array is empty
        if new1[pos] is None:
            # insert it
            new1[pos] = l
            inserted = True
            return True         
        
        # swap what was in the position with l
        new1[pos], l = l, new1[pos]
        
        # now make k and d the key and data of the evicted link
        k = l.key
        d = l.data
        
        # hash where is should be in the second table
        pos = BitHash(k, hash2) % size
        
        # if the spot is empty put it in
        if new2[pos] is None:
            new2[pos] = l
            inserted = True
            return True    

        # swap what was in the position with l
        new2[pos], l = l, new2[pos]
        
        # now make k and d the key and data of the evicted link
        k = l.key
        d = l.data
        
        limit += 1                  