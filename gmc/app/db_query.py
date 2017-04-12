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
    return results

def movie_data(cur_id):
	with connection.cursor() as cursor:
		cursor.execute("select title from title where id=" + cur_id)
		title= cursor.fetchone()
		cursor.execute("select info from movie_info where info_type_id=5 and movie_id=" + cur_id)
		mpaa= cursor.fetchone()
		cursor.execute("select info from movie_info where info_type_id=1 and movie_id=" + cur_id)
		runtime= cursor.fetchone()
		cursor.execute("select info from movie_info where info_type_id=3 and movie_id=" + cur_id)
		genre= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=16 and movie_id=" + cur_id)
		release_date= cursor.fetchone()
		cursor.execute("select rating from movie_info_idx where movie_id=" + cur_id)
		rating= cursor.fetchone()
		# number of votes
		cursor.execute("select name, person_id from name inner join cast_info on cast_info.PERSON_ID=name.id where movie_id=" +cur_id+ " and role_id=8")
		director= cursor.fetchall()
		cursor.execute("select name, person_id from name inner join cast_info on cast_info.PERSON_ID=name.id where movie_id=" +cur_id+ " and role_id=4")
		writer= cursor.fetchall()
		cursor.execute("select name, person_id, (select name from char_name where id = cast_info.person_role_id and rownum <= 1) as role from name inner join cast_info on cast_info.PERSON_ID=name.id where movie_id=" +cur_id+ " and (role_id=1 or role_id=2) order by nr_order")
		actor= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=105 and movie_id=" + cur_id)
		budget= cursor.fetchone()
		cursor.execute("select info from movie_info where info_type_id=108 and movie_id=" + cur_id)
		opweekend= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=106 and movie_id=" + cur_id)
		grweekend= cursor.fetchall()
		cursor.execute("select info from movie_info where info_type_id=107 and movie_id=" + cur_id)
		gross= cursor.fetchall()
		cursor.execute("select name, company_id from company_name inner join movie_companies on movie_companies.COMPANY_ID=company_name.id where movie_id="+cur_id+" and company_type_id=2")
		prod_comp= cursor.fetchall()
		cursor.execute("select count(gender) from name where id in (select person_id from cast_info where movie_id="+cur_id+") and gender is not null group by gender;")
		gender= cursor.fetchall()
		cursor.execute("select ranking from (select row_number() over(order by votes desc)Ranking, movie_id from movie_info_idx) where movie_id=" + cur_id + ";")
		pop1= cursor.fetchone()
		pop2=round((pop1[0]/10141.0) * 100,1)
		pop=(pop1,pop2)
		cursor.execute("select id,title from title where id in(select movie_id from movie_info where info in (select info from MOVIE_INFO where INFO_TYPE_ID=3 and movie_id =" + cur_id + ") and rownum<=5 group by movie_id having count(distinct info)<= (select count(info) from MOVIE_INFO where INFO_TYPE_ID=3 and movie_id =" + cur_id+"))")
		similar= cursor.fetchall()
		print similar
		results=[title, mpaa, runtime, genre,release_date,rating,director,writer,actor,budget,opweekend,grweekend,gross,prod_comp,gender,pop,similar]
	return results

def person_data(cur_id):
	with connection.cursor() as cursor:
		cursor.execute("select name from name where id=" + cur_id)
		name= cursor.fetchone()
		cursor.execute("select info from person_info where info_type_id=21 and PERSON_ID=" + cur_id)
		birthday= cursor.fetchone()
		cursor.execute("select info from person_info where info_type_id=23 and PERSON_ID=" + cur_id)
		deathdate= cursor.fetchone()
		cursor.execute("select info from person_info where info_type_id=24 and PERSON_ID=" + cur_id)
		spouse= cursor.fetchone()
		cursor.execute("select gender from name where id=" + cur_id)
		gender= cursor.fetchone()
		cursor.execute("select info from person_info where info_type_id=22 and PERSON_ID=" + cur_id)
		height= cursor.fetchone()
		cursor.execute("select movie_id,(select title from title where id = cast_info.movie_id) as title, (select name from char_name where id = cast_info.person_role_id and rownum <= 1) as character from cast_info where person_id = " +cur_id+ " and (role_id = 1 or role_id = 2)")
		acted= cursor.fetchall()
		cursor.execute("select distinct movie_id,(select title from title where id = cast_info.movie_id) as title from cast_info where person_id = " +cur_id+ " and role_id = 8")
		directed= cursor.fetchall()
		cursor.execute("select distinct movie_id,(select title from title where id = cast_info.movie_id) as title from cast_info where person_id = " +cur_id+ " and role_id = 4")
		wrote= cursor.fetchall()
		cursor.execute("select id,name from name where id in (select person_id from person_info where info_type_id=21 and (select info from person_info where info_type_id=21 and PERSON_ID=" + cur_id + ") like CONCAT(substr(info,1,length(info)-5),'%') and person_id <> " + cur_id + ") and rownum<=10")
		same_bd= cursor.fetchall()
		cursor.execute("select id,name from name where id in (select person_id from person_info where info_type_id=22 and info=(select info from person_info where info_type_id=22 and PERSON_ID=" + cur_id + ") and person_id <> " + cur_id + ") and rownum<=10")
		same_ht= cursor.fetchall()
		cursor.execute("select id,title from title where id in (select movie_id from (select movie_id, rating from (select movie_id, rating from movie_info_idx where movie_id in (select movie_id from cast_info where PERSON_ID =" + cur_id + ") order by rating desc)where rownum<=3));")
		top3= cursor.fetchall()
		cursor.execute("select id,title from title where id in (select movie_id from (select movie_id, rating from (select movie_id, rating from movie_info_idx where movie_id in (select movie_id from cast_info where PERSON_ID =" + cur_id + ") order by rating asc)where rownum<=3));")
		low3= cursor.fetchall()
		cursor.execute("select count(rating) from movie_info_idx where movie_id in(select movie_id from cast_info where person_id=" + cur_id + ") and rating>7;")
		excellent= cursor.fetchone()
		cursor.execute("select count(rating) from movie_info_idx where movie_id in(select movie_id from cast_info where person_id=" + cur_id + ") and rating<7 and rating>4;")
		good= cursor.fetchone()
		cursor.execute("select count(rating) from movie_info_idx where movie_id in(select movie_id from cast_info where person_id=" + cur_id + ") and rating<4;")
		poor= cursor.fetchone()
		cursor.execute("select production_year, avg(rating), count(title) from title inner join movie_info_idx on movie_info_idx.MOVIE_ID=title.ID where movie_id in(select movie_id from cast_info where person_id=" + cur_id + ") group by production_year order by production_year desc;")
		rating_movieperyear= cursor.fetchall()

		results=[name,birthday,deathdate,spouse,gender,height,acted,directed,wrote,same_bd,same_ht,top3,low3,excellent,good,poor,rating_movieperyear]
	return results
