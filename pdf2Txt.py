import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import argparse
import os


def extract_text_with_pymupdf(pdf_path):
    """
    使用 PyMuPDF (fitz) 提取 PDF 文本。
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text.append(page.get_text("text"))  # "text" 参数确保只获取文本内容
        doc.close()
        return "\n".join(full_text)
    except Exception as e:
        print(f"使用 PyMuPDF 提取 '{pdf_path}' 时出错: {e}")
        return None


def extract_text_with_pdfminer(pdf_path):
    """
    使用 pdfminer.six 提取 PDF 文本。
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"使用 pdfminer.six 提取 '{pdf_path}' 时出错: {e}")
        return None


def save_text_to_file(text, output_txt_path):
    """
    将文本保存到文件。
    """
    try:
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"文本已成功提取并保存到: {output_txt_path}")
    except Exception as e:
        print(f"保存文本到 '{output_txt_path}' 时出错: {e}")


def main():
    parser = argparse.ArgumentParser(description="从 PDF 文件中提取文本并保存为 TXT 文件。")
    parser.add_argument("pdf_file", help="输入的 PDF 文件路径")
    parser.add_argument(
        "-o", "--output", help="输出的 TXT 文件路径 (可选, 默认为 PDF文件名.txt)")
    parser.add_argument(
        "--library",
        choices=["pymupdf", "pdfminer"],
        default="pymupdf",
        help="选择用于提取文本的库 (pymupdf 或 pdfminer, 默认为 pymupdf)"
    )

    args = parser.parse_args()

    pdf_path = args.pdf_file
    if not os.path.exists(pdf_path):
        print(f"错误: PDF 文件 '{pdf_path}' 不存在。")
        return

    if args.output:
        output_txt_path = args.output
    else:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_txt_path = f"{base_name}.txt"

    print(f"正在处理: {pdf_path}")
    print(f"将使用库: {args.library}")

    extracted_text = None
    if args.library == "pymupdf":
        extracted_text = extract_text_with_pymupdf(pdf_path)
        if extracted_text is None or not extracted_text.strip():  # 如果pymupdf失败或没提取到内容
            print("PyMuPDF 未能提取文本或文本为空，尝试使用 pdfminer.six (如果已安装)...")
            extracted_text = extract_text_with_pdfminer(pdf_path)
    elif args.library == "pdfminer":
        extracted_text = extract_text_with_pdfminer(pdf_path)
        if extracted_text is None or not extracted_text.strip():
            print("pdfminer.six 未能提取文本或文本为空，尝试使用 PyMuPDF (如果已安装)...")
            extracted_text = extract_text_with_pymupdf(pdf_path)

    # 如果两种方法都尝试了，但还是没有文本
    if extracted_text is None or not extracted_text.strip():
        print(f"未能从 '{pdf_path}' 中提取任何文本。")
        print("可能原因：")
        print("1. PDF 是扫描件（图片），需要 OCR 工具。")
        print("2. PDF 内容为空或格式特殊。")
        print("3. PDF 已加密且未提供密码。")
        return

    save_text_to_file(extracted_text, output_txt_path)


if __name__ == "__main__":
    main()
