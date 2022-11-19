# -*- coding: utf-8 -*-

from engine import listing

user_id = '0000'
ls = listing()
ls.new_users(user_id=user_id)

ls.create_id_list(user_id)
print(ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) # 1390

ls.users[user_id]['search_data'] = 'Эйнштейн'
ls.create_id_list(user_id)
print(ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) #   Эйнштейн 1390


ls.users[user_id]['field'] ='autor'
ls.create_id_list(user_id)
print(ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) # autor Эйнштейн 221


ls.users[user_id]['field'] ='all'
ls.create_id_list(user_id)
print(ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id']))# all Эйнштейн 223

ls.users[user_id]['search_data'] = 'Слово'
ls.users[user_id]['field'] ='content'
ls.create_id_list(user_id)
print(ls.users[user_id]['field'], ls.users[user_id]['search_data'], len(ls.users[user_id]['listing_id'])) # content Слово 21

while ls.users[user_id]['listing_id']:
    Id = ls.random_id(user_id)
    content = ls.print_aphorism_by_id(Id,user_id)
    print(content)
