import datetime
from functools import lru_cache
from random import Random
from PIL import Image, ImageDraw, ImageFont
from .get_file import get_image, get_file
from ..settings import RESOURCE

@lru_cache(None)
def _get(date: datetime.date):
    print('nocache')
    rand = Random()
    rand.seed(date.ctime())
    
    temperature = str(round(rand.uniform(-16, 48), 1)) + "°C"

    weather = get_image(rand.choice(RESOURCE.RURU_WEATHER['weather'])).resize((500, 500), Image.ANTIALIAS)

    appropriateness = [
        rand.choice(RESOURCE.RURU_WEATHER['appropriateness']),
        rand.choice(RESOURCE.RURU_WEATHER['appropriateness'])
    ]

    season = get_image(RESOURCE.RURU_WEATHER['season'][[
        '',
        'winter', 
        'winter', 
        'spring', 
        'spring', 
        'spring', 
        'summer', 
        'summer', 
        'summer', 
        'autumn', 
        'autumn', 
        'autumn', 
        'winter'
    ][date.month]]).resize((1877, 1251))
    # 3755 * 2502

    season.paste(weather, (season.size[0] - weather.size[0] + 100, -100), weather)

    draw = ImageDraw.Draw(season)

    font_text = ImageFont.truetype(get_file("http://bnkjbms.test.upcdn.net/font/Alibaba-PuHuiTi-Bold.ttf"), size=100)
    font_temp = ImageFont.truetype(get_file("http://bnkjbms.test.upcdn.net/font/Alibaba-PuHuiTi-Bold.ttf"), size=200)
    
    text_color = (255, 255, 255)
    shadow_color = (100, 100, 100)

    draw.text((50, 50), "长颈鹿的虚拟草原天气", text_color, font=font_text, stroke_fill=shadow_color, stroke_width=10)

    temperature_size = font_temp.getsize(temperature)
    draw.text(((season.size[0] - temperature_size[0]) / 2, (season.size[1] - temperature_size[1]) / 2), temperature, text_color, font=font_temp, stroke_fill=shadow_color, stroke_width=10)

    draw.text((50, season.size[1] - 150), f"今日宜：{appropriateness[0]}", text_color, font=font_text, stroke_fill=shadow_color, stroke_width=10)

    return season

def get_weather_image():
    return _get(datetime.date.today())