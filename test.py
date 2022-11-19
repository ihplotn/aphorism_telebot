# -*- coding: utf-8 -*-

from engine import listing

user_id = '0000'
ls = listing()
ls.new_users(user_id=user_id)
print(1, ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) # 2

ls.create_id_list(user_id)
print(2, ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) # 3896

ls.search_parameters(user_id, search_data='Эйнштейн')
ls.create_id_list(user_id)
print(3, ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) #   Эйнштейн  3896

ls.search_parameters(user_id, field='autor')
ls.create_id_list(user_id)
print(4, ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) # autor Эйнштейн 221

ls.search_parameters(user_id, field='all', search_data="'2")
ls.create_id_list(user_id)
print(5,ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id']))# all 2

ls.search_parameters(user_id, field='content', search_data='люб"овь')
ls.create_id_list(user_id)
print(6, ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) # content Слово 21

while ls.users[user_id]['listing_id']:
    Id = ls.random_id(user_id)
    content = ls.print_aphorism_by_id(Id,user_id)
    print(content)
