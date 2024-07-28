import re

from yandex_music import Client, TracksList


def sanitize_filename(filename: str) -> str:
    """Функция предназначена для очистки названий музыкальных композиций от недопустимых спецсимволов."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def download_tracks(playlist_info_in_func: TracksList,
                    number_of_tracks_in_func: int,
                    start_track_in_func: int = 0,
                    finish_track_in_func: int | None = None):
    """Функция проверяет, доступен ли для скачивания трек из плейлиста "Мне нравится", и если доступен - то
    скачивает в mp3 формате, а если нет - то сообщает об этом в терминале и сохраняет данные этого трека в
    список 'not_available_tracks', а его номер в 'not_available_tracks_numbers', после чего скачивание продолжается."""

    not_available_tracks = []  # Сюда добавляются недоступные для скачивания треки.
    not_available_tracks_numbers = []  # А сюда их номер в плейлисте

    # Перебор всех треков из плейлиста через цикл:
    for track_number in range(number_of_tracks_in_func)[start_track_in_func:finish_track_in_func]:
        full_info_about_track = playlist_info_in_func[track_number].fetch_track()  # Выделение инфы о конкретном треке.
        available = full_info_about_track['available']  # Выделение параметра доступа для скачивания конкретного трека.
        title = full_info_about_track['title']  # Выделение названия конкретного трека (загрязнено пагубными силами).
        sanitized_title = sanitize_filename(title)  # Очищение огнем названия конкретного трека от нечестивых знаков.
        print(f'Скачивание {track_number + 1}-го трека. Название: \"{title}\"')

        # Если доступ есть - скачивается, если нет - добавляется в список недоступных.
        if available:
            full_info_about_track.download(f'{track_number + 1}. {sanitized_title}.mp3')
        else:
            not_available_tracks.append(full_info_about_track)
            not_available_tracks_numbers.append(track_number + 1)
            print(f'Ошибка! В доступе отказано! Переход к следующему треку.')

    # Если есть недоступные, то выводится список и их названиями и номерами, а так же создается текстовый файл с
    # подробной информацией о каждом недоступном треке:
    if not_available_tracks:
        create_txt_file(not_available_tracks, not_available_tracks_numbers)

    print(f'\nСкачивание треков из плейлиста \"Мне нравится\" завершено.')


def create_txt_file(not_available_tracks: list, not_available_tracks_numbers: list):
    """Функция предназначена для создания текстового файла, в котором сохраняются словари с данными о недоступных
     для скачивания треков. Бывает полезно, если надо разобраться, почему что-то не получается скачать."""
    print(f'\nВ доступе было отказано в следующих треках:')
    # Перебор циклом недоступных для скачивания треков для вывода в терминал и записи в файл:
    for k in range(len(not_available_tracks)):
        # Вывод в терминале списка названий и номеров в плейлисте недоступных треков:
        print(f'Недоступен {not_available_tracks_numbers[k]}-й трек: \"{not_available_tracks[k]['title']}\"')
        # Создание текстового файла с данными по недоступным трекам:
        with open("not_available_tracks.txt", "a", encoding="utf-8") as file:
            file.write(f'{not_available_tracks_numbers[k]}. {not_available_tracks[k]}\n\n')


def counting_tracks_for_download(number_of_tracks_in_func, start_track_in_func, finish_track_in_func):
    """Подсчет количества выбранных для скачивания треков"""
    if finish_track_in_func:
        return finish_track_in_func - start_track_in_func
    else:
        return number_of_tracks_in_func - start_track_in_func


def print_info_about_playlist(number_of_tracks_in_func):
    """Вывод информации о количестве треков в плейлисте "Мне нравится"."""
    if number_of_tracks_in_func == 0:
        print('Плейлист \"Мне нравится\" пуст!')
    elif str(number_of_tracks_in_func)[-1] == '1':
        print(f'Плейлист \"Мне нравится\" содержит {number_of_tracks_in_func} трек.')
    elif str(number_of_tracks_in_func)[-1] in ['2', '3', '4']:
        print(f'Плейлист \"Мне нравится\" содержит {number_of_tracks_in_func} трека.')
    else:
        print(f'Плейлист \"Мне нравится\" содержит {number_of_tracks_in_func} треков.')


def notifications_start_download(count_for_download_in_func, start_track_in_func):
    """Уведомление о начале скачивания."""
    if str(count_for_download_in_func)[-1] == '1':
        print(f'Начата загрузка {count_for_download_in_func} трека из плейлиста \"Мне нравится\", '
              f'начиная с {start_track_in_func + 1}-го и '
              f'заканчивая {start_track_in_func + count_for_download_in_func}-м.\n')
    else:
        print(f'Начата загрузка {count_for_download_in_func} треков из плейлиста \"Мне нравится\" '
              f'начиная с {start_track_in_func + 1}-го и '
              f'заканчивая {start_track_in_func + count_for_download_in_func}-м.\n')


if __name__ == '__main__':
    # Базовые переменные:
    start_track: int = 0  # Начать скачивание с трека номер 'start_track' в плейлисте "Мне нравится" (первый это 0).
    finish_track: int | None = None  # Окончить скачивание треком номер 'finish_track' в плейлисте "Мне нравится".
    token: str = ''  # Вставьте токен, он должен быть строкой (т.е. в кавычках).

    # Проверка, на то, что токен не был забыт.
    if not token:
        raise Exception('Токен не был указан. Вставьте свой яндекс токен в переменную token (строка 63).')

    # Подключение к серверам Яндекс Музыки и получение информации по плейлисту "Мне нравится":
    print(f'Подключение к серверам Яндекс Музыки по токену \"{token}\".')
    client = Client(token).init()  # Авторизация по токену.
    print('Получение информации по плейлисту \"Мне нравится\".')
    playlist_info = client.users_likes_tracks()  # Получение информации по плейлисту.
    number_of_tracks = len(playlist_info)  # Подсчет числа треков в плейлисте.

    # Подсчет количества выбранных для скачивания треков:
    count_for_download = counting_tracks_for_download(number_of_tracks, start_track, finish_track)

    # Вывод информации о количестве треков в плейлисте:
    print_info_about_playlist(number_of_tracks)

    # Проверка на то, что были выбраны треки для скачивания:
    if count_for_download != 0:
        # Уведомление о начале скачивания треков:
        notifications_start_download(count_for_download, start_track)
        # Вызов функции скачивания:
        download_tracks(playlist_info, number_of_tracks, start_track, finish_track)
    else:
        print('Очередь на скачивание треков пуста! Скрипт досрочно завершил свою работу.')
