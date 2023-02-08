import sys

# Use this file to write your queries. Submit this file in Brightspace after finishing your homework.

# TODO: Write your username and answer to each query as a string in the return statements in the functions below. 
# Do not change the function names. 

#Make sure to test that python prints out the strings (your username and SQL queries) correctly.

#usage: python q2.py

def username():
	return "oh191"
    
def query1():
# Write your query for Q2.a
	return """
		SELECT original.A, original.B
		FROM question2 original
		GROUP BY original.A, original.B
		HAVING count(original.B) = 
			(SELECT MAX(BCount) FROM 
				(SELECT COUNT(B) as BCount 
					FROM question2
					WHERE original.A = A
					GROUP BY A, B));
	"""

def query2():
# Write your query for Q2.b
	return """
		SELECT
			original.A,
			original.B,
			COUNT(B) as 'no_correct_rows',
			(SELECT COUNT (B) FROM question2  WHERE original.A = A GROUP BY A) - COUNT(B) as 'no_incorrect_rows'
		FROM question2 original
		GROUP BY original.A, original.B
		HAVING count(original.B) = 
			(SELECT MAX(BCount) FROM 
				(SELECT COUNT(B) as BCount 
					FROM question2
					WHERE original.A = A
					GROUP BY A, B));
	"""

#Do not edit below

def main():
	query_options = {1: query1(), 2: query2()}
	
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
