# KUETBitFestPreli

# Installation

- Clone the repository.
- Create a virtual environment `python3 -m venv envname` and activate it.
- Install the requirements `pip install -r requirements.txt`.


# CHALLENGE 2

# API DOC

- Route: `/ingredients`
- Method: `GET`
- Sample Response:

```json
[
  {
    "name": "egg",
    "quantity": 2,
    "id": 1,
    "unit": "pieces"
  },
  {
    "name": "suger",
    "quantity": 2,
    "id": 2,
    "unit": "kg"
  },
  {
    "name": "raw fish",
    "quantity": 2,
    "id": 3,
    "unit": "pieces"
  },
  {
    "name": "avocado",
    "quantity": 2,
    "id": 4,
    "unit": "pieces"
  },
  {
    "name": "cucumber",
    "quantity": 2,
    "id": 5,
    "unit": "kg"
  }
]
```

- Route: `/ingredients`
- Method: `POST`
- Sample Payload:

```json
{
  "name": "egg",
  "quantity": 2,
  "unit": "pieces"
}
```

- Route: `/recipes`
- Method: `POST`
- Sample Payload:

```json
// Here all the fields are optional except name and ingredients.
{
  "name": "Pudding Cake",
  "taste": "Sweet & Soft",
  "reviews": "I like the pudding so much its so soft to eat",
  "cuisineType": "Bangladeshi",
  "preparationTime": "1 Hour",
  "ingredients": ["egg", "water", "suger"],
  "instructions": "First boil water, theÏn mix eggs and suger and rotate them. Then puth them in the stove for some time. Then Cut and enjoy."
}
```

- Route: `/recipes`
- Method: `GET`
- Sample Response:

```json
{
  "query": "I want to make a pudding"
}
```