from wand.image import Image
from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color
import base64
import re

class FormFiller(object):
  def __init__(self, payload, form, image, font='Arial', font_size=24, font_color='blue'):
    if not isinstance(form, list):
      raise ValueError('form must be a list of field definitions')

    self.payload = payload
    self.form = form
    self.image = image
    self.font = font
    self.font_size = font_size
    self.font_color = font_color

    self.__fill()

  def __fill(self):
    # overlays must wait till after initial image is drawn, so just track if we need it.
    has_overlays = False

    # set up base image
    with Drawing() as draw:
      draw.font = self.font
      draw.font_size = self.font_size
      draw.fill_color = Color(self.font_color)

      #print("font={} family={} resolution={} stretch={} style={} weight={}".format(draw.font, draw.font_family, draw.font_resolution, draw.font_stretch, draw.font_style, draw.font_weight))

      # iterate over form definitions
      for definition in self.form:
        def_type = definition['type']

        if definition['name'] not in self.payload:
          continue

        if not self.payload[definition['name']]:
          continue

        #print("filling {}".format(definition['name']))

        if def_type == 'draw':
          self.__fill_draw(draw, definition)
        elif def_type == 'fill':
          self.__fill_fill(draw, definition)
        elif def_type == 'circle':
          self.__fill_circle(draw, definition)
        elif def_type == 'enclose':
          self.__fill_enclose(draw, definition)
        elif def_type == 'overlay':
          has_overlays = True
        else:
          raise ValueError("unknown definition type: {}".format(def_type))

      # stash the drawn image while we have the objects in scope
      if isinstance(self.image, Image):
        draw(self.image)
        self.drawn = self.image.make_blob(format='png')
      else:
        with Image(filename=self.image) as image:
          draw(image)
          self.drawn = image.make_blob(format='png')

    if has_overlays:
      for definition in self.form:
        if definition['type'] != 'overlay':
          continue
        self.__fill_overlay(definition)

    # image fully drawn

  def __fill_draw(self, draw, definition):
    draw.text(definition['x1'], definition['y2'], self.payload[definition['name']])

  def __fill_fill(self, draw, definition):
    x1 = definition['x1']
    x2 = definition['x2']
    y1 = definition['y1']
    y2 = definition['y2']
    draw.rectangle(left=x1, top=y1, right=x2, bottom=y2)

  def __fill_enclose(self, draw, definition):
    x1 = definition['x1']
    x2 = definition['x2']
    y1 = definition['y1']
    y2 = definition['y2']
    prev_fill = draw.fill_color
    prev_stroke = draw.stroke_color
    draw.stroke_color = Color(self.font_color)
    draw.fill_color = Color('transparent') # TODO optional?
    draw.rectangle(left=x1, top=y1, right=x2, bottom=y2)
    draw.stroke_color = prev_stroke
    draw.fill_color = prev_fill

  def __fill_circle(self, draw, definition):
    x1 = definition['x1']
    x2 = definition['x2']
    y1 = definition['y1']
    y2 = definition['y2']
    prev_stroke = draw.stroke_color
    draw.stroke_color = Color(self.font_color)
    prev_fill = draw.fill_color
    draw.fill_color = Color('transparent') # TODO optional?
    center_y = (y1 + y2) / 2
    center_x = (x1 + x2) / 2
    draw.circle((center_x, center_y), (x1, center_y))
    draw.stroke_color = prev_stroke
    draw.fill_color = prev_fill

  def __fill_overlay(self, definition):
    base64encoded_img_with_mime = str(self.payload[definition['name']])
    matches = re.fullmatch(r"(data:image/(.+?);base64),(.+)", base64encoded_img_with_mime, re.I)
    if not matches:
      raise ValueError("overlay requires a 'data:image/<type>;base64,' prefix")

    mime_type = matches.group(1)
    image_format = matches.group(2)
    base64encoded_img = matches.group(3)
    #print("mime={} image_format={} b64={}".format(mime_type, image_format, base64encoded_img[0:10]))
    overlay = Image(blob=base64.b64decode(base64encoded_img), format=image_format)

    # optionally resize overlay if necessary
    target_width = definition['x2'] - definition['x1']
    target_height = definition['y2'] - definition['y1']
    if overlay.width > target_width or overlay.height > target_height:
      overlay.resize(width=target_width, height=target_height)

    self.overlay(base64.b64encode(overlay.make_blob(format='png')), top=definition['y1'], left=definition['x1'])

  def as_base64(self):
    return base64.b64encode(self.as_png())

  def as_png(self):
    return self.drawn

  def as_image(self):
    return Image(blob=self.drawn, format='png')

  def to_file(self, filename):
    return self.as_image().save(filename=filename)

  def overlay(self, base64_encoded_string, format='png', left=0, top=0):
    binary_overlay = base64.b64decode(base64_encoded_string)
    with Image(blob=binary_overlay, format=format) as overlay_image:
      original_image = self.as_image()
      original_image.composite(overlay_image, left=left, top=top)
      self.drawn = original_image.make_blob(format='png')

