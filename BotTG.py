import asyncio
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram import types
import database_afishe as db
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
admins = [540929323,]

def send_photo_to_vk(caption, source=None, group_id=None):
    import vk_api
    from BotVk import vk_with_api
    from vk_api.utils import get_random_id
    upload = vk_api.VkUpload(vk_with_api)
    photo = upload.photo_messages(('/home/tehnokrat/PythonProjects/Posters/poster_TG.jpg'
                                    if not source else "/home/tehnokrat/PythonProjects/Posters/poster_from_group.jpg"))
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk_with_api.messages.send(chat_id=4, message=caption, random_id=get_random_id(), attachment=attachment)


async def give_new_poster(loop):
    asyncio.ensure_future(main())
    while True:
        file = open("/home/tehnokrat/PythonProjects/url.txt", "r")
        url = file.readlines()
        file.close()
        if url:
            file = open("/home/tehnokrat/PythonProjects/url.txt", "w")
            await bot.send_photo(540929323, photo=types.InputFile("/home/tehnokrat/PythonProjects/Posters/afisha.jpg"), caption=db.get_poster()[2])
            await bot.send_photo(chat_id=-1001772576895, caption=db.get_poster()[2],
                                 photo=types.InputFile("/home/tehnokrat/PythonProjects/Posters/afisha.jpg"))
            file.writelines("")
            file.close()
        groups = db.get_groups()
        #print(groups)   
        if groups:
            for group in groups:
                if group[5] == False and group[3]:
                    print(group)
                    input_file = types.InputFile(("/home/tehnokrat/PythonProjects/Posters/poster_from_group.jpg" if group[4] else '/home/tehnokrat/Pictures/Easter_EGG.png'))
                    if len(str(group[3])) > 1024:
                        await bot.send_message(chat_id=-1001772576895, text=group[3])
                        await bot.send_photo(chat_id=-1001772576895, photo=input_file) 
                    else:
                        await bot.send_photo(chat_id=-1001772576895, caption=group[3], photo=input_file)
                    db.set_group(group_id=group[0], domain=group[1], last_post_id=group[2], post_text=group[3], photo_attachments_url=group[4], is_published=True)
        await asyncio.sleep(3)


async def main():
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("add_my_vk_group", "Добавить группу ВК для постоянной проверки на новую афишу"),
    ])

    class Form(StatesGroup):
        link_to_group = State()
        link_to_photo = State()
        send_to_moderation = State()

    @dp.message_handler(commands=['add_my_vk_group'])
    async def add_band(message: types.Message):
        if message.chat.id in admins:
            await Form.link_to_group.set()
            await message.answer('Снова привет, укажите краткую ссылку группы вк')
        else:
            await message.answer('Прости, но мы решили отключить эту функцию для всех. Чтобы пользовавться этой функцией напиши @tehnokratgod')

    @dp.message_handler(commands=['start'], state="*")
    async def start(message: types.Message):
        print(message.chat.id)
        await message.answer("Дарова, это бот который собирает афишу в одном месте для вашего удобства. \n"
                             "Команда /start вызывает это сообщение \n"
                             "Команда /add_my_vk_group добавляет группу в ВК для постоянной проверки на новую афишу. "
                             "\n\n "
                             "Чтобы добавить новую афишу, вам требуется написать #афиша и свой текст, добавить "
                             "фотографию афиши, например:")
        try:
            text = db.get_poster()[2]
        except:
            text = "#афиша\nНовый концерт!\nЖдем всех!"
        await message.answer_photo(caption=text, photo=types.InputFile('/home/tehnokrat/PythonProjects/Posters/poster_TG.jpg'))
        await asyncio.sleep(0.2)
        await message.answer('При этом в беседе ВК "Гиги Архив"(https://vk.me/join/AJQ1dwt1thv1/NzRg32loLYG)'
                             ' и канале ТГ (https://t.me/GigsArchive) появится отправленная вами афиша')

    @dp.message_handler(content_types=[types.ContentType.PHOTO])
    async def new_poster(message):
        if "#афиша" in str(message.caption):
            print(message)
            print("send_to_moderation")
            keyboard = types.InlineKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
            button_OK = types.InlineKeyboardButton(text="OK", callback_data="OK")
            button_NOT_OK = types.InlineKeyboardButton(text="Not OK", callback_data=f"NOT/{message.chat.id}")
            keyboard.add(button_OK) 
            keyboard.add(button_NOT_OK)
            frw_message = await bot.forward_message(chat_id=540929323, from_chat_id=message.chat.id, message_id=message.message_id)
            await frw_message.reply(f"Оцените последнее от @{message.chat.username} (id: {message.chat.id}):", reply_markup=keyboard)

    @dp.callback_query_handler()
    async def inline_query(inline: types.InlineQuery):
        if inline.data == "OK":
            print(inline.message.message_id)
            message = await bot.forward_message(chat_id=-1001772576895, from_chat_id=inline.message.chat.id, message_id=int(inline.message.message_id - 1))
            await message.photo[-1].download("/home/tehnokrat/PythonProjects/Posters/poster_TG.jpg")
            callback = " OK"
            send_photo_to_vk(message.caption)
            db.set_poster("TG", picture_url=str(message.photo[-1]), text=message.caption)
        else:
            chat_id = str(inline.data).split("/")[1]
            callback = " NOT OK"
            await bot.send_message(chat_id=chat_id, text="Ваша заявка была отклонена. Не злоупотребляйте этой функцией.")
        await inline.answer()
        await bot.edit_message_reply_markup(chat_id=inline.from_user.id, message_id=inline.message.message_id, reply_markup=None)
        await bot.edit_message_text(chat_id=inline.from_user.id, message_id=inline.message.message_id,text=str(inline.message.text)+callback)

    @dp.message_handler(commands='cancel', state='*')
    @dp.message_handler(Text(equals=['cancel', 'отмена'], ignore_case=True), state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return
        logging.info('Cancelling state %r', current_state)
        await state.finish()

        await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

    @dp.message_handler(state=Form.link_to_group)
    async def process_link_to_group(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['link_to_group'] = message.text

        await Form.next()
        await message.reply('Теперь отправьте ссылку на любую фотографию из вашего сообщества в вк\n'
                            'ДЛЯ ОТМЕНЫ отправьте команду /cancel')

    @dp.message_handler(state=Form.link_to_photo)
    async def process_link_to_photo(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['link_to_photo'] = message.text

        link = str(data['link_to_group']).split('com/')[1]
        id_group = int(str(data['link_to_photo']).split('photo')[1].split('_')[0])

        if db.get_groups(group_id=id_group):
            await message.answer(f"Кто-то уже добавил эту группу. Как только в {md.bold(link)} появятся новые записи,"
                                 " они сразу же будут отправлены в канал и беседу :-)")
            return

        db.set_group(group_id=id_group, domain=link)

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Отлично! Группа в ВК:', md.bold(link)),
                md.text('id группы:', md.code(id_group)),
                md.text("Данные уже занесены в базу данных"),
                sep='\n',
            ),
            parse_mode=types.ParseMode.MARKDOWN,
        )
        await state.finish()

    await dp.start_polling()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    token = "token"

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    logger.info("Starting bot")

    storage = MemoryStorage()
    bot = Bot(token=token)
    dp = Dispatcher(bot, storage=storage)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(give_new_poster(loop))
