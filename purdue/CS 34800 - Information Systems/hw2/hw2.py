import sys

# Use this file to write your queries. Submit this file in Brightspace after finishing your homework.

#TODO: Write your username and answer to each query as a string in the return statements in the functions below. 
# Do not change the function names. 

#Your resulting tables should have the attributes in the same order as appeared in the sample answers. 

#Make sure to test that python prints out the strings (your username and SQL queries) correctly.

#usage: python hw1.py or python3 hw1.py

def username():
	return "oh191"
    
def query1():
	return """
    SELECT
		place.id,
		place.name,
		place.price,
		room.room_type
	FROM
		place,
		room
	WHERE
		place.price = 
			(SELECT MIN(price)
			FROM place)
		AND room.room_type_id = place.room_type_id;
	"""

def query2():
	return """
		SELECT
			host.host_id,
			host.host_name,
			COUNT(place.id) as count_places
		FROM
			host,
			place
		WHERE
			place.host_id = host.host_id
		GROUP BY
			place.host_id
		HAVING
			COUNT(place.host_id) = 
				(SELECT COUNT(place.id)
				FROM place
				GROUP BY place.host_id
				ORDER BY COUNT(place.id) DESC);
	"""

def query3():
	return """
		SELECT
			'neighbourhood with cheapest price' as neighbourhood,
			neighbourhood.name,
			MIN(place.price) as price
		FROM
			place, neighbourhood
		WHERE
			place.neighbourhood_id = neighbourhood.neighbourhood_id
		GROUP BY
			place.neighbourhood_id
		HAVING
			place.price = 
			(SELECT MIN(price)
			FROM place)
		UNION
		SELECT
			'neighbourhood with most expensive price' as neighbourhood,
			neighbourhood.name,
			MIN(place.price) as price
		FROM
			place, neighbourhood
		WHERE
			place.neighbourhood_id = neighbourhood.neighbourhood_id
		GROUP BY
			place.neighbourhood_id
		HAVING
			place.price = 
			(SELECT MAX(price)
			FROM place);
		"""
	
def query4():
	return """
		SELECT id, name, number_of_reviews
		FROM place
		WHERE number_of_reviews IN 
			(SELECT number_of_reviews
			FROM place
			GROUP BY number_of_reviews
			ORDER BY number_of_reviews DESC
			LIMIT 2);
	"""

def query5():
	return """
	SELECT *
	FROM
		(SELECT
			host.host_id,
			host.host_name,
			COUNT(p2.price) as place_count,
			AVG(p2.price) as avg_price
		FROM
			host, place p2
		WHERE host.host_id = p2.host_id
		GROUP BY p2.host_id
		HAVING count(p2.price) >= 3) as q1,
		(SELECT
			host.host_id,
			host.host_name,
			COUNT(p2.price) as place_count,
			AVG(p2.price) as avg_price
		FROM
			host, place p2
		WHERE host.host_id = p2.host_id
		GROUP BY p2.host_id
		HAVING count(p2.price) >= 3) as q2
	WHERE q1.place_count = q2.place_count AND q1.host_id < q2.host_id;
	"""

def query6():
	return """
		SELECT area.area
		FROM area
		LEFT OUTER JOIN neighbourhood ON neighbourhood.area_id = area.area_id
		LEFT OUTER JOIN place ON place.neighbourhood_id = neighbourhood.neighbourhood_id
		GROUP BY area.area_id
		HAVING place.price IS NULL OR MAX(place.price) <=
			(SELECT AVG(place.price)
			FROM place);
	"""

def query7():
	return """
		SELECT
			p1.id,
			p1.name,
			p1.number_of_reviews,
			AVG(p2.number_of_reviews) as avg_number_of_reviews,
			p1.reviews_per_month,
			AVG(p2.reviews_per_month) as avg_reviews_per_month
		FROM
			place as p1, place as p2
		GROUP BY
			p1.id
		HAVING
			p1.number_of_reviews >= 
			(SELECT AVG(number_of_reviews) as avg_nor
			FROM place)
			AND p1.reviews_per_month <= 
			(SELECT AVG(reviews_per_month) as avg_rpm
			FROM place);
	"""

def query8():
	return """
		SELECT
			place.id,
			place.name,
			place.price,
			room.room_type
		FROM place, room
		JOIN
			(SELECT place.room_type_id, place.price FROM place, room
			WHERE place.room_type_id = room.room_type_id
			GROUP BY place.room_type_id
			HAVING MIN(place.price)) as q1
			ON q1.room_type_id = place.room_type_id AND q1.price = place.price
		WHERE place.room_type_id = room.room_type_id;
	"""

def query9():
	return """
		SELECT
			area.area,
			COUNT(place.id) as overall_count,
			COUNT(case when place.room_type_id = 2 then 1 end) as 'Private_room_count',
			COUNT(case when place.room_type_id = 3 then 1 end) as 'Shared_room_count',
			COUNT(case when place.room_type_id = 1 then 1 end) as 'Entire_home_count'
		FROM area
		JOIN neighbourhood ON area.area_id = neighbourhood.area_id
		JOIN place ON neighbourhood.neighbourhood_id = place.neighbourhood_id
		GROUP BY area.area;
	"""

def query10():
	return """
		SELECT
			area.area,
			AVG(place.price) as area_avg_price,
			AVG(p2.price) as other_areas_avg_price
		FROM area, place p2, neighbourhood n2
		JOIN neighbourhood ON area.area_id = neighbourhood.area_id
		JOIN place ON neighbourhood.neighbourhood_id = place.neighbourhood_id
		WHERE p2.neighbourhood_id = n2.neighbourhood_id
			AND n2.area_id <> area.area_id
		GROUP BY area.area
		ORDER BY avg(place.price);
	"""

def query11():
	return """
		SELECT area.area
		FROM place
		JOIN neighbourhood ON place.neighbourhood_id = neighbourhood.neighbourhood_id
		JOIN area ON neighbourhood.area_id = area.area_id
		GROUP BY area.area_id
		HAVING MIN(place.minimum_nights) = 
			(SELECT MIN (minimum_nights)
			FROM place) AND MAX(place.minimum_nights) =
  			(SELECT MAX(minimum_nights)
			FROM place);
	"""

def query12():
	return """
		SELECT
			id,
			latitude,
			longitude,
			price
		FROM
			place
		WHERE
			price > 150
			AND latitude < 
				(SELECT ((MAX(latitude) + MIN(latitude)) / 2) FROM place)
			AND longitude < 
				(SELECT ((MAX(longitude) + MIN(longitude)) / 2) FROM place);
	"""

def query13():
	return """
		SELECT
			'north east' as city_side,
			COUNT(*) as count
		FROM
			place
		WHERE
			latitude > (SELECT ((MAX(latitude) + MIN(latitude)) / 2) FROM place)
			AND longitude > (SELECT ((MAX(longitude) + MIN(longitude)) / 2) FROM place)

		UNION

		SELECT
			'north west' as city_side,
			COUNT(*) as count
		FROM
			place
		WHERE
			latitude > (SELECT ((MAX(latitude) + MIN(latitude)) / 2) FROM place)
			AND longitude < (SELECT ((MAX(longitude) + MIN(longitude)) / 2) FROM place)

		UNION

		SELECT
			'south east' as city_side,
			COUNT(*) as count
		FROM
			place
		WHERE
			latitude < (SELECT ((MAX(latitude) + MIN(latitude)) / 2) FROM place)
			AND longitude > (SELECT ((MAX(longitude) + MIN(longitude)) / 2) FROM place)

		UNION

		SELECT
			'south west' as city_side,
			COUNT(*) as count
		FROM
			place
		WHERE
			latitude < (SELECT ((MAX(latitude) + MIN(latitude)) / 2) FROM place)
			AND longitude < (SELECT ((MAX(longitude) + MIN(longitude)) / 2) FROM place)

		UNION

		SELECT
			'total' as city_side,
			count (*) as count
		FROM place;
	"""


#Do not edit below

def main():
	query_options = {1: query1(), 2: query2(), 3: query3(), 4: query4(), 5: query5(), 6: query6(), 7: query7(), 8: query8(), 
		9: query9(), 10: query10(), 11: query11(), 12: query12(), 13: query13()}
	
	if len(sys.argv) == 1:
		if username() == "username":
			print("Make sure to change the username function to return your username.")
			return
		else:
			print(username())
		for query in query_options.values():
			print(query)
	elif len(sys.argv) == 2:
		if sys.argv[1] == "username":
			print(username())
		else:
			print(query_options[int(sys.argv[1])])

	
if __name__ == "__main__":
   main()
