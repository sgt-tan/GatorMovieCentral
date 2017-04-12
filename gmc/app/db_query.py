from django.db import connection

def tuple_count():
    with connection.cursor() as cursor:
		cursor.execute("SELECT count(*) FROM cast_info")
		cast_info = cursor.fetchone()
		cursor.execute("SELECT count(*) FROM char_name")
		char_name = cursor.fetchone()
		cursor.execute("SELECT count(*) FROM company_name")
		company_name = cursor.fetchone()
		cursor.execute("SELECT count(*) FROM movie_companies")
		movie_companies = cursor.fetchone()
		cursor.execute("SELECT count(*) FROM movie_info")
		movie_info = cursor.fetchone()
		cursor.execute("SELECT count(*) FROM movie_info_idx")
		movie_info_idx = cursor.fetchone()
		cursor.execute("SELECT count(*) FROM name")
		name = cursor.fetchone()
		cursor.execute("SELECT count(*) FROM person_info")
		person_info = cursor.fetchone()
		cursor.execute("SELECT count(*) FROM title")
		title = cursor.fetchone()

		result = ("cast_info: " + str(cast_info[0]) + "<br>" +
			"char_name: " + str(char_name[0]) + "<br>" +
			"company_name: " + str(company_name[0]) + "<br>" +
			"movie_companies: " + str(movie_companies[0]) + "<br>" +
			"movie_info: " + str(movie_info[0]) + "<br>" +
			"movie_info_idx: " + str(movie_info_idx[0]) + "<br>" +
			"name: " + str(name[0]) + "<br>" +
			"person_info: " + str(person_info[0]) + "<br>" +
			"title: " + str(title[0]) + "<br>" +
			"TOTAL: " + str(cast_info[0]+char_name[0]+company_name[0]+movie_companies[0]+movie_info[0]+movie_info_idx[0]+name[0]+person_info[0]+title[0]))

    return result

def search_movie(query):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id,title FROM title WHERE upper(title) LIKE \'%" + query.upper() + "%\' AND rownum <= 10")
        results = cursor.fetchall()
    return results

def search_person(query):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id,name FROM name WHERE upper(name) LIKE \'%" + query.upper() + "%\' AND rownum <= 10")
        results = cursor.fetchall()
        for res in results:
            res = (res[0], ' '.join(res[1].split(',')[::-1]).strip())
    return results
