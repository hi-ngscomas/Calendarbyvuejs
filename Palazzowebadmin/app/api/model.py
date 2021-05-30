import re
import logging
def getslug(name:str):
    try:
        regex = f'[^\w]'
        name = re.sub(regex, "_", name).lower()
        return name
    except Exception as e:
        logging.error("Thuộc tính tên không thể format thành slug | " + str(e))
        return name

def getname(name:str):
    try:
        return name.rstrip().upper()
    except Exception as e:
        logging.error("Thuộc tính tên không thể format thành getname | " + str(e))
        return name 
