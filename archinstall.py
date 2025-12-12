import subprocess
from pathlib import Path
import sys

#Path for setup 
PATH_LOCALE = Path("/usr/share/zoneinfo/Europe")
PATH_LOCALE_GEN = Path("/etc/locale.gen")


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
    


def local_language_setup():
    user_locale = str(input("Enter name locale, to cancel, type 'close' here:"))
    if user_locale == 'close':
        return "Locale not selected[-]"

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



def configure_locale_gen():
    user_input = str(input("Select options for locale.gen for example - [en_US.UTF-8], to cancel, type 'close' here:"))

    if user_input.lower() == "close":
        print("Locale gen setup cancelled.")
        return "CANCELLED"

    configure_input = f"#{user_input} UTF-8"
    un_configure_input = f"{user_input} UTF-8"

    try:
        content = PATH_LOCALE_GEN.read_text()
        new_date = None

        if configure_input in content:
            new_date = content.replace(configure_input, un_configure_input)

        elif un_configure_input in content:
            pass

        else:
            print(f"Could not find locale '{user_input}' in {PATH_LOCALE_GEN}.")
            print("Please check the spelling and try again.")
            return configure_locale_gen()
    
        if new_date is not None:
            PATH_LOCALE_GEN.write_text(new_date)
            print(f"File {PATH_LOCALE_GEN} update: add {user_input}.")
        else:
            print(f"Options {user_input} already configured {PATH_LOCALE_GEN}.")

        user_flag = str(input('Would you like to add another locale?[Y/n]')).lower()
        if user_flag == 'y':
            result = configure_locale_gen()
            return result 
        
        return True
    
    
    except FileNotFoundError:
        print(f"Critical error: not found {PATH_LOCALE_GEN}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error: locale-gen: {e.stderr.strip()}")
        return False

def locale_generation():
    print("Starting locale generation (locale-gen)...")
    subprocess.run(["locale-gen"], check=True, text=True, capture_output=True)
    print("Locale generation completed[+]")


res = welcome()    

if res.lower() == 'y':
    #Time zone
    main_user_input = str(input("Do you want to customize locales?[Y/n]:")).lower()
    if main_user_input == 'y':
        local_language_setup()
    else:
        print("Skip setup locales")
    
    
    # setup locale.gen
    main_user_input = (str(input('Want to configure locale.gen?[Y/n]:'))).lower()
    if main_user_input == 'y':
        locale_gen_res = configure_locale_gen()
    
        if locale_gen_res is True:
            locale_generation()
        elif locale_gen_res == "CANCELLED":
            print("Locale configuration cancelled by user.")
        else:
            print("Setup locale-gen failed due to a critical error.")
    else:
        print("Skip setup locales")
    

else:
    print("Script stopped working, Bye")


