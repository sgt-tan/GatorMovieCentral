from django.db import connection

def search_movie(query):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id,title FROM title WHERE upper(title) LIKE \'%" + query.upper() + "%\' AND rownum <= 10")
        results = cursor.fetchall()
    return results

def search_person(query):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id,name FROM name WHERE upper(name) LIKE \'%" + query.upper() + "%\' AND rownum <= 10")
        results = cursor.fetchall()
    return results
