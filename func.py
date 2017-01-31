import os,psycopg2,urlparse
 urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
conn.close();
def index(path):
    return "hello"
def pg(path):
    return "<b>pg"