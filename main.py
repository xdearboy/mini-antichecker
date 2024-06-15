import random
import string
import flet as ft
import winreg
import os

def generate_random_name(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def main(page: ft.Page):
    page.title = generate_random_name()
    
    def delete_subkeys(registry, key):
        open_key = winreg.OpenKey(registry, key, 0, winreg.KEY_ALL_ACCESS)
        info_key = winreg.QueryInfoKey(open_key)
        for x in range(info_key[0]):
            subkey = winreg.EnumKey(open_key, 0)
            try:
                winreg.DeleteKey(open_key, subkey)
                print(f"Удален подключ: {key}\\{subkey}")
            except OSError:
                delete_subkeys(registry, f"{key}\\{subkey}")
                winreg.DeleteKey(open_key, subkey)
                print(f"Удален подключ: {key}\\{subkey}")
        winreg.CloseKey(open_key)
    
    def clear_registry_path(registry_path):
        try:
            reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            delete_subkeys(reg, registry_path)
            winreg.DeleteKey(reg, registry_path)
            print(f"{registry_path} очищен.")
        except Exception as e:
            print(f"Ошибка при очистке {registry_path}: {e}")

    def clear_shellbags(e):
        shellbags_path = (
            r"Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU"
        )
        clear_registry_path(shellbags_path)
    
    def clear_lastactivityview(e):
        try:
            registry_path = (
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU"
            )
            reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(reg, registry_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteKey(key, "")
            print("LastActivityView очищено.")
        except Exception as e:
            print(f"Ошибка при очистке LastActivityView: {e}")

    def clearpath(e):
        prefetch_path = os.path.expanduser(
            '~\\AppData\\Local\\Microsoft\\Windows\\Prefetch'
        )
        if os.path.exists(prefetch_path):
            try:
                for filename in os.listdir(prefetch_path):
                    if filename.endswith('.pf'):
                        os.remove(os.path.join(prefetch_path, filename))
                print("Префетч очищен.")
            except Exception as e:
                print(f"Ошибка при очистке префахтов: {e}")
        else:
            print(f"Путь {prefetch_path} не найден.")

        recent_path = os.path.expanduser(
            '~\\AppData\\Local\\Microsoft\\Windows\\Explorer\\RecentDocs'
        )
        if os.path.exists(recent_path):
            try:
                for filename in os.listdir(recent_path):
                    if filename.endswith('.exe') or filename.endswith('.dll'):
                        os.remove(os.path.join(recent_path, filename))
                print("Recent очищен.")
            except Exception as e:
                print(f"Ошибка при очистке Recent: {e}")
        else:
            print(f"Путь {recent_path} не найден.")
        
        try:
            downloads_path = os.path.expanduser('~\\Downloads')
            for filename in os.listdir(downloads_path):
                if 'exloader' in filename.lower():
                    os.remove(os.path.join(downloads_path, filename))
            print("Exloader удален.")
        except Exception as e:
            print(f"Ошибка при удалении exloader: {e}")

    page.add(
        ft.Column([
            ft.Text("Очистка следов"),
            ft.ElevatedButton("Очистить Shellbags", on_click=clear_shellbags),
            ft.ElevatedButton("Очистить LastActivityView", on_click=clear_lastactivityview),
            ft.ElevatedButton("Удалить конфиги читов", on_click=clearpath),
        ])
    )

ft.app(target=main)