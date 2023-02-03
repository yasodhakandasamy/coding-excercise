import glob, os
import pandas as pd
from datetime import datetime

from sqlalchemy import create_engine

"""
create database 'weatherdb' and table 'weather_data'
"""
def create_weatherdb():
    engine = create_engine('mysql+pymysql://root:Admin21$@127.0.0.1')
    conn = engine.connect()

    conn.execute("CREATE database IF NOT EXISTS weatherdb;")
    conn.execute("USE weatherdb;")
    sql = "CREATE TABLE IF NOT EXISTS {} (station_id char(20) not null, date date NOT NULL, max_temp float, min_temp float, rain float, PRIMARY KEY(station_id, date)) ;".format(
        tableName)
    conn.execute(sql)
    conn.close()

"""
Insert Records from text files into weather_data table
station_id (filename), date, max_temp (maximum temperature), min_temp (minimum temperature), rain (amount of precipitation)
"""
def insert_weather_data(path, fileName):

    path = (path + '\\' + fileName)
    df = pd.read_csv(path, sep="\t", header=None, names=['date', 'max_temp', 'min_temp', 'rain'])
    df = df.set_index('date')
    df['station_id'] = fileName[:-4]

    engine = create_engine('mysql+pymysql://root:Admin21$@127.0.0.1/weatherdb')
    conn = engine.connect()
    try:
        rows = df.to_sql(name='weather_data', con=conn, index=True, if_exists='append', chunksize=1000)

    except Exception as ee:
        print("skipping duplicate entries")
        return 0

    """
    replace -9999 with nulls values
    """

    conn.execute("update weather_data set min_temp = NULL where min_temp = -9999")
    conn.execute("update weather_data set max_temp = NULL where max_temp = -9999")
    conn.execute("update weather_data set rain = NULL where rain = -9999")
    conn.close()
    return rows

"""
creating a table for 'weather_stats' in database 'weatherdb'
"""
def create_weather_stats():
    engine = create_engine('mysql+pymysql://root:Admin21$@127.0.0.1/weatherdb')
    conn = engine.connect()

    conn.execute("create table if not exists weather_stats(station_id char(20) not null, year int, avg_min_temp float, avg_max_temp float, total_rain float, primary key(station_id, year))")
    conn.close()
    print("Table weather_stats created successfully!")

"""
calculating the weather stats for avg_max_temp (Average maximum temperature),
avg_min_temp(Average minimum temperature),
tot_rain(Total accumulated precipitation) based on weather data
and insert those records into weather_stats table
"""
def insert_weather_stats(fileName):
    engine = create_engine('mysql+pymysql://root:Admin21$@localhost/weatherdb')
    conn = engine.connect()
    for year in range(1985,2015):
        sql = "select avg(max_temp)/10 as max_temp from weather_data where year(date)={} and station_id='{}'".format(year,fileName[:-4])
        avg_max_temp = conn.execute(sql).fetchall()[0][0]

        sql = "select avg(min_temp)/10 as min_temp from weather_data where year(date) = {} and station_id='{}'".format(year,fileName[:-4])
        avg_min_temp = conn.execute(sql).fetchall()[0][0]

        sql = "select sum(rain)/10 from weather_data where year(date) = {} and station_id='{}'".format(year,fileName[:-4])
        tot_rain = conn.execute(sql).fetchall()[0][0]

        if avg_min_temp is None:
            avg_min_temp='NULL'
        if avg_max_temp is None:
            avg_max_temp = 'NULL'
        if tot_rain is None:
            tot_rain = 'NULL'
        stats = (textfile[:-4], year, avg_min_temp, avg_max_temp, tot_rain)
        sql = "insert ignore into weather_stats values('{}',{},{},{},{})".format(stats[0],stats[1],
                    str(stats[2]),stats[3],stats[4])
        conn.execute(sql)

    conn.close()

"""
checking the count no of records in each file
"""
def count_total_records(tableName):
    engine = create_engine('mysql+pymysql://root:Admin21$@127.0.0.1/weatherdb')
    conn = engine.connect()
    records = conn.execute("select count(*) from {}  ;".format(tableName)).fetchall()[0][0]
    return records


if __name__  == "__main__" :
    tableName = "weather_data"
    path = os.getcwd() + r"/wx_data"
    os.chdir(path)
    wx_files = glob.glob('*.txt')
    print("Files in current directory:")
    print(wx_files)
    create_weatherdb()
    create_weather_stats()
    tot_records = 0
    for textfile in wx_files:

        start_time = datetime.now()
        print("starting data injection of file {} at ".format(textfile), start_time,"seconds")
        
        """Weather data method calling"""
        
        count=insert_weather_data(path, textfile)

        end_time = datetime.now()
        print("reached end of data injection at ", end_time, "seconds")
        print("time taken for data injection from file is %.3f"%(end_time.timestamp() - start_time.timestamp()), "seconds")
        print(count, " records inserted from file", textfile)
        tot_records=count_total_records("weather_data")
        print(tot_records," total number of records in database")
        print()
        
        """Weather stats method calling"""
        
        insert_weather_stats(textfile)


