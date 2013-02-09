import datetime

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

USERNAME_LEN_MIN = 4
USERNAME_LEN_MAX = 25

REALNAME_LEN_MIN = 4
REALNAME_LEN_MAX = 25

PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16


def format_date(d):
    return datetime.datetime.strftime(d, '%H:%M %d %b %Y')
