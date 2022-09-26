import random
import string

username_admin_login_page = "user"
password_admin_login_page = "bitnami"


def get_userdata(long=10, letters=True, digits=False, simbols=False):
    strings = (string.ascii_letters if letters else "") + \
              (string.digits if digits else "") + \
              (string.punctuation if simbols else "")
    return "".join(random.choice(strings) for x in range(long))


def get_email(long=10, letters=True, digits=False, simbols=False):
    strings = (string.ascii_letters if letters else "") + \
              (string.digits if digits else "") + \
              (string.punctuation if simbols else "")
    return "".join(random.choice(strings) for x in range(long)) + "@mail.ru"
