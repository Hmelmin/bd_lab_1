#from mysql import connector
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.code import Code
from . import cache
import time
from bson.son import SON
import datetime

class DatabaseManager:
    def __init__(self):
        self.connector = MongoClient('localhost',27017)
        self.db = self.connector.lab2


    def close(self):
        self.connector.close()




    def SelectAllFlights(self):
        get_flights = self.db.Flights.find()
        return get_flights



    def SelectFlightById(self,id):
        get_flight = self.db.Flights.find_one({"_id":ObjectId(id)})
        return get_flight

    def SelectFlightByTime(self,time):
        get_flight = self.db.Flights.find_one({"time":time})
        return get_flight




    def InsertFlight(self, airlines, departure, destination, plane, time_out,passengers):
        set_flight = {"departure":{"city":departure},
                      "destination":{"city":destination},
                      "plane":{"name":plane},
                      "airlines":{"name":airlines},
                      "date":time_out,
                      "passengers":int(passengers)}
        insertion = self.db.Flights.insert_one(set_flight)


    def InsertFlightTemp(self, airlines, departure, destination, plane, time_out,passengers,time):
        set_flight = {"departure":{"city":departure},
                      "destination":{"city":destination},
                      "plane":{"name":plane},
                      "airlines":{"name":airlines},
                      "date":time_out,
                      "passengers":int(passengers),
                      "time":time}
        insertion = self.db.Flights.insert_one(set_flight)


    def DeleteFlight(self,id):
        self.db.Flights.remove({"_id":ObjectId(id)})


    def EditFlight(self, id,   departure, destination, plane,airlines,passengers):
        self.db.Flights.update_one({"_id":ObjectId(id)},{"$set":{"departure":{"city":departure},
                                                                "destination":{"city":destination},
                                                                "plane":{"name":plane},
                                                                "airlines":{"name":airlines},
                                                                 "passengers":int(passengers)}})

    def SearchSelect(self,date ):

        print(len(date))
        print(date)
        if len(date)>0:
            if cache.is_key_present(date):
                start = time.clock()
                flights =  cache.get_from(date)
                finish = time.clock()
                print flights
                print"FROM CACHE!!!!!!!!"
                print finish - start
            else:
                start = time.clock()
                results= self.db.Flights.find({"date": date})
                finish=time.clock()
                query = []
                flights=[]
                for item in results:
                    query.append(item)
                    flights.append(item)
                cache.set_from(date,query)
                print "FROM DB!"
                print finish-start
                for item in flights:
                    print item
        else:
            flights = self.db.Flights.find({})

        # for item in flights:
        #     print (item)
        return flights





    def mapreduce1(self):
        mapper = Code("function () { emit(this.airlines.name, this.passengers);}")
        reducer = Code("function(key,value) {return Array.sum(value);}")
        result = self.db.Flights.map_reduce(mapper,reducer,"results")
        for item in result.find():
            print item
        return result


    def mapreduce2(self):
        mapper = Code("function () { emit(this.destination.city, this.passengers);}")
        reducer = Code("""function(key,value) {var max = value[0];
                    value.forEach(function(val){
                    if (val > max) max = val;
                    })
                    return max;}""")
        result = self.db.Flights.map_reduce(mapper,reducer,"results")
        for item in result.find():
            print item
        return result


    def aggregate(self):
        results = [
        {"$group": {"_id": "$airlines.name", "count": {"$sum": 1}}}]
        #{"$sort": SON([("count", -1), ("_id", -1)])}]
        result =  self.db.Flights.aggregate(results)
        # for item in result:
        #     print item
        return result









#
dm = DatabaseManager()
# #dm.InsertAirport("Ukraine","Lviv")
# #print(dm.GetLastIdFromAirports())
# dm.SelectAllFlights()
# print ('###############3')
# #dm.DeleteFlight('5815e4ca41a571225f93928d')
# #dm.InsertFlight('WizzAir','Oslo','Rome','Boeing747',datetime.datetime(2016,9,16,23,45,55))
# #dm.EditFlight('5815e5618136a2e515350b98','WizzAir','Warshaw','Porto','Boeing747',datetime.datetime(2016, 10, 12, 21, 0))
# dm.SelectAllFlights()
dm.mapreduce1()
print("#################")
dm.mapreduce2()
print("#################")
dm.aggregate()
dm.close()
#
