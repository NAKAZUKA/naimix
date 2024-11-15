import configparser

config = configparser.ConfigParser()


def read_file(file='settings.ini'):
    global config
    config.read(file)
    # return SETTINGS


def get(section, key):
    global config
    return config.get(section, key)


def GET(KEY):
    KEY = KEY.lower()
    global config
    k = get_ALL()[KEY]
    try:
        if str(float(k)) == k:
            return float(k)
    except:
        pass
    try:
        if str(int(k)) == k:
            return int(k)
    except:
        pass
    try:
        if k == 'True':
            return True
        elif k == 'False':
            return False
    except:
        pass
    return k.encode('cp1251').decode('utf-8')


def get_main():
    global config
    return config.defaults()


def get_sections_name():
    global config
    return config.sections()


def get_section(section):
    global config
    p = {}
    k = config.options(section)
    for i in k:
        p[i] = config.get(section, i)
    return p


def get_ALL():
    global config
    # print(get_main())
    p = get_main()['section']
    p = get_section(p)
    return p


read_file()
# print(get_main())
# print(get_section('Set'))
# print(get_ALL())
