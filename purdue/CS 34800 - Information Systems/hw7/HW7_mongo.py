import sys

#TODO: Write your username and answer to each query as a string in the return statements 
# in the functions below. Do not change the function names. 

# Write your queries using multi-line strings and use proper indentation to increase readability.
# Write mapreduce code as multi-line string. For example:
# 
# def query6():
#     return """
# 
#             var mapFunction1 = function() {
#                ...
#             }
# 
#             var reduceFunction1 = function(a, b) {
#                return ...
#             }
# 
#             db.bills.mapReduce(mapFunction1, reduceFunction1, {
#                ...
#             })
#           """

# Your result should have the attributes in the same order as appeared in the sample answers. 

# Make sure to test that python prints out the strings correctly.

# usage: python hw6.py

def username():
	return "oh191"
    
def query1():
    return """
        db.earthquakes.aggregate([
            { $match: { "properties.mag" : { $gte: 2.0 } } },
            { $project: { _id: 1, "place": "$properties.place", "mag" : "$properties.mag", "sig": "$properties.sig" } },
            ]).pretty();
           """ 

def query2():
    return """
        db.earthquakes.aggregate([
            { $match: { "geometry.coordinates.0" : { $gte: -120, $lte: -60 }, "geometry.coordinates.1" : { $gte: 30, $lte: 35 } } },
            { $project: { "_id": 0, "geometry.coordinates" : 1, "place": "$properties.place" } },
            ]).pretty();
           """
            
def query3():
    return """
        db.earthquakes.aggregate([
            { $group: { "_id" : "$properties.status", "avg_mag" : { $avg: "$properties.mag"} } }
            ]).pretty();
           """ 

def query4():
    return """
        var mapFunction = function(){ emit(this.properties.status, this.properties.mag); };
        var reduceFunction = function(key, values){ var result = Array.avg(values); return result };
        db.earthquakes.mapReduce(mapFunction, reduceFunction, {out: {inline:1}});
           """

def query5():
    return """
        db.earthquakes.aggregate([
            {
                $lookup: {
                    from: "earthquakes",
                    localField: "properties.net",
                    foreignField: "properties.net",
                    as: "matches"
                }
            },
            { $unwind: "$matches" },
            { $match: { $expr: { $gt: ["$_id", "$matches._id"] } } },
            { 
                $project: {
                    "place": "$properties.place",
                    "net": "$properties.net",
                    "other_id": "$matches._id",
                    "other_place": "$matches.properties.place",
                    "other_net": "$matches.properties.net"
                            }
            }
        ]).pretty();
           """ 

def query6():
    return """
    db.earthquakes.aggregate([
        {
            $lookup: {
                from: "networks",
                localField: "net",
                foreignField: "properties.net",
                as: "matches"
            }
        },
        { $unwind: "$matches" },
        { $match: { $expr: { $eq: ["$properties.net", "$matches.net"] } } },
        { 
            $project: {
                "_id": 0,
                "place": "$properties.place",
                "netCode": "$properties.net",
                "description": "$matches.description"
                        }
        }
    ]).pretty();
    
           """

def query7():
    return """
    db.earthquakes.aggregate([
        {
            $lookup: {
                from: "networks",
                localField: "net",
                foreignField: "properties.net",
                as: "matches_net"
            }
        },
        { $unwind: "$matches_net" },
        {
            $lookup: {
                from: "magnitude_types",
                localField: "magType",
                foreignField: "properties.magType",
                as: "matches_mag"
            }
        },
        { $unwind: "$matches_mag" },
        { $match: { $expr: { $eq: ["$properties.net", "$matches_net.net"] } } },
        { $match: { $expr: { $eq: ["$properties.magType", "$matches_mag.magType"] } } },
        { 
            $project: {
                "_id": 0,
                "place": "$properties.place",
                "netCode": "$properties.net",
                "magType": "$matches_mag.magType",
                "description": "$matches_net.description",
                "magDescription": "$matches_mag.magDescription",
                "magRange": "$matches_mag.Magnitude Range",
                "distanceRange": "$matches_mag.Distance Range"
            }
        }
    ]).pretty();
           """

def query8():
    return """
    db.earthquakes_embedded.aggregate([
        {
            $lookup: {
                from: "networks",
                localField: "net",
                foreignField: "properties.net.net",
                as: "matches_net"
            }
        },
        { $unwind: "$matches_net" },
        {
            $lookup: {
                from: "magnitude_types",
                localField: "magType",
                foreignField: "properties.magType.magType",
                as: "matches_mag"
            }
        },
        { $unwind: "$matches_mag" },
        { $match: { $expr: { $eq: ["$properties.net.net", "$matches_net.net"] } } },
        { $match: { $expr: { $eq: ["$properties.magType.magType", "$matches_mag.magType"] } } },
        { 
            $project: {
                "_id": 0,
                "place": "$properties.place",
                "netCode": "$properties.net.net",
                "magType": "$matches_mag.magType",
                "description": "$matches_net.description",
                "magDescription": "$matches_mag.magDescription",
                "magRange": "$matches_mag.Magnitude Range",
                "distanceRange": "$matches_mag.Distance Range"
            }
        }
    ]).pretty();
           """

def query9():
    return """
    var mapFunction = function(){ var types = this.properties.types.split(","); types.forEach((element) => { if(element != "") emit(element, 1); });};
    var reduceFunction = function(key, values){ return values.length; };
    db.earthquakes_embedded.mapReduce(mapFunction, reduceFunction, {out: {inline:1}});
           """

def query10():
    return """
    db.graph.aggregate([
        {
            $project: {
                "_id": 0,
                "node_id": 1,
                "adj_list": 1,
                "degree": { $size: "$adj_list" }
            }
        },
        { $unwind: "$adj_list" },
        { $out: "unwind_graph" }
    ]);
    db.unwind_graph.aggregate([
        {
            $lookup: {
                from: "unwind_graph",
                localField: "adj_list",
                foreignField: "node_id",
                as: "adj"
            }
        },
        { $unwind: "$adj" },
        {
            $project: {
                "_id": 0,
                "node_id": 1,
                "degree": 1,
                "adj": 1
            }
        },
        { $out: "graph_list" }
    ]);
    db.graph_list.aggregate([
        {
            $group: {
                "_id": {
                    "node_id": "$node_id",
                    "adj": "$adj.node_id"
                },
                "par_node_deg": { $max: "$degree" },
                "adj_node_deg": { $max: "$adj.degree" }
                
            }
        },
        {
            $group: {
                "_id": "$_id.node_id",
                "par_node_deg": { $max: "$par_node_deg" },
                "adj_node_deg": { $max: "$adj_node_deg" }
            }
        },
        {
            $project: {
                "_id": 1,
                "value": {
                    $cond: { if: { $gte: [ "$par_node_deg", "$adj_node_deg" ] },
                    then: { $concat: ["node degree =", { $toString: "$par_node_deg" }, " , this node's degree is >= the degree of all of its neighbors" ]},
                    else: "this node's degree is smaller than the degree of its neighbors" }
                }
            }
        },
        { $out: "result" }
    ]);
    var mapFunction = function(){ emit(this._id, this.value); };
    var reduceFunction = function(key, values){ return values[0]; };
    db.result.mapReduce(mapFunction, reduceFunction, {out: {inline:1}});
           """

def query11():
    return """
           """

#Do not edit below

def main():
	query_options = {1: query1(), 2: query2(), 3: query3(), 4: query4(), 
		5: query5(), 6: query6(), 7: query7(), 8: query8(), 9: query9(), 10: query10(), 11: query11()}
	
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
