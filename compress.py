from PIL import Image
import os
import sys
from io import BytesIO

def compress_image(input_path, output_path, max_size_kb=300, step=5, min_quality=10):
    max_size = max_size_kb * 1024
    img = Image.open(input_path)
    img_format = img.format

    # 只对JPEG压缩效果最佳，其他格式可先转为JPEG
    if img_format != 'JPEG':
        img = img.convert('RGB')

    quality = 95
    while quality >= min_quality:
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=quality)
        size = buffer.tell()
        if size <= max_size:
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())
            print(f"压缩成功，最终质量：{quality}，文件大小：{size // 1024}KB")
            return True
        quality -= step

    print("无法压缩到目标大小，请尝试缩小图片分辨率。")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python compress_image.py 输入图片路径 输出图片路径")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    compress_image(input_path, output_path)
