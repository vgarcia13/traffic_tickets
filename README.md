# Traffic Ticket API Implementation

## How to install?
### Using Docker Hub
Pre requisites: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Run `docker pull vgarcia13/traffic_tickets:latest`
* Finally, run `docker run -it -p 8000:8000 vgarcia13/traffic_tickets`
* Navigate to [http://0.0.0.0:8000/api/](http://0.0.0.0:8000/api/) to access API root.

### Using Docker
Pre requisites: [Docker Desktop](https://www.docker.com/products/docker-desktop/)

* Clone this repository
* Access the repo's root folder `/traffic_tickets`
* Run `docker build -t traffic_tickets .` to build and create the container.
* Finally, run `docker run -it -p 8000:8000 traffic_tickets` to run the container.
* Navigate to [http://0.0.0.0:8000/api/](http://0.0.0.0:8000/api/) to access API root.


### Using Virtualenv
* Clone this repository
* Access the repo's root folder `/traffic_tickets`
* Run `python3 -m venv venv` to create a brand new virtual env,
* Run `source venv/bin/activate` to activate te virtual env.
* Run `pip install -r requirements.txt` to install project's dependencies.
* Run `python manage.py migrate` to apply current model into DB (sqlite)
* Finally, run `python manage.py runserver 0.0.0.0:8000` to run Django server
* Navigate to [http://0.0.0.0:8000/api/](http://0.0.0.0:8000/api/) to access API root.

## How to use?

### Administration site
#### Accessing the administration site
##### * Docker
* To access administration site, first run `docker container ls` and extract the `Container ID` 
related to `traffic_tickets` image.
* Run `docker exec -it <CONTAINER_ID> python manage.py createsuperuser` and type a username and password.
* Navigate to [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/) with the credentials created.

##### * Virtualenv
* To access administration site, run `python manage.py createsuperuser` (with `venv` activated) and type 
a username and password.
* Navigate to [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/) with the credentials created.

#### Create a `Person` instance
* Within the admin site, click `"Add"` button right after `"Persons"`
* You need to create a `User` instance first (used for access token generation), click the `"+"` button in the `"User"` row 
and type the email of the `Person` to create in the `Username` field, nothing else is required here.
* After the `User` creation, type the `Person` email (used in the last step) and the full name, and click "Save"

`Person` instance is the base model for `Officer` and `Vehicle` creation.

#### Create an access token
* Within the admin site, click `"Add"` button right after `"Token"`
* Select the related `User`
* Click `"Save"`

The generated token is the access token related to the `Person` related to the selected `User`

#### Create an `Officer` instance
* Within the admin site, click `"Add"` button right after `"Officer"`
* Select the `Person` related to the `Officer` to be created.
* Click `"Save"`

#### Create a `Vehicle` instance
* Within the admin site, click `"Add"` button right after `"Vehicle"`
* Select the `Person` related to the `Vehicle` to be created and fill all the other values.
* Click `"Save"`

#### Create a `Ticket` instance
* Within the admin site, click `"Add"` button right after `"Ticket"`
* Select the `Vehicle` related to the `Ticket` to be created and the `Officer` that is creating the ticket. `Notes`
field is optional.
* Click `"Save"`

**NOTE:** This process is not intended to be done in the admin site, there is an endpoint
available for this.

CRUD operations are fully supported.

### API Instance
#### Accessing the API instance
* Navigate to [http://0.0.0.0:8000/api/](http://0.0.0.0:8000/api/) with the credentials created.
* All CRUD operations in all the instances described above are supported here.

**NOTE:** Processes have been simplified in the API instance for a more intuitive use.

**EX:** When creating a `Person` within the API instance, a `Token` is created automatically.

Forms are rendered to create new records and accessing elements using `GET` with the unique record `UUID`,
`PUT`, `PATCH` and `DELETE` operations are supported.

**EX:**
```
http://0.0.0.0:8000/api/persons/<PERSON_UUID>/
http://0.0.0.0:8000/api/vehicles/<VEHICLE_UUID>/
http://0.0.0.0:8000/api/officers/<OFFICER_UUID>/
http://0.0.0.0:8000/api/tickets/<TICKET_UUID>/
```


#### `create_ticket` endpoint
* For creating a ticket, a `POST` request needs to be done to [http://0.0.0.0:8000/api/tickets](http://0.0.0.0:8000/api/tickets)
using a `body` like this:

```
{
    "plate": "<VEHICLE_PLATE>,
    "notes": "<NOTES>
}
```

This request needs to be done with an `Authorization` header, like:

```
Authorization: Token <PERSON_ACCESS_TOKEN>
```

* If the plate is not found, a 404 status will be returned.
* If the access_token is not found or is invalid, a 401 status will be returned.
* The ticket's `timestamp` is saved by default using `datetime.now()`

#### `generate_inform` endpoint
* For generating an inform (a JSON with the tickets related to a specific `Person`), a `GET` request needs to be done to [http://0.0.0.0:8000/api/generate_inform](http://0.0.0.0:8000/api/generate_inform)
using a `query_param` like this:

```
http://0.0.0.0:8000/api/generate_inform/?email=<PERSON_EMAIL>
```

This request don't need authorization.


