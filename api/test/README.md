### Postman collection methods

There is no automatic tests provided, you can use this collection for Postman to work with requests


```
GET /
```
Show status: clients, routes, updated time (directly from `openvpn-status.log`)

```
POST /create

{
	"name": "test"
}
```

Generates new key-pair for client with given name. Returns certificate id

```
POST /delete

{
	"name": "test"
}
```

Removes new key-pair from CA for client with given name. Returns OK


```
GET /list
```

Returns certificates list with specific parameters