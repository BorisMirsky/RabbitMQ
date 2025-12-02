import json


{
"measuring": "temperature",
 "timestamp": "2023-01-21T02:05:55.000Z ",
  "device": [
{
    "device_id": 4123,
    "value": 69.67,
    "status": "OK"
},
{
    "device_id": 587,
    "value": 19.67,
    "status": "ERROR"
},
{
    "device_id": 1524,
    "value": 123,
    "status": "ERROR"
},
{
    "device_id": 97,
    "value": 70,
    "status": "OK"
}
]
}



{
"measuring": "pressure",
 "timestamp": "2023-01-21T02:05:55.000Z ",
  "device": [
{
    "device_id": 4123,
    "value": 9.67,
    "status": "OK"
},
{
    "device_id": 587,
    "value": 1.03,
    "status": "ERROR"
},
{
    "device_id": 1524,
    "value": 6.34,
    "status": "OK"
},
{
    " device_id": 97,
    "value": 0.21,
    "status": "ERROR"
}
]
}

  
json_string = json.dumps('temperature', indent=4) # indent for pretty-printing
#json_string1 = json.dumps(pressure, indent=4)
print(json_string)
