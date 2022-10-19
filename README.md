Form-Filler
=========================

![Build Status](https://github.com/BlueprintKansas/form-filler-py/actions/workflows/pull_request.yml/badge.svg?branch=main)

Form-Filler Python module makes it easy to create completed forms based on a payload of text and a base image.

# Example

```python
from formfiller import FormFiller

form_definition = [
  dict(name="hello", x1=10, y1=10, x2=20, y2=20, type="draw")
]

payload = { 'hello': 'world' }

ff = FormFiller(
  payload=payload,
  image='path/to/base-form-image.png',
  form=form_definition,
  font='path/to/font.ttf', # default Liberation-Sans
  font_color='blue', # default
  font_size=24 # default
)

print("base64 image: {}".format(ff.as_base64()))
ff.to_file('/tmp/filled-form.png')
```

You can also invoke formfiller from the command line:

```shell
% python -m formfiller --form=path/to/form-definition.json --image=path/to/base-form-image.png --payload=path/to/payload.json
```

# Copyright and License

MIT license.

Copyright 2020 Blueprint Kansas
