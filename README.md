Form-Filler
=========================

[![Build Status](https://travis-ci.org/BlueprintKansas/form-filler-py.svg?branch=main)](https://travis-ci.org/BlueprintKansas/form-filler-py)

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
  font='path/to/font.ttf', # default Arial
  font_color='blue', # default
  font_size=24 # default
)

print("base64 image: {}".format(ff.as_base64()))
ff.to_file('/tmp/filled-form.png')
```

# Copyright and License

MIT license.

Copyright 2020 Blueprint Kansas
