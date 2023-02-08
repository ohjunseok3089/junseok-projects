import sqlite3

def query_room_type(cursor):
    sql = "SELECT * FROM room"
    cursor.execute(sql)
    return cursor.fetchall()

def main(cursor, conn):
    result_query = "SELECT area.area, COUNT(place.id) as overall_count, "
    create_table_query = "CREATE TABLE IF NOT EXISTS area_room_type (area text, overall_count integer)"
    
    rows = query_room_type(cursor)
    room_types = rows
    rowslen = len(rows)
    
    cursor.execute("DROP TABLE IF EXISTS area_room_type")
    cursor.execute(create_table_query)
    for i in range(len(rows)):
        row = rows[i]
        fetch_format = "COUNT(case when place.room_type_id = " + str(row[0]) + " then 1 end) as '" + row[1].replace(" ", "_") + "'"
        create_format = "ALTER TABLE area_room_type ADD " + "`" + row[1].replace(" ", "_") + "_count` integer;"
        cursor.execute(create_format)
        if (i != rowslen - 1):
            fetch_format += ", "
        else:
            fetch_format += " "
        result_query += fetch_format
    
    result_query += """FROM area JOIN neighbourhood ON area.area_id = neighbourhood.area_id
        JOIN place ON neighbourhood.neighbourhood_id = place.neighbourhood_id
        GROUP BY area.area;"""

    # print(result_query)
    # print(create_table_query)

    rows = cursor.execute(result_query).fetchall()
    for row in rows:
        insert_query = "INSERT INTO area_room_type (\'area\', \'overall_count\', "
        for i in range(len(room_types)):
            val = str(room_types[i][1]).replace(" ", "_")
            insert_query = insert_query + "\'" + val + "_count\'"
            if (i != len(room_types) - 1):
                insert_query += ", "
            else:
                insert_query += ")"
        insert_query += " VALUES (\'"
        for i in range(len(row)):
            val = row[i]
            insert_query += str(row[i])
            if (i == 0): insert_query += "\'"
            if (i != len(row) - 1):
                insert_query += ", "
            else:
                insert_query += ")"
        # print(insert_query)
        cursor.execute(insert_query)
        conn.commit()
        
if __name__ == "__main__":
    connection = sqlite3.connect("./airbnb.db")
    connection.text_factory = str
    cursor = connection.cursor()
    main(cursor, connection)
    cursor.close()
    connection.close()