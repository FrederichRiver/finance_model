#!/usr/bin/python3

# 静态方法，产生生成器

def get_sh_stock_list(prefix=0):
    if prefix == 1:
        pf = '0'
    else:
        pf = 'SH'
    stock_list = (f"{pf}60{str(i).zfill(4)}" for i in range(4000))
    return stock_list

def get_sz_stock_list(prefix=0):
    if prefix == 1:
        pf = '1'
    else:
        pf = 'SZ'
    stock_list = (f"{pf}{str(i).zfill(6)}" for i in range(1, 1000))
    return stock_list

def get_cyb_stock_list(prefix=0):
    if prefix == 1:
        pf = '1'
    else:
        pf = 'SZ'
    stock_list = (f"{pf}300{str(i).zfill(3)}" for i in range(1, 1000))
    return stock_list

def get_zxb_stock_list(prefix=0):
    if prefix == 1:
        pf = '0'
    else:
        pf = 'SZ'
    stock_list = (f"{pf}002{str(i).zfill(3)}" for i in range(1, 1000))
    return stock_list

def get_b_stock_list(prefix=0):
    import itertools
    if prefix == 1:
        pf1 = '0'
        pf2 = '1'
    else:
        pf1 = 'SH'
        pf2 = 'SZ'
    s1 = (f"{pf1}900{str(i).zfill(3)}" for i in range(1, 1000))
    s2 = (f"{pf2}200{str(i).zfill(3)}" for i in range(1, 1000))
    stock_list = itertools.chain(s1, s2)
    return stock_list

def get_index_list(prefix=0):
    import itertools
    if prefix == 1:
        pf1 = '0'
        pf2 = '1'
    else:
        pf1 = 'SH'
        pf2 = 'SZ'
    index1 = (f"{pf1}000{str(i).zfill(3)}" for i in range(1,1000))
    index2 = (f"{pf1}950{str(i).zfill(3)}" for i in range(1000))
    index3 = (f"{pf2}399{str(i).zfill(3)}" for i in range(1000))
    stock_list = itertools.chain(index1, index2, index3)
    return stock_list

def get_kcb_stock_list(prefix=0):
    if prefix == 1:
        pf = '0'
    else:
        pf = 'SH'
    stock_list = (f"{pf}688{str(i).zfill(3)}" for i in range(1000))
    return stock_list

def get_xsb_stock_list(prefix=0):
    if prefix == 1:
        pf = '0'
    else:
        pf = 'SH'
    stock_list = (f"{pf}83{str(i).zfill(3)}" for i in range(1000))
    return stock_list

def get_stock_list():
    """
    @API function
    """
    import itertools
    s1 = get_sh_stock_list()
    s2 = get_sz_stock_list()
    s3 = get_cyb_stock_list()
    s4 = get_zxb_stock_list()
    s5 = get_kcb_stock_list()
    s6 = get_b_stock_list()
    stock_list = itertools.chain(s1, s2, s3, s4, s5, s6)
    return stock_list


def get_stock_list2():
    """
    @API function,生成网易财经格式的stock_code
    """
    import itertools
    s1 = get_sh_stock_list(1)
    s2 = get_sz_stock_list(1)
    s3 = get_cyb_stock_list(1)
    s4 = get_zxb_stock_list(1)
    s5 = get_kcb_stock_list(1)
    s6 = get_b_stock_list(1)
    stock_list = itertools.chain(s1, s2, s3, s4, s5, s6)
    return stock_list

def get_index_list2():
    """
    @API function,生成网易财经格式的stock_code
    """
    stock_list = get_index_list(1)
    return stock_list


def stock_code_decoding(stock_code:str):
    if stock_code.startswith("'6") or stock_code.startswith("'83"):
        stock_id = stock_code.replace("'", 'SH')
    elif stock_code.startswith("'000") or stock_code.startswith("'002") or stock_code.startswith("'300"):
        stock_id = stock_code.replace("'", 'SZ')
    else:
        stock_id = stock_code.replace("'", 'SH')
    return stock_id


def index_code_decoding(stock_code:str):
    if stock_code.startswith("'9") or stock_code.startswith("'000"):
        stock_id = stock_code.replace("'", 'SH')
    elif stock_code.startswith("'399"):
        stock_id = stock_code.replace("'", 'SZ')
    else:
        stock_id = stock_code.replace("'", 'SH')
    return stock_id


def read_stock_list():
    from libsql_utils.engine import engine_init
    from sqlalchemy.orm import Session
    from sqlalchemy import select
    from libsql_utils.model.stock import formStockManager
    eng = engine_init(host='localhost', acc='root', pw='6414939', db='stock')
    with Session(eng) as session:
        query = select(formStockManager.stock_code, formStockManager.stock_code2)
        result = session.execute(query).all()
    stock_list = []
    for item in result:
        stock_list.append((item[0], item[1]))
    return stock_list