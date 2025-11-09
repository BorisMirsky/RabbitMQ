from fastapi import FastAPI, Request
from datetime import datetime
from middleware import Tracker
from sender import sender
import json
app = FastAPI()


@app.middleware("tracker")
async def tracker(request: Request, call_next):
    service_tracker = Tracker("service_one")
    tracker = str(service_tracker.visitor_tracker(request))

    sender(tracker)
    print(tracker)
    response = await call_next(request)

    return response


@app.get("/")
def index():
    return "Hello, world"

@app.get("/json")
def some_func():
    return {
        "some_json": "Some Json"
    }



if __name__ == "__main__":
    app.run(debug=True)
