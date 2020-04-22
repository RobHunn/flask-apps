from datetime import datetime

def helper_date(date):
    d = datetime.strptime(str(date['entry_date']),'%Y%m%d')
    return d