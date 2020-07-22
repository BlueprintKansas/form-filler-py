from wand.image import Image
from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color
import base64

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

    self.fill()

  def fill(self):
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

        if def_type == 'draw':
          self.__fill_draw(draw, definition)
        elif def_type == 'fill':
          self.__fill_fill(draw, definition)
        elif def_type == 'circle':
          self.__fill_circle(draw, definition)
        else:
          raise ValueError("unknown definition type: {}".format(def_type))

      # stash the drawn image while we have the objects in scope
      with Image(filename=self.image) as image:
        draw(image)
        self.drawn = image.make_blob(format='png')

  def __fill_draw(self, draw, definition):
    draw.text(definition['x1'], definition['y2'], self.payload[definition['name']])

  def __fill_fill(self, draw, definition):
    x1 = definition['x1']
    x2 = definition['x2']
    y1 = definition['y1']
    y2 = definition['y2']
    draw.rectangle(left=x1, top=y1, right=x2, bottom=y2)

  def __fill_circle(self, draw, definition):
    x1 = definition['x1']
    x2 = definition['x2']
    y1 = definition['y1']
    y2 = definition['y2']
    prev_stroke = draw.stroke_color
    draw.stroke_color = Color(self.font_color)
    draw.circle((x1, y1), (x2, y2))
    draw.stroke_color = prev_stroke

  def as_base64(self):
    return base64.b64encode(self.as_png())

  def as_png(self):
    return self.drawn

  def as_image(self):
    return Image(blob=self.drawn, format='png')

  def to_file(self, filename):
    return self.as_image().save(filename=filename)

