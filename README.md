# Gigi_Archive
## Telegram + VK + Parser(VK wall) bot on python
Used aiogram, vk, vk_api

### Whole project consists of three parts
* #### [BotTG](../main/BotTG.py) - working on VK API. Collect messages from users with mark #афиша (#Poster)
* #### [BotVK](../main/BotVk.py) - working on Telegram API. Collect messages from users with mark #афиша (#Poster), send this messages to telegram channel, get base commands
* #### [VK groups parser](../main/parsing_groups.py) - working on VK API. Collect new posts from group's wall, send them to database.
_____________________________________________

#### [BotVK](../main/BotVk.py)
- With longpool getting events, check if it is messages with photo or wall objects and is message with mark.
When the message passed all this exams bot send post to database and then BotTG send it to telegram channel.
#### [BotTG](../main/BotTG.py)
- Bot based on AioGram. Checking new messages from user, if message have mark #Poster send it to Telegram channel and send message to Vk 
(check function __send_photo_to_vk__ in _[BotTG](../main/BotTG.py)_). To download photo to message first of all bot needs to upload it to VK server ( also in __send_photo_to_vk__) 
#### [VK groups parser](../main/parsing_groups.py)
- Based on VK. To parse groups in VK you need to _[register application](https://vk.com/editapp?act=create)_. Then to parse group you need to get __domain__ and __group_id__. This two arguments parser gets from _[BotTG](../main/BotTG.py)_ (check function __process_link_to_group()__ and __process_link_to_photo()__)

Hosting on Local computer (old notebook with linux elementary OS on it). 
Takes about 500 mb of RAM. 
