import subprocess
from pathlib import Path

def welcome():
    print('Welcome to the basic Arch Linux setup script!')
    welcome_message = """
    #########################################################
    #                                                       #
    #            SCRIPT INSTALL ARCH LINUX                  #
    #                                                       #
    #########################################################
    """
    print(welcome_message)
        
    input_welcome = str(input("This script will help you configure Arch. Do you want to continue?[Y/n]:"))

    return input_welcome
    

PATH_LOCALE = Path("/usr/share/zoneinfo/Europe")

def local_language_setup():
    user_locale = str(input("Enter name locale, to cancel, type 'close' here:"))
    if user_locale == 'close':
        return "Locale not selected"

    full_path = PATH_LOCALE / user_locale
    print(type(full_path))
    print(f'Search {user_locale} locale in {PATH_LOCALE}...')

    if full_path.is_file():
        try:
            source_path = str(full_path)
            target_path = "/etc/localtime"
            subprocess.run(["ln", "-sf", source_path, target_path], check=True, text=True, capture_output=True)
            print(f'The hourly search has been successfully configured[+]')

            subprocess.run(["hwclock","--systohc", "--utc"], check=True, text=True, capture_output=True)
            print('hwclock setup[+]')

            return user_locale
            
        except subprocess.CalledProcessError as e:
            print(f"Critical error during setup: {e.stderr.decode()}")
            return "System error during setup"
    else:
        print("Locale not found.Try again")
        return local_language_setup()

res = welcome()

if res == "Y" or res == "y":
    user_input = str(input("Do you want to customize locales?[Y/n]:"))
    if user_input == "Y" or user_input == "y":
        local_language_setup()
    
else:
    print("Script stopped working, Bye")


