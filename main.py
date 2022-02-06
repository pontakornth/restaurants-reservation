import datetime

from fastapi import FastAPI, Query, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import datetime


class Reservation(BaseModel):
    name: str
    time: datetime.datetime
    table_number: int


client = MongoClient('mongodb://localhost', 27017)

db = client["exceed_restaurant"]

collection = db["reservation"]

app = FastAPI()


@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name: str):
    result = collection.find({'name': name}, {'_id': 0})
    reservation_list = []
    for r in result:
        reservation_list.append(r)
    return {
        'reservations': reservation_list
    }


@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    result = collection.find({'table_number': table}, {'_id': 0})
    reservation_list = [r for r in result]
    return {
        'reservations': reservation_list
    }


@app.post("/reservation")
def reserve(reservation: Reservation):
    if reservation.table_number < 1 or reservation.table_number > 12:
        raise HTTPException(400, {'status': 'bad request', 'error': 'table must be in 1 to 12.'})
    existing_reservation = collection.find_one({'time': reservation.time, 'table_number': reservation.table_number})
    if existing_reservation:
        return HTTPException(409, {'status': 'conflict', 'error': 'Reservation already exists'})
    collection.insert_one({
        'name': reservation.name,
        'time': reservation.time,
        'table_number': reservation.table_number
    })
    return {'status': 'created'}


@app.put("/reservation/update/{name}/{table_number}")
def update_reservation(name: str, table_number: int, reservation: Reservation):
    pass


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    query = collection.delete_one({ "name" : name , "table_number" : table_number })
    return {"result" : "done" ,}
