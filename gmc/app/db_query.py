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

		result = [('cast_info',cast_info[0]),
				  ('char_name',char_name[0]),
				  ('company_name',company_name[0]),
				  ('movie_companies',movie_companies[0]),
				  ('movie_info',movie_info[0]),
				  ('movie_info_idx',movie_info_idx[0]),
				  ('name',name[0]),
				  ('person_info',person_info[0]),
				  ('title',title[0]),
				  ('TOTAL',(cast_info[0]+char_name[0]+company_name[0]+movie_companies[0]+movie_info[0]+movie_info_idx[0]+name[0]+person_info[0]+title[0]))
		]

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
def movie_data(cur_id):
	with connection.cursor() as cursor:
		cursor.execute("select title from title where movie_id=" + cur_id)
		title= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=5 and movie_id=" + cur_id)
		mpaa= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=1 and movie_id=" + cur_id)
		runtime= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=3 and movie_id=" + cur_id)
		genre= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=16 and movie_id=" + cur_id)
		release_date= cursor.fetchall()
		cursor.execute("select rating from movie_info_idx where movie_id=" + cur_id)
		rating= cursor.fetchall()
		cursor.execute("select name, person_id from name inner join cast_info on cast_info.PERSON_ID=name.id where movie_id=" +cur_id+ " and role_id=8)
		director= cursor.fetchall()
		cursor.execute("select name, person_id from name inner join cast_info on cast_info.PERSON_ID=name.id where movie_id=" +cur_id+ " and role_id=4)
		writer= cursor.fetchall()
		cursor.execute("select name, person_id from name inner join cast_info on cast_info.PERSON_ID=name.id where movie_id=" +cur_id+ " and (role_id=1 or role_id=2)")
		actor= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=105 and movie_id=" + cur_id)
		budget= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=108 and movie_id=" + cur_id)
		opweekend= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=106 and movie_id=" + cur_id)
		grweekend= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=107 and movie_id=" + cur_id)
		gross= cursor.fetchall()
		cursor.execute(select name, company_id from company_name inner join movie_companies on movie_companies.COMPANY_ID=company_name.id where movie_id="+cur_id+" and company_type_id=2)
		prod_comp= cursor.fetchall()
		results=[title, mpaa, runtime, genre,release_date,rating,director,writer,actor,budget,opweekend,grweekend,gross,prod_comp]
	return results

def person_data(cur_id):
	with connection.cursor() as cursor:
		cursor.execute("select name from name where id=" + cur_id)
		name= cursor.fetchall()
		cursor.execute("select info from person_info where info_type_id=21 and PERSON_ID=" + cur_id)
		birthday= cursor.fetchall()
		cursor.execute("select info from person_info where info_type_id=23 and PERSON_ID=" + cur_id)
		deathdate= cursor.fetchall()
		cursor.execute("select info from person_info where info_type_id=24 and PERSON_ID=" + cur_id)
		spouse= cursor.fetchall()
		cursor.execute("select gender from name where id=" + cur_id)
		gender= cursor.fetchall()
		cursor.execute("select info from person_info where info_type_id=22 and PERSON_ID=" + cur_id)
		height= cursor.fetchall()
		results=[name,birthday,deathdate,spouse,gender,height]
	return results
