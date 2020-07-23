import pytest
import base64
from os import path
from formfiller import FormFiller
from wand.image import Image

def test_synopsis():
  signature = Image(filename='signature.png')
  sig_b64 = base64.b64encode(signature.make_blob(format='png'))
  print("width={} height={}".format(signature.width, signature.height))
  #assert base64.b64encode(Image(blob=base64.b64decode(sig_b64), format='png').make_blob(format='png')) == sig_b64

  definition = [
    dict(name="iamcircle", x1=140, y1=140, x2=160, y2=160, type="circle"),
    dict(name="iamfill", x1=240, y1=240, x2=260, y2=260, type="fill"),
    dict(name="iam-unused", x1=240, y1=240, x2=260, y2=260, type="fill"),
    dict(name="hello", x1=10, y1=10, x2=20, y2=30, type="draw"),
    dict(name="signature", x1=30, y1=30, x2=200, y2=70, type="overlay"),
  ]

  ff = FormFiller(
    payload={'hello': 'world', 'iamcircle': True, 'iamfill': True, 'signature': "data:image/png;base64," + sig_b64.decode() },
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

  # explicit (extra) overlay
  ff.overlay(sig_b64, left=200, top=10)
  ff.to_file('/tmp/filled-form-signed.png')
  assert path.exists('/tmp/filled-form-signed.png') == True
