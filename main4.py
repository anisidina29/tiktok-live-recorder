import argparse
import subprocess
import threading
import multiprocessing
import os
import time

# Hàm để phân tích cú pháp các đối số dòng lệnh
def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-username",
                        dest="username",
                        help="List username.",
                        required=True,
                        action='store')
    args = parser.parse_args()
    return args

# Hàm để chạy lệnh bên ngoài
def run_command(username, output):
    command = f"python3 main.py -user {username} -mode automatic -output {output} -ffmpeg"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}.")
        print(f"Error output: {e.stderr}")

# Hàm để xử lý video bằng demucs và ffmpeg
def process_single_video(video_path, output_dir):
    # Tách âm thanh bằng demucs
    command = f"python -m demucs.separate -d cuda --out {output_dir} {video_path}"
    subprocess.run(command, shell=True)
    
    # Đường dẫn tới tệp âm thanh giọng hát đã tách
    vocals_path = os.path.join(output_dir, "htdemucs", os.path.basename(video_path).replace(".mp4", ""), "vocals.wav")

    # Đường dẫn tới video tạm thời không có âm thanh
    temp_video_path = f"{video_path[0:-4]}_temp.mp4"

    # Tách âm thanh khỏi video và lưu lại video không có âm thanh
    subprocess.run(f"ffmpeg -i {video_path} -c copy -an {temp_video_path}", shell=True)

    # Thay âm thanh của video bằng âm thanh giọng hát đã tách và lưu video mới
    without_music_dir = os.path.join(output_dir, "without_music")
    if not os.path.exists(without_music_dir):
        os.makedirs(without_music_dir)
    output_video_path = os.path.join(without_music_dir, f"{os.path.basename(video_path[0:-4])}_without_music.mp4")
    subprocess.run(f"ffmpeg -i {temp_video_path} -i {vocals_path} -c:v copy -c:a aac -strict experimental {output_video_path}", shell=True)

    # Xóa video tạm thời và video gốc
    os.remove(temp_video_path)
    os.remove(video_path)

# Hàm để xử lý video bằng demucs và ffmpeg
def process_video(output_dir, interval=300):
    processed_files = set()
    while True:
        # Lấy danh sách các tệp video mới trong thư mục output
        for file_name in os.listdir(output_dir):
            if file_name.endswith(".mp4") and file_name not in processed_files:
                video_path = os.path.join(output_dir, file_name)
                processed_files.add(file_name)

                # Tạo luồng để xử lý video
                thread = threading.Thread(target=process_single_video, args=(video_path, output_dir))
                thread.start()
                thread.join()
        
        # Đợi một khoảng thời gian trước khi kiểm tra lại
        time.sleep(interval)

# Danh sách các username
usernames1 = ["park.77m1","bonbarber2210","minhly06_01", "hunggymcalis", "quocvu93","nienty28", "buiquoc_sw","truongminhdung1904","anhhhh_tu","hongduong.1199"]
usernames2 = ["honguynvn04","365.ngy.nh.em","herst277","trinhatquankhu1","thang_masic","gymerteamhonda"]
usernames3 = ["duongkimochii","duongtapxo","congmanhfitness","_nmd04","hieuluoitap","fu_nguyen68"]
usernames4 = ["hmatuan9","huutinh103","anhbodoi6mui","ikram_rmdn","kieubanana","cokhiminhtrung","hungrambo1_"]
usernames5 = ["hpp358965","rforrachman","ntf_205","rhenz_win","ashuracalisthenicsteam","nihao22012003"]
usernames6 = ["tvc.gym","ngthanhlong021006","kenvo12022001","minhnam2004","minh.ha0102","tienfit"]
usernames7 = ["hy.calis","bimostreetworkout.id","kenvo12022001","vanbinh0906","duc_trong9x","huyvo.1510"]
usernames8 = ["hoanganh1112022","tuntl675", "yeuem2003n","thanabodxx","minh.ha0102","quang_fitness","huuhieulam","nxp.fitness","thanhthong2608"]
usernames9 = ["chulongcuaemm","141201nth", "voquyhuyyy24102001","manhhiucute","hieuvilai2007","trun_trun.32"]
usernames10 = ["anhhhh_tu","tuanhamez","sinhan68","jdnummer1","minhnguyen_ifbb","duyanh_15112003","nxp.fitness","thanhthong2608","bee.calisthenics"]
# Mapping choices to actual lists
username_lists = {
    'usernames1': usernames1,
    'usernames2': usernames2,
    'usernames3': usernames3,
    'usernames4': usernames4,
    'usernames5': usernames5,
    'usernames6': usernames6,
    'usernames7': usernames7,
    'usernames8': usernames8,
    'usernames9': usernames9,
    'usernames10': usernames10
}

def main():
    args = parse_args()
    output = args.username
    # Lấy danh sách các username từ đối số dòng lệnh
    usernames = username_lists[args.username]

    # Tạo tiến trình cho mỗi username trong danh sách
    processes = []
    for username in usernames:
        process = multiprocessing.Process(target=run_command, args=(username, output))
        processes.append(process)

    # Tạo tiến trình để xử lý video
    video_process = multiprocessing.Process(target=process_video, args=(output,))

    # Bắt đầu chạy các tiến trình
    for process in processes:
        process.start()
    video_process.start()

    # Đợi tất cả các tiến trình hoàn thành
    for process in processes:
        process.join()
    video_process.join()

    print("Tất cả tiến trình đã hoàn thành.")

if __name__ == "__main__":
    main()
