import pytest
from os import path
from formfiller import FormFiller

def test_synopsis():
  definition = [
    dict(name="iamcircle", x1=140, y1=140, x2=160, y2=160, type="circle"),
    dict(name="hello", x1=10, y1=10, x2=20, y2=30, type="draw"),
  ]
  ff = FormFiller(
    payload={'hello': 'world', 'iamcircle': True},
    image='test-base-image.png',
    form=definition
  )
  #print("base64 image: {}".format(ff.as_base64()))
  try:
    utf8_str = ff.as_base64().decode()
  except (UnicodeDecodeError, AttributeError):
    pass

  ff.to_file('/tmp/filled-form.png')
  assert path.exists('/tmp/filled-form.png') == True

