import sys


#TODO: Write your username and answer to each query as a string in the return statements 
# in the functions below. Do not change the function names. 

# Write your queries using multi-line strings and use proper indentation to increase readability

#Your result should have the attributes in the same order as appeared in the sample answers. 

#Make sure to test that python prints out the strings correctly.

#usage: python hw5_Neo4J.py

def username():
	return "oh191"
    
def query6():
    return """
            MATCH (au:Author)-[:Wrote]->(ar:Article)-[:Used]->(la:Language)
            WHERE la.name = "Python"
            RETURN au.name, ar.title, la.name;
           """ 

def query7():
    return """
            MATCH (au:Author)-[:Wrote]->(ar:Article)-[:Used]->(la:Language)
            WHERE la.name = "Python" OR la.name = "Java"
            RETURN au.name, ar.title, la.name;
           """ 


def query8():
    return """
            MATCH (au:Author)-[wr:Wrote|Reviewed]->(ar:Article)-[:In_Area]->(to:Topic)
            WHERE to.name = "Database Systems"
            RETURN au.name, type(wr), ar.title, to.name;
           """ 


def query9():
    return """
            MATCH (au:Author)-[wr:Wrote|Reviewed]->(ar:Article)
            WITH au, COUNT(*) AS appear, collect(ar.title) AS articles
            WHERE appear = 2
            RETURN au.name AS author, articles[0] AS paper1, articles[1] AS paper2, "highly related" AS relatedness;
           """ 


def query10():
    return """
            MATCH (la:Language)<-[rel:Used]-(ar:Article)
            WITH la, COUNT(ar.title) AS appear
            WHERE appear >= 2
            RETURN la.name AS author, appear as cnt;
           """ 


def query11():
    return """
            MATCH (ar:Article)<-[:Wrote]-(au_w:Author)
            OPTIONAL MATCH (ar)<-[:Reviewed]-(au_r:Author)
            WITH ar, COUNT(au_r) as reviewers_count, COUNT(au_w) as writers_count
            RETURN ar.title, reviewers_count, writers_count;
           """ 


def query12():
    return """
            MATCH (au2:Author)-[:Wrote]->(ar:Article)-[:In_Area]->(to:Topic), (ar)-[:Used]->(la:Language)
            WITH au2, la, COUNT(la.name) AS cnt, to
            WHERE to.name = "Database Systems"
            RETURN au2.name, cnt;
           """ 


def query13():
    return """
            MATCH (ar:Article)-[:In_Area]->(to:Topic), (ar)-[:Used]->(la:Language)
            WITH la, to, COUNT(DISTINCT ar.title) as cnt
            return la.name, to.name, cnt;
           """ 

def query14():
    return """
            MATCH (au:Author)-[:Wrote|Reviewed]->(ar:Article)-[:In_Area]->(to:Topic), (ar)-[:Used]->(la:Language)
            WITH la, to, COUNT(DISTINCT au.name) as authors_count
            return la.name, to.name, authors_count;
           """ 


#Do not edit below

def main():
	query_options = { 6: query6(), 7: query7(), 8: query8(), 
		9: query9(), 10: query10(), 11: query11(), 12: query12(), 13: query13(), 14: query14()}
	
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
