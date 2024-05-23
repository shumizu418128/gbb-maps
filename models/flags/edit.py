import os
import subprocess
from tqdm import tqdm

# 現在のディレクトリを取得
current_directory = os.getcwd()

# 現在のディレクトリ内のすべてのファイルを取得
for filename in tqdm(os.listdir(current_directory)):

    # ファイルがPNG形式の場合
    if filename.endswith(".png"):

        # ファイル名から拡張子を除いた部分を取得
        name_without_extension = os.path.splitext(filename)[0]

        # 名前から _flag と - を削除
        name_without_extension = name_without_extension.replace("_flag", "")

        # 名前のすべての - をスペースに置き換え
        name_without_extension = name_without_extension.replace("-", " ")

        # WebP形式の新しいファイル名を作成
        new_filename = name_without_extension + ".webp"

        # cwebpツールを使用してPNGをWebPに変換
        subprocess.run(["cwebp", filename, "-o", new_filename])

        # 変換前のPNGファイルを削除
        os.remove(filename)
