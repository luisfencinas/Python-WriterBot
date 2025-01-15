'''
Author: Luis Fernando Encinas
File: writer_bot_ht.py
Purpose: Breakdown a file into a number of prefixes and it's suffixes.
        hashing these prefixes and putting suffixes into matching location in
        list. Then randomly picking a number of words based off of first prefix
        and picking next word from prefix in hashtable, changing prefix to include
        that word and repeat until it hits an end or produces all words. 
'''
import random
import sys
random.seed(8)
class Hashtable:
    '''
        an object housing a list the size of 'size',
        where we will then hash keys and implement the
        given value. Also being able to return said value
        if asked for or can just check if inside.
    '''
    def __init__(self,size):
        self._pairs = [None] * size
        self._size = size

    def _hash(self, key):
        p = 0
        for c in key:
            p = 31*p + ord(c)
        return p % self._size
    
    def put(self, key, value):
        '''
            takes in key and value, hashes key with hash
            method and then places in list, decrementing by 1
            if already taken. if already there, adds to list, if 
            empty, creates list, containing key and a list of value. 
        '''
        key_hash = self._hash(key)
        placed = False
        while placed != True:
            if self._pairs[key_hash] == None:
                self._pairs[key_hash] = [key, [value]]
                placed = True
            elif self._pairs[key_hash][0] == key:
                self._pairs[key_hash][1].append(value)
                placed = True
            else:
                key_hash -= 1
    
    def get(self, key):
        '''
            looks through list and finds key, returning 
            value list, in this case our suffixes. 
        '''
        for all in range(len(self._pairs)):
            if self._pairs[all] != None: 
                if key == self._pairs[all][0]:
                    return  self._pairs[all][1]
        return None
    
    def contains(self, key):
        '''
            Similar to get, but instead provides true of false
            depending on if it is contained in list. Taking in 
            key to do so. 
        '''
        for all in range(len(self._pairs)):
            if self._pairs[all] != None: 
                if key == self._pairs[all][0]:
                    return  True
        return False

    def __str__(self):
        return str(self._pairs)
    

def main():
    '''
        main function which serves the purpose of 
        getting inputs, ensures prefix size and 
        word count is greater then 1. Then goes 
        through file, gets all words, gets prefixes and 
        suffixes while inserting them into hashtable. Then 
        randomly choosing words after the first prefix amount.
        Either until we hit a dead end or meet word count.
    '''
    file_source = input()
    size_of_hash_table = int(input())
    prefix_size = int(input())
    if prefix_size < 1:
        print('ERROR: specified prefix size is less than one')
        sys.exit(0)
    words_to_be_generated = int(input())
    if words_to_be_generated < 1:
        print('ERROR: specified size of the generated text is less than one')
        sys.exit(0)
    hashtable = Hashtable(size_of_hash_table)
    file_access = open(file_source, 'r')
    file_lines = file_access.readlines()
    # gets prefix ammount for nonword then goes through and 
    # splits lines, appending each word within those lines. 
    all_words = ['@'] * prefix_size
    for lines in file_lines:
        words = lines.strip()
        words = words.split()
        for word in words:
            all_words.append(word)
    # goes through from beggining of nonword, and goes by one changing up 
    # prefix to get all suffixes.
    pos = 0
    while pos + prefix_size < len(all_words):
        current_pre_fix = ' '.join(all_words[pos:pos + prefix_size])
        hashtable.put(current_pre_fix, all_words[pos + prefix_size])
        pos += 1
    pos = prefix_size
    current_prefix_info = all_words[pos:pos + prefix_size]
    all_random_words = []
    # adds beginning words
    for word in current_prefix_info:
        all_random_words.append(word)
    no_suffix = False
    word_count = prefix_size
    pos = 0
    # Then begins to add words until either dead end or we meet count.
    while no_suffix != True and word_count < words_to_be_generated:
        current_prefix_data = all_random_words[pos: pos + prefix_size]
        curr_prefix = ' '.join(current_prefix_data)
        if hashtable.contains(curr_prefix) == False:
            no_suffix = True
        elif hashtable.get(curr_prefix) == None:
            no_suffix = True
        else:
            possible_suffix = hashtable.get(curr_prefix)
            if len(possible_suffix) == 1:
                all_random_words.append(possible_suffix[0])
            else:
                all_random_words.append(possible_suffix[random.randint(0, len(possible_suffix) - 1)])
        pos += 1
        word_count += 1
    # Prints words in increments of 10 until can 
    # either done or no longer greater then 10, 
    # in which we then print the last words. 
    while len(all_random_words) > 10:
        print(' '.join(all_random_words[0:10]))
        all_random_words = all_random_words[10:]
    print(' '.join(all_random_words))

main()

    