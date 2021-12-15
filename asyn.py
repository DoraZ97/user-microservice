import grequests
from datetime import datetime
import requests


urls = [
    'http://www.heroku.com',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://kennethreitz.com'
]

url = [
    'http://127.0.0.1:5000/address',
    'http://127.0.0.1:5000/users',
    'http://127.0.0.1:5000/users/1',
    'http://127.0.0.1:5000/users/1/address'
]


def t1():
    s = datetime.now()
    #rs = (grequests.get(u) for u in urls)
    rs = (grequests.get(u) for u in url)
    x = grequests.map(rs)
    print(x)
    e = datetime.now()

    print("T1")
    print("Elapsed time = ", e-s)

    for r in x:
        print(r.url, r.status_code)


def t2():

    s = datetime.now()
    result = []

    for u in url:
        r = requests.get(u)
        result.append([u, r.status_code])

    e = datetime.now()

    print("T2")
    print("Elapsed time = ", e - s)

    for x in result:
        print(x)


t1()
#t2()