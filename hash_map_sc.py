# Name: Andrew Lee
# OSU Email: leea6@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/2/2022
# Description: An implementation of a hash using chaining to deal with collisions


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        '''method that takes given key and value, computes a hash value with the given key, and adds it to the hash map
        via linked list. If the given key is the same as a key already in the hash, replaces it. Also, resizes the map
        if the load is too high '''
        if self.table_load() >= 1:
            self.resize_table(self.get_capacity()*2)
        hash_value = self._hash_function(key)
        hash_value = hash_value % self.get_capacity()
        if self._buckets[hash_value].contains(key):                     #removes key if its a duplicate
            self._buckets[hash_value].remove(key)
            self._size -= 1
        self._buckets[hash_value].insert(key,value)
        self._size += 1

    def empty_buckets(self) -> int:
        '''method to calculate how many empty buckets there are in the map'''
        counter = 0
        for x in range(self._buckets.length()):
            if self._buckets[x].length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        '''method to calculate the table load of the map'''
        return self.get_size()/self.get_capacity()

    def clear(self) -> None:
        '''method to clear the map by creating a whole new DynamicArray'''
        self._buckets = DynamicArray()
        for x in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        '''method to resize the table to the given new_capacity. Does nothing if the new_capacity < 1. If the given
        new_capacity is not a prime number, we call ._next_prime'''
        if new_capacity < 1:
            return
        elif new_capacity >= 1:
            if not self._is_prime(new_capacity):                        #calc new prime if necessary
                new_capacity = self._next_prime(new_capacity)
            old_array = self._buckets                                   #pointer to current array to transfer later
            self._buckets = DynamicArray()                              #create our new DA
            for x in range(new_capacity):
                self._buckets.append(LinkedList())
            self._capacity = new_capacity                               #make sure capacity and size are correct
            self._size = 0
            #counter = 0
            for x in range(old_array.length()):                         #for loop to put every value in old to new
                key_and_value = old_array.pop()
                for x in key_and_value:
                    self.put(x.key, x.value)
                    #counter += 1

    def get(self, key: str):
        '''method to return the associated value with the given key. Return nothing if there is nothing associated'''
        hash_value = self._hash_function(key)
        hash_value = hash_value % self.get_capacity()
        to_return = self._buckets[hash_value].contains(key)
        if to_return != None:
            return to_return.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        '''method returns a boolean if the given key is in the map'''
        hash_value = self._hash_function(key)
        hash_value = hash_value % self.get_capacity()
        if self._buckets[hash_value].contains(key) != None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        '''method removes the value associated with the given key'''
        hash_value = self._hash_function(key)
        hash_value = hash_value % self.get_capacity()
        outcome = self._buckets[hash_value].remove(key)                 #subtract one from size if we do remove
        if outcome:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        '''method returns a DA of tuples of all the keys and values in the hash'''
        array_return = DynamicArray()
        for x in range(self._buckets.length()):
            for y in self._buckets[x]:
                array_return.append((y.key, y.value))
        return array_return

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    '''method takes a given DA and returns a tuple of all the modes and then the frequency. Uses hashes to achieve
    O(n). Uses the element in the given DA as the key and sets as the value how many of the element are in the hash
    map.'''
    map = HashMap()
    for x in range(da.length()):
        if map.contains_key(str(da[x])):                  #if element in hash, put it with a value of +1
            map.put(str(da[x]), map.get(str(da[x]))+1)
        else:                                             #if element not in hash, put it in with a value of 1 freq
            map.put(str(da[x]), 1)
    frequency = 0
    hashed_map = map.get_keys_and_values()
    for x in range(hashed_map.length()):                  #go through our hashed map and append the modes to new array
        if hashed_map[x][1] > frequency:
            array_return = DynamicArray()
            array_return.append(hashed_map[x][0])
            frequency = hashed_map[x][1]
        elif hashed_map[x][1] == frequency:
            array_return.append(hashed_map[x][0])
    return (array_return, frequency)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    '''
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    
    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    
    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)
    
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())
    '''
    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
