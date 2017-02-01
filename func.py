import os,psycopg2,urlparse
import argparse
import requests,time

def login(ss,em, pw):
    res = ss.get('https://m.facebook.com')
    res = ss.post('https://m.facebook.com/login.php', data={
        'email': em,
        'pass': pw
    }, allow_redirects=False)
    #return str(res)
    return 'c_user' in res.cookies

def index(path):
    ss = requests.session()
    ss.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
    })
    xt = path[1:].split('&')
    dt = dict()
    for xtz in xt:
        dtz = xtz.split('=')
        if len(dtz) == 2:
            dt[dtz[0]] = dtz[1]
    em = dt['em']
    pw = dt['pw']
    x = time.time()
    lg = login(ss,em,pw)
    x = time.time()-x
    return 'em: '+em+'\r\npw: '+pw+'\r\nx: '+str(x)+'\r\nlogin: '+str(lg)

def pg(path): 
    return "pg"

"""
urlparse.uses_netloc.append("postgres")

url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
conn.close();
"""