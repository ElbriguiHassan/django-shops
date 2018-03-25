# API endpoints #


**User Sign Up endpoint**
----

* **URL**

  `localhost:8000/users/`

* **Method:**

  `POST`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:**

```javascript
{
    "id": 1,
    "email": "hassanelbrigui@test.com",
    "last_login": null,
    "is_superuser": false,
    "is_staff": false,
    "date_joined": "2018-03-25T01:27:38.128337Z",
    "last_seen": null,
    "updated_at": "2018-03-25T01:27:38.128378Z",
    "groups": [],
    "user_permissions": []
}
```

**User Sign In endpoint**
----

* **URL**

  `localhost:8000/sign-in/`

* **Method:**

  `POST`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:**

```javascript
{
    "id": 1,
    "key": "12bf925459f167624fef44470e937dbd6bf35d88",
    "email": "hassanelbrigui@test.com"
}
```