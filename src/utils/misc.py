from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from utils.constants.images import IMAGE_PATH, FONTS_PATH


def num_emoji(n: int) -> str:
    """Returns the emoji of the given number"""

    emojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    return "".join(emojis[int(i)] for i in str(n))


def xp_bar(percentage: float, level: int) -> BytesIO:
    """Returns the xp bar image"""

    # load the images
    xp_full = Image.open(IMAGE_PATH + "xp_bar_full.png")
    xp_empty = Image.open(IMAGE_PATH + "xp_bar_empty.png")

    # get the size of the image
    width, height = xp_full.size

    # crop the image at the given percentage
    cropped_width = int(width * percentage)

    # crop the image
    xp_full = xp_full.crop((0, 0, cropped_width, height))
    xp_empty = xp_empty.crop((cropped_width, 0, width, height))

    # paste the cropped image on the other image
    new_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    new_image.paste(xp_full, (0, 0))
    new_image.paste(xp_empty, (cropped_width, 0))

    # draw the number
    return draw_number(new_image, str(level))


def draw_number(image, number: int) -> BytesIO:
    """Draws a number on the image of the xp bar"""

    # load the font
    font = ImageFont.truetype(FONTS_PATH + "minecraft_font.ttf", size=14)

    # get the size of the text
    text_size = font.getsize(number)

    # calculate the position of the text
    text_x = (image.width - text_size[0]) / 2
    text_y = (image.height - text_size[1]) / 2 - 7

    # draw the text on the image
    draw = ImageDraw.Draw(image)
    draw.text((text_x + 2, text_y + 2), number, font=font, fill=(32, 64, 0))
    draw.text((text_x, text_y), number, font=font, fill=(127, 255, 0))

    # Save the image as a BytesIO object
    image_binary = BytesIO()
    image.save(image_binary, "PNG")
    image_binary.seek(0)

    return image_binary


def xp_to_next_level(current_level: int) -> int:
    """Returns the amount of xp needed to reach the next level"""
    return 500 * (current_level**2) + 500 * current_level
