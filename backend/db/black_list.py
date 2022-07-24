def init_blacklist_file():
    """
    Создает файл blacklist
    """
    open('blacklist_db.txt', 'a').close()
    return True


def add_blacklist_token(token):
    """
    Добавляет токен в blacklist
    """
    with open('blacklist_db.txt', 'a') as file:
        file.write(f'{token},')
    return True


def is_token_blacklisted(token):
    """
    Проверяет есть ли он в файле
    """
    with open('blacklist_db.txt') as file:
        content = file.read()
        array = content[:-1].split(',')
        for value in array:
            if value == token:
                return True

    return False
