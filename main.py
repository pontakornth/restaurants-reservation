from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel


class Reservation(BaseModel):
    name: str
    time: int
    table_number: int


client = MongoClient('mongodb://localhost', 27017)

db = client["exceed_restaurant"]

collection = db["reservation"]

app = FastAPI()


# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name: str):
    result = collection.find({'name': name}, {'_id': 0})
    reservation_list = []
    for r in result:
        reservation_list.append(r)
    return {
        'reservations': reservation_list
    }


@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    pass


@app.post("/reservation")
def reserve(reservation: Reservation):
    pass


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    pass
