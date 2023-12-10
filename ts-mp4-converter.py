import subprocess
import glob
import os
from concurrent.futures import ThreadPoolExecutor

def convert_video(input_file):
    # 生成對應的輸出檔案名稱，例如，input.ts 將轉換為 input.mp4
    output_file = input_file.replace('.ts', '.mp4')

    # 指定 FFmpeg 的路徑
    ffmpeg_path = r'C:\Users\"USERNAME"\Desktop\ffmpeg\bin\ffmpeg.exe'

    try:
        # 執行ffmpeg命令轉換檔案
        subprocess.run([ffmpeg_path, '-i', input_file, output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 檢查是否成功轉換並存在 .mp4 檔案
        if os.path.exists(output_file):
            print(f"轉換成功：{input_file}")
            # 刪除原始 .ts 檔案
            os.remove(input_file)
        else:
            print(f"轉換失敗：{input_file}，無法找到對應的 .mp4 檔案")
    except Exception as e:
        print(f"轉換失敗：{input_file}，錯誤訊息：{str(e)}")

if __name__ == "__main__":
    # 使用通配符來獲取所有符合條件的.ts檔案
    input_files = glob.glob('*.ts')

    # 清點有多少.ts檔案
    num_files = len(input_files)
    print(f"總共有 {num_files} 個.ts檔案")

    # 使用ThreadPoolExecutor並行處理轉換任務
    with ThreadPoolExecutor(max_workers=4) as executor:
        for input_file in input_files:
            executor.submit(convert_video, input_file)
