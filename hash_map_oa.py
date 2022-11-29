# Name: Andrew Lee
# OSU Email: leea6@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/2/2022
# Description: An implementation of a hash using open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity()*2)
        to_be_put = HashEntry(key, value)
        hash_value = self._hash_function(key)
        hash_value = hash_value % self.get_capacity()
        original_hash = hash_value
        if self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key == key:
            self._buckets[hash_value] = to_be_put
        elif self._buckets[hash_value] == None or self._buckets[hash_value].is_tombstone == True:
            self._buckets[hash_value] = to_be_put
            self._size += 1
        else:
            j = 1
            while self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key != key:
                hash_value = original_hash
                hash_value = (hash_value + j ** 2) % self.get_capacity()
                j += 1
                if self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key == key:
                    self._size -= 1
            self._buckets[hash_value] = to_be_put
            self._size += 1

    def table_load(self) -> float:
        return self.get_size()/self.get_capacity()


    def empty_buckets(self) -> int:
        counter = 0
        for x in range(self._buckets.length()):
            if self._buckets[x] == None or self._buckets[x].is_tombstone == True:
                counter += 1
        return counter

    def resize_table(self, new_capacity: int) -> None:
        if new_capacity < self.get_size():
            return
        else:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)
            old_array = self._buckets
            self._buckets = DynamicArray()
            for x in range(new_capacity):
                self._buckets.append(None)
            self._capacity = new_capacity
            self._size = 0
            for x in range(old_array.length()):
                hash_entry = old_array[x]
                if hash_entry != None and hash_entry.is_tombstone == False:
                    self.put(hash_entry.key, hash_entry.value)

    def get(self, key: str) -> object:
        '''method to return the value associated with the given key. Uses the same logic as our put method to find the
        hash value with the key. '''
        hash_value = self._hash_function(key)
        hash_value = hash_value % self.get_capacity()
        original_hash = hash_value
        if self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key == key:
            return self._buckets[hash_value].value
        elif self._buckets[hash_value] == None or self._buckets[hash_value].is_tombstone == True:
            return None
        else:
            j = 1
            while self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key != key:
                hash_value = original_hash
                hash_value = (hash_value + j ** 2) % self.get_capacity()
                j += 1
            return self._buckets[hash_value].value

    def contains_key(self, key: str) -> bool:
        if self.get_size() == 0:
            return False
        hash_value = self._hash_function(key)
        hash_value = hash_value % self.get_capacity()
        original_hash = hash_value
        if self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key == key:
            return True
        elif self._buckets[hash_value] == None or self._buckets[hash_value].is_tombstone == True:
            return False
        else:
            j = 1
            while self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key != key:
                hash_value = original_hash
                hash_value = (hash_value + j ** 2) % self.get_capacity()
                j += 1
            return True

    def remove(self, key: str) -> None:
        hash_value = self._hash_function(key)
        hash_value = hash_value % self.get_capacity()
        original_hash = hash_value
        if self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key == key:
            self._buckets[hash_value].is_tombstone = True
            self._size -= 1
        elif self._buckets[hash_value] == None or self._buckets[hash_value].is_tombstone == True:
            return
        else:
            j = 1
            while self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key != key:
                hash_value = original_hash
                hash_value = (hash_value + j ** 2) % self.get_capacity()
                j += 1
                #if self._buckets[hash_value] != None and self._buckets[hash_value].is_tombstone == False and self._buckets[hash_value].key == key:
                #    self._size -= 1
            self._buckets[hash_value].is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        self._buckets = DynamicArray()
        for x in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        array_returned = DynamicArray()
        for x in range(self._buckets.length()):
            if self._buckets[x] != None and self._buckets[x].is_tombstone == False:
                array_returned.append((self._buckets[x].key, self._buckets[x].value))
        return array_returned

    def __iter__(self):
        '''__iter__ method that sets an index = 0'''
        self._index = 0
        return self

    def __next__(self):
        '''__next__ method that will raise StopIteration once we get a DynamicArrayException'''
        '''try:
            value = self._da[self._index]
        except DynamicArrayException:
            raise StopIteration'''

        try:
            condition = True
            while condition:
                if self._buckets[self._index] != None and self._buckets[self._index].is_tombstone == False:
                    condition = False
                else:
                    self._index = self._index + 1
            value = self._buckets[self._index]
            self._index += 1
]        except DynamicArrayException:
            raise StopIteration
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    '''
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
        #if i == 14 or i == 15:
            print(i, m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print('--------', i)
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - contains_key example 2") #GIVING PROBLEMS
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
    '''
    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
