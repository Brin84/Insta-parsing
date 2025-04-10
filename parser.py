import instaloader
import os


def login_instagram():
    """Авторизация в Instagram и сохранение сессии"""
    loader = instaloader.Instaloader(dirname_pattern='data/output', download_pictures=False, download_videos=False)

    username = input("Введите ваш Instagram логин: ")
    password = input("Введите ваш Instagram пароль: ")

    try:
        loader.login(username, password)
        print("[✓] Успешный вход в аккаунт.")

        loader.save_session_to_file()
        return loader
    except Exception as e:
        print(f"[!] Ошибка входа: {e}")
        return None

def get_followers(loader, target_username):
    """Получение списка подписчиков """
    print(f"[~] профиль {target_username}...")
    profile = instaloader.Profile.from_username(loader.context, target_username)

    print(f"[~] Сбор подписчиков... Всего подписчиков: {profile.followers}")

    followers = profile.get_followers()
    usernames = [follower.username for follower in followers]

    print(f"[✓] Собрано логинов: {len(usernames)}")
    return usernames


if __name__ == "__main__":
    print("=== Instagram ===")

    loader = instaloader.Instaloader(dirname_pattern='data/output', download_pictures=False, download_videos=False)

    if os.path.exists("SESSION"):
        print("[~] Используется сохранённая сессия.")
        loader.load_session_from_file()
    else:
        loader = login_instagram()
        if not loader:
            exit()

    target = input("Введите username аккаунта для сбора подписчиков: ")
    usernames = get_followers(loader, target)

    # Сохраняем список
    with open("data/output/followers_list.txt", "w", encoding="utf-8") as f:
        for u in usernames:
            f.write(f"{u}\n")

    print("[✓] Логины сохранены в data/output/followers_list.txt")