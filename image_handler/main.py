import textwrap

from PIL import Image, ImageDraw, ImageFont

from rest_app.utils.yaml_reader import read_yaml


if __name__ == '__main__':
    cf = read_yaml("../config.yaml")

    with Image.open('C:/Users/andre/Documents/testProjectUrbantech/upload_files/дерево_ферма_goatherd.jpg') as img:
        img.load()
    width, height = img.size
    img = img.crop((0, 0, width, height+100))
    pencil = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(cf.get('FONT'), size=20)
    except OSError as e:
        print(e)
    text = 'Test Textfldjnf fffffffffffff fffffffffffff aaaaaaaaaaa bbbbbbbbbbbbbbbbbbb ccccccccccccc fffffffffffff ffffffffffff'
    margin = 0
    offset = height
    for line in textwrap.wrap(text, width=75):
        pencil.text(
            (margin, offset),
            line,
            font=font,
            fill=('white')
        )
        offset += 25

    img.show()
