import argparse
import subprocess
import threading

# Hàm để phân tích cú pháp các đối số dòng lệnh
def parse_args():
    """
    Parse command line arguments.
    """
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

# Đọc usernames từ file TXT
def load_usernames(file_path):
    with open(file_path, 'r') as file:
        usernames = [line.strip() for line in file if line.strip()]
    return usernames

# Chia usernames thành 10 danh sách
def split_usernames(usernames, num_lists=10):
    # Chia đều usernames thành num_lists danh sách
    return [usernames[i::num_lists] for i in range(num_lists)]

def main():
    args = parse_args()
    output = args.username
    
    # Đọc usernames từ file TXT
    usernames = load_usernames('usernames.txt')
    
    # Chia usernames thành 10 danh sách
    username_lists = split_usernames(usernames)
    
    # Lấy danh sách các username từ đối số dòng lệnh
    index = int(args.username) - 1  # Giả sử đối số là số từ 1 đến 10
    if 0 <= index < len(username_lists):
        usernames_to_process = username_lists[index]
    else:
        print("Invalid username list index.")
        return
    
    # Tạo luồng cho mỗi username trong danh sách
    threads = []
    for username in usernames_to_process:
        thread = threading.Thread(target=run_command, args=(username, output))
        threads.append(thread)

    # Bắt đầu chạy các luồng
    for thread in threads:
        thread.start()

    # Đợi tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()

    print("Tất cả luồng đã hoàn thành.")

if __name__ == "__main__":
    main()
