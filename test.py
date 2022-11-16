# -*- coding: utf-8 -*-

from engine import listing

user_id = '12356'
ls = listing()
ls.new_user(user_id=user_id)

ls.create_id_list(user_id)
print(len(ls.listing_id[user_id])) # 1390

ls.data_search[user_id] = 'Эйнштейн'
ls.create_id_list(user_id)
print(ls.field[user_id], ls.data_search[user_id], len(ls.listing_id[user_id])) #   Эйнштейн 1390


ls.field[user_id] ='autor'
ls.create_id_list(user_id)
print(ls.field[user_id], ls.data_search[user_id], len(ls.listing_id[user_id])) # autor Эйнштейн 21

ls.data_search[user_id] = 'Эйнштейн'
ls.field[user_id] ='all'
ls.create_id_list(user_id)
print(ls.field[user_id], ls.data_search[user_id], len(ls.listing_id[user_id])) # all Марк 26

ls.field[user_id] ='content'
ls.create_id_list(user_id)
print(ls.field[user_id], ls.data_search[user_id], len(ls.listing_id[user_id])) # content Эйнштейн 6

while ls.listing_id[user_id]:
    Id = ls.random_id(user_id)
    _aphorism = ls.print_aphorism_by_id(Id,user_id)
    content = f"{_aphorism['info']}\n <b>--{_aphorism['meta']}--</b>\n{_aphorism['content']}\n\t <i>~{_aphorism['autor']}</i>"

    print(content)
