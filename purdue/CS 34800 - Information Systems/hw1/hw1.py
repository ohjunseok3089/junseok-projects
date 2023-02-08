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
			host.host_name,
			room.room_type,
			place.price,
			neighbourhood.name as neighbourhood, area.area
		FROM
			place
		JOIN
			host ON place.host_id = host.host_id 
		JOIN
			room ON place.room_type_id = room.room_type_id
		JOIN
			neighbourhood ON place.neighbourhood_id = neighbourhood.neighbourhood_id
		JOIN
			area ON neighbourhood.area_id = area.area_id
		WHERE
			neighbourhood.name = 'Harlem';
	"""

def query2():
	return """
		SELECT
			place.id,
			place.name,
			host.host_name,
			room.room_type,
			place.price,
			place.longitude,
			place.latitude
		FROM
			place
		JOIN
			host ON place.host_id = host.host_id 
		JOIN
			room ON place.room_type_id = room.room_type_id
		GROUP BY
			place.id
		HAVING 
			place.latitude >= 40.75 AND place.latitude <= 40.77
			AND place.longitude <= -73.97 AND place.longitude >= -73.99;
	"""

def query3():
	return """
		SELECT
			minimum_nights
		FROM
			place
		GROUP BY
			minimum_nights
	"""
	
def query4():
	return """
		SELECT
			AVG(place.price) as avg_price,
			COUNT(place.id) as place_count,
			MAX(place.price) as max_price,
			MIN(place.price) as min_price
		FROM
			place;
	"""

def query5():
	return """
		SELECT
			AVG(place.price) as avg_price,
			COUNT(place.id) as place_count,
			MAX(place.price) as max_price,
			MIN(place.price) as min_price
		FROM
			place
		JOIN
			neighbourhood
		ON
			neighbourhood.neighbourhood_id = place.neighbourhood_id
		WHERE
			neighbourhood.name = 'Harlem';
	"""

def query6():
	return """
		SELECT
			neighbourhood.name as neighbourhood,
			AVG(place.price) as avg_price,
			COUNT(place.id) as place_count,
			MAX(place.price) as max_price,
			MIN(place.price) as min_price
		FROM
			place
		JOIN
			neighbourhood
		ON
			neighbourhood.neighbourhood_id = place.neighbourhood_id
		GROUP BY
			neighbourhood.name
		ORDER BY
			avg_price DESC;
	"""

def query7():
	return """
		SELECT
			neighbourhood.name as neighbourhood,
			room.room_type as room_type,
			AVG(place.price) as avg_price,
			COUNT(place.id) as place_count,
			MAX(place.price) as max_price,
			MIN(place.price) as min_price
		FROM
			place
		JOIN
			neighbourhood ON neighbourhood.neighbourhood_id = place.neighbourhood_id
		JOIN
			room ON place.room_type_id = room.room_type_id
		GROUP BY
			neighbourhood.name, room_type
		ORDER BY
			avg_price DESC;
	"""

def query8():
	return """
		SELECT
			area.area as area,
			neighbourhood.name as neighbourhood,
			place.id as id,
			place.name as name,
			place.price as price
		FROM
			area
		LEFT OUTER JOIN
			neighbourhood ON area.area_id = neighbourhood.area_id
		LEFT OUTER JOIN
			place ON neighbourhood.neighbourhood_id = place.neighbourhood_id
		WHERE
			area.area = 'Staten Island'; 
	"""

def query9():
	return """
		SELECT
			area.area as area,
			neighbourhood.name as neighbourhood,
			COUNT(place.id) as place_count,
			AVG(place.price) as avg_price
		FROM
			area
		LEFT OUTER JOIN
			neighbourhood ON area.area_id = neighbourhood.area_id
		LEFT OUTER JOIN
			place ON neighbourhood.neighbourhood_id = place.neighbourhood_id
		WHERE
			area.area NOT IN ('Manhattan', 'Brooklyn')
		GROUP BY
			area.area, neighbourhood.name;
 	"""

def query10():
	return """
		SELECT
			area.area as area,
			neighbourhood.name as neighbourhood,
			COUNT(place.id) as place_count,
			AVG(place.price) as avg_price
		FROM
			area
		LEFT OUTER JOIN
			neighbourhood ON area.area_id = neighbourhood.area_id
		LEFT OUTER JOIN
			place ON neighbourhood.neighbourhood_id = place.neighbourhood_id
		WHERE
			area.area NOT IN ('Manhattan', 'Brooklyn')
		GROUP BY
			area.area, neighbourhood.name
		HAVING
			place_count >= 2;
	"""

def query11():
	return """
		SELECT
  			neighbourhood.name as name
		FROM
  			neighbourhood
		WHERE
  			neighbourhood.name LIKE "B%"
		UNION
		SELECT
  			area.area as name
		FROM
  			area
		WHERE
  			area.area LIKE "B%";
	"""

def query12():
	return """
		SELECT
			neighbourhood.name as name
		FROM
			neighbourhood 
		JOIN
			place ON place.neighbourhood_id = neighbourhood.neighbourhood_id
		GROUP BY
			neighbourhood.neighbourhood_id
		HAVING
			COUNT(place.id) >= 5
			AND MIN(place.price) <= 70;
	"""

def query13():
	return """
		SELECT
			area
		FROM
			area
		WHERE NOT EXISTS
		(SELECT *
			FROM room, place, neighbourhood
			WHERE room.room_type = 'Entire home/apt'
				AND place.room_type_id = room.room_type_id
				AND neighbourhood.area_id = area.area_id
				AND neighb ourhood.neighbourhood_id = place.neighbourhood_id)
		GROUP BY area;
	"""

def query14():
	return """
		SELECT p1.name, p1.price, p2.name, p2.price
		FROM place as p1, place as p2
		WHERE p1.price < p2.price
			AND p1.neighbourhood_id = p2.neighbourhood_id
			AND p1.room_type_id = p2.room_type_id
			AND p1.number_of_reviews = p2.number_of_reviews;
"""

def query15():
	return """
	SELECT
		p1.id as place1_id,
		p2.id as place2_id,
		p3.id as place3_id,
		p1.price as price,
		p1.room_type_id as room_type_id
	FROM
		place as p1,
		place as p2,
		place as p3
	WHERE
		p1.id < p2.id
		AND p2.id < p3.id
		AND p1.price = p2.price
		AND p2.price = p3.price
		AND p1.room_type_id = p2.room_type_id
		AND p2.room_type_id = p3.room_type_id
		AND p1.neighbourhood_id <> p2.neighbourhood_id
		AND p2.neighbourhood_id <> p3.neighbourhood_id
		AND p1.neighbourhood_id <> p3.neighbourhood_id
		AND p1.price < 100;
	"""

#Do not edit below

def main():
	query_options = {1: query1(), 2: query2(), 3: query3(), 4: query4(), 5: query5(), 6: query6(), 7: query7(), 8: query8(), 
		9: query9(), 10: query10(), 11: query11(), 12: query12(), 13: query13(), 14: query14(), 15: query15()}
	
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
