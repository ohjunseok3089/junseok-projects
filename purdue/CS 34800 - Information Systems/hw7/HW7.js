/*
HW7: MongoDB
Due Date: 4/25/2022 at 11:59 pm
Consider the json files: earthquakes.json, earthquakes_embedded.json, networks.json, magnitude_types.json, and graph.json included with this homework.

Instructions:
1- Use Mongodb version 4.4 or an earlier version. Mapreduce is not supported by version 5.0
2- To install mongodb 4.4 in GCP compute engine, follow these instructions:
--2.1 in GCP console, go to compute engine (you can search for compute engine in the search box)
--2.2 Create a new virtual machine, use the smallest machine available (small RAM, small cpu, ..) 
-----2.2.1 a small virtual machine costs about 7 dollars a month. Using a VM for a few days to work on the homework should not cost more than 2 to 4 dollars.

--2.3 SSH to the machine

--2.4 install wget using the command 
      sudo apt-get install wget

--2.5 run the following commands (source:https://www.mongodb.com/docs/v4.4/tutorial/install-mongodb-on-debian/)

wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

sudo apt-get update

sudo apt-get install -y mongodb-org=4.4.13 mongodb-org-server=4.4.13 mongodb-org-shell=4.4.13 mongodb-org-mongos=4.4.13 mongodb-org-tools=4.4.13

echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections

-- 2.6 start mongodb server
sudo systemctl start mongod

-- 2.7 Verify that MongoDB has started successfully
sudo systemctl status mongod

-- 2.8 upload the json datasets to the virtual machine (use dropdown menu in the top reight corner)

-- 2.9 upload the datasets to MongoDB, use the mongoimport command as follows:
for example,
mongoimport --db db1 --collection earthquakes --file earthquakes.json

-- 2.10 start the mongo shell 
mongo

-- 2.11 switch to the database you want
use db1

- 2.12 start writing queries

- 2.13 done with the homework! terminate the VM. Go to compute engine and delete the VM. 
*/


//3. Include only attributes shown in the expected output. The order of the attributes in your result should match the one in the expected result. The order of the documents (rows) can be different.

//4. All questions (except Question 8) use the earthquakes json dataset. Only Question 8 uses the earthquakes_embedded.json 

//4. Copy and paste your queries to HW7_mongo.py
//  Submit your homework to Brightspace

// Questions:

//1) (5 points) list earthquakes with magnitude of 2.0 or more. 

//Expected output
{
    "_id" : ObjectId("625751f3f3ed753c1850fbb9"),
    "place" : "15 km SW of Leilani Estates, Hawaii",
    "mag" : 2.44,
    "sig" : 92
}
{
    "_id" : ObjectId("625751f3f3ed753c1850fbbc"),
    "place" : "0 km WSW of Magas Arriba, Puerto Rico",
    "mag" : 3.16,
    "sig" : 154
}
{
    "_id" : ObjectId("625751f3f3ed753c1850fbbe"),
    "place" : "12km NNE of Lake Hughes, CA",
    "mag" : 2.07,
    "sig" : 66
}

//2) (7 points) List earthquakes with longitude (coordinates[0]) between -60 and -120 and latitude (coordinates[1] between 30 and 35). 

//Expected output
{
    "geometry" : {
            "coordinates" : [
                    -116.779,
                    32.9331667,
                    17.25
            ]
    },
    "place" : "8km S of San Diego Country Estates, CA"
}
{
    "geometry" : {
            "coordinates" : [
                    -118.4033333,
                    34.7781667,
                    0.69
            ]
    },
    "place" : "12km NNE of Lake Hughes, CA"
}

// 3) (5 points) Use the aggregate pipeline to list the average magnitude (mag attribute) for each status type (status attribute) 

//Expected output
{ "_id" : "reviewed", "avg_mag" : 2.31 }
{ "_id" : "automatic", "avg_mag" : 1.5633333333333332 }

//4) (8 points) Redo the previous question using mapreduce

//Expected output

{
    "results" : [
            {
                    "_id" : "reviewed",
                    "value" : 2.31
            },
            {
                    "_id" : "automatic",
                    "value" : 1.5633333333333332
            }
    ],
    "ok" : 1
}

//5) (13 points)
//Using the aggregate pipeline, find pairs of earthquakes that have the same network type (net attribute)

//Expected output
{
    "_id" : ObjectId("625751f3f3ed753c1850fbb9"),
    "place" : "15 km SW of Leilani Estates, Hawaii",
    "net" : "hv",
    "other_id" : ObjectId("625751f3f3ed753c1850fbbd"),
    "other_place" : "8 km E of Pāhala, Hawaii",
    "other_net" : "hv"
}
{
    "_id" : ObjectId("625751f3f3ed753c1850fbbb"),
    "place" : "8km S of San Diego Country Estates, CA",
    "net" : "ci",
    "other_id" : ObjectId("625751f3f3ed753c1850fbbe"),
    "other_place" : "12km NNE of Lake Hughes, CA",
    "other_net" : "ci"
}

//6) (10 points) Using the aggregate pipeline, compute the natural join between earthquakes and networks collections. Use the net attribute for the join condition.

//Expected output
{
    "place" : "15 km SW of Leilani Estates, Hawaii",
    "netCode" : "hv",
    "description" : "Hawaii Volcano Observatory"
}
{
    "place" : "22 km NNW of Nelchina, Alaska",
    "netCode" : "ak",
    "description" : "Alaska Earthquake Center"
}
{
    "place" : "8km S of San Diego Country Estates, CA",
    "netCode" : "ci",
    "description" : "California Integrated Seismic Network: Southern California Seismic Network (Caltech/USGS Pasadena and Partners) and Southern California Earthquake Data Center"
}
{
    "place" : "0 km WSW of Magas Arriba, Puerto Rico",
    "netCode" : "pr",
    "description" : "Puerto Rico Seismic Network"
}
{
    "place" : "8 km E of Pāhala, Hawaii",
    "netCode" : "hv",
    "description" : "Hawaii Volcano Observatory"
}
{
    "place" : "12km NNE of Lake Hughes, CA",
    "netCode" : "ci",
    "description" : "California Integrated Seismic Network: Southern California Seismic Network (Caltech/USGS Pasadena and Partners) and Southern California Earthquake Data Center"
}

 //7) (15 points) Using the aggregate pipeline, compute earthquakes natural join networks natural join magnitude_types. Use the earthquakes.json, networks.json, and magnitude_types.json files. 

//Expected output
{
    "place" : "15 km SW of Leilani Estates, Hawaii",
    "netCode" : "hv",
    "magType" : "ml",
    "description" : "Hawaii Volcano Observatory",
    "magDescription" : "ml  (local)",
    "magRange" : "~2.0 to ~6.5",
    "distanceRange" : "0 - 600 km"
}
{
    "place" : "22 km NNW of Nelchina, Alaska",
    "netCode" : "ak",
    "magType" : "ml",
    "description" : "Alaska Earthquake Center",
    "magDescription" : "ml  (local)",
    "magRange" : "~2.0 to ~6.5",
    "distanceRange" : "0 - 600 km"
}
{
    "place" : "8km S of San Diego Country Estates, CA",
    "netCode" : "ci",
    "magType" : "ml",
    "description" : "California Integrated Seismic Network: Southern California Seismic Network (Caltech/USGS Pasadena and Partners) and Southern California Earthquake Data Center",
    "magDescription" : "ml  (local)",
    "magRange" : "~2.0 to ~6.5",
    "distanceRange" : "0 - 600 km"
}
{
    "place" : "0 km WSW of Magas Arriba, Puerto Rico",
    "netCode" : "pr",
    "magType" : "md",
    "description" : "Puerto Rico Seismic Network",
    "magDescription" : "md  (duration)",
    "magRange" : "~4 or smaller",
    "distanceRange" : "0 - 400 km"
}
{
    "place" : "8 km E of Pāhala, Hawaii",
    "netCode" : "hv",
    "magType" : "md",
    "description" : "Hawaii Volcano Observatory",
    "magDescription" : "md  (duration)",
    "magRange" : "~4 or smaller",
    "distanceRange" : "0 - 400 km"
}
{
    "place" : "12km NNE of Lake Hughes, CA",
    "netCode" : "ci",
    "magType" : "ml",
    "description" : "California Integrated Seismic Network: Southern California Seismic Network (Caltech/USGS Pasadena and Partners) and Southern California Earthquake Data Center",
    "magDescription" : "ml  (local)",
    "magRange" : "~2.0 to ~6.5",
    "distanceRange" : "0 - 600 km"
}

//8) (7 points) Using the aggregate pipeline, redo the previous question using earthquakes_embedded.json. 

// 9) (10 points) Use the mapreduce framework to count each type (the individual terms in the types attribute).

//Expected output
{
    "results" : [
            {
                    "_id" : "origin",
                    "value" : 6
            },
            {
                    "_id" : "phase-data",
                    "value" : 6
            },
            {
                    "_id" : "nearby-cities",
                    "value" : 2
            },
            {
                    "_id" : "scitech-link",
                    "value" : 2
            }
    ],
    "ok" : 1
}

//10) (20 points) Consider the undirected graph in graph.json. A diagram of the graph is shown below:
/*
     (G:Student)     
     /
    F(Course)        
   /         \       
  B(Faculty)--D(Course)---\
 /          \     /        \
A(student)   C(Faculty)----E(student)
*/

//The degree of a node is the number of edges it has. Find any node whose degree is greater than or equal the degree of every adjacent node. For example, the node B has a degree 4 which is >= the degree of all B's adjacent nodes (A=1, F=2, C=3, D=4)

//Expected Output
{
    "results" : [
            {
                    "_id" : "C",
                    "value" : "this node's degree is smaller than the degree of its neighbors"
            },
            {
                    "_id" : "D",
                    "value" : "node degree =4 , this node's degree is >= the degree of all of its neighbors"
            },
            {
                    "_id" : "A",
                    "value" : "this node's degree is smaller than the degree of its neighbors"
            },
            {
                    "_id" : "G",
                    "value" : "this node's degree is smaller than the degree of its neighbors"
            },
            {
                    "_id" : "B",
                    "value" : "node degree =4 , this node's degree is >= the degree of all of its neighbors"
            },
            {
                    "_id" : "F",
                    "value" : "this node's degree is smaller than the degree of its neighbors"
            },
            {
                    "_id" : "E",
                    "value" : "this node's degree is smaller than the degree of its neighbors"
            }
    ],
    "ok" : 1
}

//11) (Extra Credit, 10% of the homework grade) Consider the graph in the previous question. Find any subgraphs of three nodes that match the pattern (x1:Faculty)-(x2:Course)-(x3:Student)

//Expected output
{
    "results" : [
            {
                    "_id" : "A",
                    "value" : "no match found"
            },
            {
                    "_id" : "D",
                    "value" : {
                            "matches_found" : [
                                    "(C:Faculty)-(D:Course)-(E:Student)",
                                    "(B:Faculty)-(D:Course)-(E:Student)"
                            ]
                    }
            },
            {
                    "_id" : "C",
                    "value" : "no match found"
            },
            {
                    "_id" : "E",
                    "value" : "no match found"
            },
            {
                    "_id" : "G",
                    "value" : "no match found"
            },
            {
                    "_id" : "B",
                    "value" : "no match found"
            },
            {
                    "_id" : "F",
                    "value" : {
                            "matches_found" : [
                                    "(B:Faculty)-(F:Course)-(G:Student)"
                            ]
                    }
            }
    ],
    "ok" : 1
}