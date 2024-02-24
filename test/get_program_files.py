import winreg

def get_installed_programs():
    # インストールされているプログラムのリストを保持する辞書
    programs = {}

    # レジストリのパス
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    # レジストリを開く
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)

    # レジストリ内のプログラム情報を取得
    i = 0
    while True:
        try:
            # サブキー（プログラム）の名前を取得
            subkey_name = winreg.EnumKey(reg_key, i)
            subkey_path = reg_path + "\\" + subkey_name
            subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            
            # プログラム名とインストールパスを取得
            try:
                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                path = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                if name and path:
                    programs[name] = path
            except FileNotFoundError:
                pass

            i += 1
        except WindowsError:
            break

    return programs

# インストールされているプログラムの名前とパスを表示
installed_programs = get_installed_programs()
for name, path in installed_programs.items():
    print(f"{name}: {path}")