from PIL import Image, ImageOps
import numpy as np
import random
import os


def get_non_transparent_area(image):
    """
    获取图像中非透明部分的坐标和边界框。
    """
    data = np.array(image)
    alpha_channel = data[:, :, 3]
    non_transparent_indices = np.where(alpha_channel != 0)
    y_min, y_max = non_transparent_indices[0].min(), non_transparent_indices[0].max() + 1
    x_min, x_max = non_transparent_indices[1].min(), non_transparent_indices[1].max() + 1
    return (x_min, y_min, x_max, y_max)


def random_crop_transparent_image(image, min_size=50):
    """
    随机裁剪透明图像的非透明部分，确保裁剪区域不小于min_size。
    """
    x_min, y_min, x_max, y_max = get_non_transparent_area(image)

    crop_width = random.randint(min_size, x_max - x_min)
    crop_height = random.randint(min_size, y_max - y_min)

    x_start = random.randint(0, x_max - crop_width)
    y_start = random.randint(0, y_max - crop_height)

    return image.crop((x_start, y_start, x_start + crop_width, y_start + crop_height))


def stamp_image(target_image_path, stamp_image_path, output_path):
    """
    在目标图像上加盖公章，并保存结果。
    """
    target_image = Image.open(target_image_path).convert("RGBA")
    stamp_image = Image.open(stamp_image_path).convert("RGBA")

    # 获取图像的像素数据
    datas = stamp_image.getdata()

    # 创建一个新的列表来存储修改后的像素数据
    new_data = []

    # 遍历每个像素，调整透明度
    # 假设我们将透明度调整为原始值的一半
    for item in datas:
        r, g, b, a = item
        new_a = int(a * random.uniform(0.1,1))  # 调整透明度
        new_data.append((r, g, b, new_a))

        # 将修改后的像素数据放回图像
    stamp_image.putdata(new_data)


    # 随机裁剪公章的非透明部分
    stamp_crop = random_crop_transparent_image(stamp_image)

    # 获取目标图像的尺寸
    target_width, target_height = target_image.size

    # 计算裁剪后的公章尺寸
    stamp_width, stamp_height = stamp_crop.size

    # 计算公章放置的随机位置，确保不会超出目标图像边界




    # left = random.randint(-50, -10)
    # top = random.randint(-400, -1)

    # 创建目标图像的副本，避免直接修改原始图像
    target_image_copy = target_image.copy()

    # 将裁剪后的公章粘贴到目标图像上，超出部分直接截取
    target_image_copy.paste(stamp_crop, (1, 1), stamp_crop)

    # 保存结果图像，转换为RGB格式去除透明通道
    target_image_copy_rgb = target_image_copy.convert("RGB")
    target_image_copy_rgb.save(output_path)


# 示例使用
# 指定文件夹路径
folder_path = 'D:/datasetproject/test2'

# 遍历文件夹并打印文件名
for filename in os.listdir(folder_path):
    # 构造完整的文件路径（可选）
    full_path = os.path.join(folder_path, filename)

    # 检查是否是文件（而不是文件夹）
    if os.path.isfile(full_path):
        # 图像存储时的名字
        new_file_name = filename[:-4] + '.png'
        # 目标图像
        target_image_path = "D:/datasetproject/test2/" + filename
        # 印章图像
        stamp_image_path = "D:/datasetproject/companyseal/5.png"
        # 存储路径
        output_path = "D:/datasetproject/result2/" + new_file_name
        stamp_image(target_image_path, stamp_image_path, output_path)