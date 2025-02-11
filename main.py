from PIL import Image, ImageDraw
import hashlib
import random
import math
import os
from datetime import datetime

imageX = 64
imageY = 64
# Example usage
words = ["foo","live laugh love", "girlfriend", "dog's name"]

def create_image(seed_text):


    # Use each letter of the input text to generate a separate SHA-256 seed
    individual_seeds = [
        hashlib.sha256(letter.encode()).hexdigest() for letter in seed_text
    ]

    # Concatenate all individual seeds to form the full seed
    full_seed = "".join(individual_seeds)

    # Set block size
    block_size = (19, 19)

    # Calculate the number of segments based on the updated hash length
    num_segments = len(full_seed) // 3

    # Create a new image
    image = Image.new(
        "RGB", (imageX * block_size[0], imageY * block_size[1]), "white"
    )
    draw = ImageDraw.Draw(image)

    # Draw blocks with a mix of seed for colors
    for x in range(0, imageX):
        for y in range(0, imageY):
            block_x = x * block_size[0]
            block_y = y * block_size[1]

            # Determine the range of seed characters for the current block
            start_index = (x + y * imageX) % num_segments * 3
            end_index = start_index + 3

            # Use the current 3-digit part of the seed as seeds for the SHA-256 algorithm
            seed_for_sha256 = full_seed[start_index:end_index].encode()
            new_seed = hashlib.sha256(seed_for_sha256).hexdigest()

            # Use the new seed as a seed for generating a random color
            pixelColor = tuple(int(new_seed[i : i + 2], 16) for i in (0, 2, 4))

            draw.rectangle(
                [block_x, block_y, block_x + block_size[0], block_y + block_size[1]],
                fill=pixelColor,
            )

    # Save the image
    # image.save(output_path)
    return image


def draw_shapes(image, seed_text):
    shapes_seed = int(hashlib.sha256(seed_text.encode()).hexdigest(), 16)

    random.seed(shapes_seed)
    num_shapes = random.randint(5, 10)  # Number of shapes
    print("numshapes:", num_shapes)

    for _ in range(num_shapes):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Shape type (0: circle, 1: line, 2: cross, 3: triangle, 4: rectangle, 5-9: additional polygons)
        shape_type = random.randint(0, 12)
        print("type:", shape_type)

        # Coordinates and size of the shape
        x = random.randint(0, image.width - 1)
        y = random.randint(0, image.height - 1)
        size = random.randint(int(imageX), 10*int(imageX))

        # Draw the shape
        if shape_type == 0:
            draw_circle(image, x, y, size, color)
        elif shape_type == 1:
            draw_line(image, x, y, size, color)
        elif shape_type == 2:
            draw_cross(image, x, y, size, color)
        elif shape_type == 3:
            draw_triangle(image, x, y, size, color)
        elif shape_type == 4:
            draw_rectangle(image, x, y, size, color)
        elif shape_type in range(5, 10):
            draw_polygon(image, x, y, size, color, sides=shape_type)

    return image


def draw_circle(image, x, y, size, color):
    draw = ImageDraw.Draw(image)
    draw.ellipse([x, y, x + size, y + size], fill=color)


def draw_line(image, x, y, size, color):
    draw = ImageDraw.Draw(image)
    draw.line([x, y, x + size, y + size], fill=color, width=random.randint(10,50))


def draw_cross(image, x, y, size, color):
    draw = ImageDraw.Draw(image)
    draw.line([x, y, x + size, y + size], fill=color, width=random.randint(10,50))
    draw.line([x, y + size, x + size, y], fill=color, width=random.randint(10,50))


def draw_triangle(image, x, y, size, color):
    draw = ImageDraw.Draw(image)
    draw.polygon(
        [(x, y), (x + size, y), (x + size // 2, y + size)], fill=color
    )


def draw_rectangle(image, x, y, size, color):
    draw = ImageDraw.Draw(image)
    draw.rectangle([x, y, x + size, y + size], fill=color)


def draw_polygon(image, x, y, size, color, sides=5):
    print("draw poly: ", sides)
    draw = ImageDraw.Draw(image)
    angle = 360 / sides
    points = []
    for i in range(sides):
        angle_rad = i * angle * (3.141592653589793 / 180)
        point_x = x + size * 0.5 * math.cos(angle_rad)
        point_y = y + size * 0.5 * math.sin(angle_rad)
        points.append((point_x, point_y))
    draw.polygon(points, fill=color)


def generate_images_for_word(name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = str(imageX)+ "x" + str(imageY)
    if not os.path.exists(folder):
        os.mkdir(folder)
    # Original version
    output_path_original = folder+"/"+f"{timestamp}_{name}_small.png"
    image1 = create_image(name)
    final_image = draw_shapes(image1, name)
    image1.save(output_path_original)

    # Capitalized version
    capitalized_name = name.capitalize()
    output_path_capitalized = folder+"/"+f"{timestamp}_{capitalized_name}_cap.png"
    image2 = create_image(capitalized_name)
    final_image = draw_shapes(image2, capitalized_name)
    image2.save(output_path_capitalized)

    # Uppercase version
    uppercase_name = name.upper()
    output_path_uppercase = folder+"/"+f"{timestamp}_{uppercase_name}_up.png"
    image3 = create_image(uppercase_name)
    final_image = draw_shapes(image3, uppercase_name)
    image3.save(output_path_uppercase)


for word in words:
    generate_images_for_word(word)
