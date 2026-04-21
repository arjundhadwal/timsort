#!usr/bin/env python3

"""
timsort.py
An algorithm that implements the TimSort method for sorting arrays. 
"""

import time
import math
import random
import matplotlib.pyplot as plt

__author__ = "Arjun Dhadwal"
__version__ = "03-18-26"

class Stack(object): ##Copied from atds.py. Specially modified for Timsort.
    def __init__(self):
        self.list = []

    def push(self, item):
        """
        Adds an item to the end of the stack.
        """
        self.list.append(item)

    def pop(self):
        """
        Removes an item from the end of the stack.
        """
        if len(self.list)>0:
            return self.list.pop()
    
    def peek(self):
        """
        Gets the top item from the stack
        """
        if len(self.list)>0:
            return self.list[-1]
        return None
        
    def peek2(self):
        if len(self.list)>1:
            return self.list[-2]
        return None
        
    def peek3(self):
        if len(self.list)>2:
            return self.list[-3]
        return None
        
    def is_empty(self):
        """
        Returns true if the stack is empty, false otherwise.
        """
        return len(self.list) == 0
    
    def size(self):
        """
        Returns the length of the stack.
        """
        return len(self.list)
    
    def __repr__(self)->str:
        return "Stack"+str(self.list)

def generate_random_numbers(min,max,count):
    arr = []
    for i in range(count):
        arr.append(random.randint(min,max))
    return arr

def calculate_min_run(n): #We worked on this in class during the TimSort lunch. Forked from the GitHub repo. Uses bitwise operations for high speed.
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r
    
def is_sorted(arr)->int: #0 if unsorted, 1 if sorted fwd, 2 if sorted reverse
    if arr[0]>arr[-1]: ##descending
        for i in range(1,len(arr)):
            if arr[i-1]<arr[i]: #if prev. element is smaller than current element.
                return 0
        return 2
    else: #ascending
        for i in range(1, len(arr)):
            if arr[i-1]>arr[i]: #if prev. element is bigger than current element
                return 0
        return 1
    return 0

def insertion_sort(arr:list): #Regular Insertion sort. Slower than binary insertion sort.
    """Uses insertion sort to sort an array"""
    for index in range(1,len(arr)): #loop from 1 to the end
        temp_index = index
        while arr[temp_index]<arr[temp_index-1] and temp_index>0: #out of order and haven't gotten to the end
            arr[temp_index], arr[temp_index-1] = arr[temp_index-1], arr[temp_index] #swap
            temp_index-=1 #go back one space
    return arr

def search(numbers, target): #Binary search implementation.
    low, high = 0, len(numbers) - 1
    while low <= high:
        middle = (low + high) // 2
        if numbers[middle] == target:
            return middle
        elif numbers[middle] < target:
            low = middle + 1 #search in the zone higher
        else:
            high = middle - 1 #search in the zone lower
    return low # type: ignore
    
def binary_insertion_sort(arr:list): #Time complexity of O(nlog(n)) because of the binary search rather than linear search.
    sorte = arr[0:1]
    for index in range(1,len(arr)):
        #print(sorte)
        key = arr[index]
        position = search(sorte,key)
        sorte.insert(position,key)
    return sorte

def merge(left,right):
    GALLOPCT = 5
    arr = [None]*(len(left)+len(right))
    lc = 0
    rc = 0
    ac = 0
    left_wins = 0 ##For galloping. If one array is consistently larger than the other, we can start skipping indices.
    right_wins = 0
    while lc<len(left) and rc<len(right): ##comparing and adding in
        if left[lc] <= right[rc]: #If the left is SMALLER, when galloping we lop on a chunk of the LEFT array
            arr[ac] = left[lc]
            lc+=1
            ac+=1
            left_wins +=1
            right_wins=0
            
            if left_wins>GALLOPCT:
                #we start galloping through the left
                #print("gallop_left")
                key = right[rc]
                new_lc_step = 1
                while lc+new_lc_step<len(left) and left[lc+new_lc_step]<=key:
                    new_lc_step*=2
                low = lc+new_lc_step//2
                high = lc + min(new_lc_step,len(left))
                target_index = lc + search(left[low:high],key) #Add in to account offset.
                """
                for i in range(lc,target_index): #Throwing em on until we hit the target. This is the chunk.
                    arr[ac] = left[i]
                    ac+=1
                    lc+=1
                """
                print("gallopleft")
                print(lc,target_index)
                print(low,high)
                arr[ac:ac+(target_index-lc)] = left[lc:target_index]
                ac += target_index-lc ##amount increased by
                lc = target_index
                

                left_wins = 0
                
        else: #if the right is SMALLER, the left is BIGGER, when galloping we lop on a chunk of the RIGHT array
            arr[ac] = right[rc]
            rc+=1
            ac+=1
            right_wins +=1
            left_wins=0
            
            if right_wins>GALLOPCT:
                #we start galloping through the right
                #print("gallop_right")
                key = left[lc]
                new_rc_step = 1
                while rc+new_rc_step<len(right) and right[rc+new_rc_step]<=key:
                    new_rc_step*=2
                high = rc+min(len(right),new_rc_step)
                low = rc+new_rc_step//2
                target_index = rc + search(right[low:high],left[lc])
                """
                for i in range(rc,target_index): #Throwing em on until we hit the target. This is the chunk.
                    arr[ac] = right[i]
                    ac+=1
                    rc+=1
                right_wins = 0
                """
                print("gallopright")
                print(rc,target_index)
                print(low,high)
                arr[ac:ac+(target_index-rc)] = right[rc:target_index]
                ac += target_index-rc ##amount increased by
                rc = target_index
                right_wins = 0
    while lc<len(left): #appending final items
        arr[ac] = left[lc]
        lc+=1
        ac+=1
    while rc<len(right):
        arr[ac] = right[rc]
        rc+=1
        ac+=1
    return arr

def timsort(arr:list):
    #linear scan to check if sorted
    if is_sorted(arr) == 1:
        return arr
    elif is_sorted(arr) == 2:
        return arr.reverse()
    #Calculating minimum run length
    RUN = calculate_min_run(len(arr))
    #Splitting array into runs of length n
    numberOfRuns = math.ceil(len(arr)/RUN)
    runs_container = Stack() #This is the stack that contains the runs.
    for i in range(numberOfRuns):
        le_run = arr[i*RUN:(i+1)*RUN]
        if is_sorted(le_run) == 1:
            runs_container.push(le_run) #Take advantage of forward sorted runs.
        elif is_sorted(le_run) == 2:
            runs_container.push(le_run.reverse()) #Take advantage of reverse sorted runs.
        else:
            runs_container.push(binary_insertion_sort(le_run)) #Sorts and pushes the run onto the stack
        if runs_container.size()>2 and type(runs_container.peek())==list:
            X,Y,Z = len(runs_container.peek()), len(runs_container.peek2()), len(runs_container.peek3()) # type: ignore
            if Z > X+Y and Y>X: #Checking invariants found on Wikipedia for optimal run merging.
                array = merge(runs_container.peek(), runs_container.peek2())
                runs_container.pop() #Pop the top two and push the merged big one
                runs_container.pop()
                runs_container.push(array)
            else: #When these invariants are violated, merge the Y with the smallest of X or Z (for optimal merge time, it's faster to merge runs of relatively equal size), and then try again.
                if X<=Z: #first one smaller
                    temp = merge(runs_container.peek(),runs_container.peek2())
                    runs_container.pop()
                    runs_container.pop()
                    runs_container.push(temp)
                else: #third one smaller
                    temp = merge(runs_container.peek2(),runs_container.peek3())
                    temp2 = runs_container.peek()
                    for i in range(3):
                        runs_container.pop() #Pops top three
                    runs_container.push(temp) #pushes merge of bottom two
                    runs_container.push(temp2) #pushes original top one, now at the top of the Stack

    while runs_container.size()>2: #Final merging to put all of the runs together.
        X,Y,Z = len(runs_container.peek()), len(runs_container.peek2()), len(runs_container.peek3()) # type: ignore
        if Z > X+Y and Y>X: #Checking invariants found on Wikipedia for optimal run merging.
            array = merge(runs_container.peek(), runs_container.peek2())
            runs_container.pop()
            runs_container.pop()
            runs_container.push(array)
        else:
            if X<=Z: #first one smaller
                temp = merge(runs_container.peek(),runs_container.peek2())
                runs_container.pop()
                runs_container.push(temp)
            else: #third one smaller
                temp = merge(runs_container.peek2(),runs_container.peek3())
                temp2 = runs_container.peek()
                for i in range(2):
                    runs_container.pop()
                runs_container.push(temp)
                runs_container.push(temp2)
    arr2 = merge(runs_container.peek(),runs_container.peek2()) #Final merge
    return arr2

def main():
    randoms = generate_random_numbers(1,100000,40000)
    sorteds = timsort(randoms)
    print(sorteds)
    print(is_sorted(sorteds))

if __name__ == "__main__":
    main()
