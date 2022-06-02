from vk_photos import Vk_class
photos_count = int(input('Введите количество фото для загрузки: '))
vk_user = Vk_class(count=photos_count)
vk_user.get_photos()
