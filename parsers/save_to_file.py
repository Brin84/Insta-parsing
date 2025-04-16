import pandas as pd
import os


def save_single_profile_to_excel(profile_data, filename="single_profile.xlsx"):
    os.makedirs("data/output", exist_ok=True)
    file_path = f"data/output/{filename}"

    if os.path.exists(file_path):
        df_old = pd.read_excel(file_path)
    else:
        df_old = pd.DataFrame()

    df_new = pd.DataFrame([profile_data])

    if not df_old.empty and profile_data["username"] in df_old["username"].values:
        print(f"⚠️ Профиль {profile_data['username']} уже есть в файле — пропущен.")
        return

    df_all = pd.concat([df_old, df_new], ignore_index=True)

    columns = [
        "username", "full_name", "bio", "external_url", "followers",
        "following", "posts", "is_private", "email", "phone", "profile_url"
    ]
    df_all = df_all[columns]
    df_all.to_excel(file_path, index=False)
    print(f"✅ Профиль добавлен в {file_path}")