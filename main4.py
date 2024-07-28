import os
import subprocess
import threading
import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-username", dest="username", help="List username.", required=True, action='store')
    args = parser.parse_args()
    return args

# Function to run external command
def run_command(username, output):
    command = f"python3 main.py -user {username} -mode automatic -output {output} -ffmpeg"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}.")
        print(f"Error output: {e.stderr}")

# Function to run YouTube automation in a separate thread
def run_thread(keyword):
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.youtube.com/")
        search_box = driver.find_element(By.XPATH, '//input[@id="search"]')
        search_box.send_keys("@Boymuscleworkout")
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        video_link = driver.find_element(By.XPATH, '//*[@id="subscribers" and contains(text(), "@Boymuscleworkout")]')
        video_link.click()
        time.sleep(5)

        playlists = driver.find_element(By.XPATH, '//yt-tab-shape[@tab-title="Playlists"]')
        playlists.click()
        time.sleep(5)
        
        watch_video = driver.find_element(By.XPATH, f'//a[@id="video-title" and contains(text(), "{keyword}")]')
        watch_video.click()
        time.sleep(10)

        while True:
            driver.save_screenshot(f"screenshot_{keyword}_{time.time()}.png")
            print(f"Screenshot taken for keyword: {keyword}")
            time.sleep(300)  # Wait for 10 minutes before taking the next screenshot

    except Exception as e:
        print(f"Exception occurred: {e}")
        driver.get("https://www.youtube.com/@Boymuscleworkout/playlists")
        time.sleep(10)
        
        watch_video = driver.find_element(By.XPATH, f'//a[@id="video-title" and contains(text(), "{keyword}")]')
        watch_video.click()
        time.sleep(10)

        while True:
            driver.save_screenshot(f"screenshot_{keyword}_{time.time()}.png")
            print(f"Screenshot taken for keyword: {keyword}")
            time.sleep(300)  # Wait for 10 minutes before taking the next screenshot

    finally:
        driver.quit()

# List of usernames for different categories
usernames1 = ["park.77m1","bonbarber2210","minhly06_01", "hunggymcalis", "quocvu93","nienty28", "buiquoc_sw","truongminhdung1904","hongduong.1199","k6will"]
usernames2 = ["honguynvn04","365.ngy.nh.em","herst277","trinhatquankhu1","thang_masic","gymerteamhonda","kimnguyennanh","namomothichbenchpress","duongbeobuong","tinthichnhay2000"]
usernames3 = ["duongkimochi","duongtapxo","congmanhfitness","_nmd04","hieuluoitap","fu_nguyen68","phongbum2002","vonhut.201","rin.fitness6","cuong_02032006","dksjsjn"]
usernames4 = ["hmatuan9","huutinh103","anhbodoi6mui","ikram_rmdn","kieubanana","cokhiminhtrung","hungrambo1_","bachmahoangtu2k","frog2lee2_","duc_trong11","t_fitness3993"]
usernames5 = ["hpp358965","rforrachman","ntf_205","rhenz_win","ashuracalisthenicsteam","nihao22012003","dp_120796","chuyn1999","noluckyluat2","phuongquan778899","truong66789"]
usernames6 = ["tvc.gym","ngthanhlong021006","minhnam2004","tienfit","anhtung_0510","vanhcalis2007","hoangchuii","pt.lehoan","duongerik99k","letruong0362"]
usernames7 = ["hy.calis","bimostreetworkout.id","kenvo12022001","vanbinh0906","duc_trong9x","huyvo.1510","hung01082004","khacllong","thanhhau6.3","vantugdji"]
usernames8 = ["hoanganh1112022","tuntl675", "yeuem2003n","thanabodxx","minh.ha0102","quang_fitness","huuhieulam","trunghuynh1105","thanhthong2608","sadboiz26032004_"]
usernames9 = ["pvmminh","141201nth", "voquyhuyyy24102001","manhhiucute","hieuvilai2007","trun_trun.32","congsothichtapgym","nien_2006","kiennguyenvan0302","louischien7","_vcuongg15_"]
usernames10 = ["anhhhh_tu","tuanhamez","sinhan68","jdnummer1","minhnguyen_ifbb","duyanh_15112003","nxp.fitness","thanhthong2608","bee.calisthenics","trungduong.97","nguyendatfitness"]

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
    usernames = username_lists[args.username]

    # Create threads for each username
    threads = []
    for username in usernames:
        thread = threading.Thread(target=run_command, args=(username, output))
        threads.append(thread)
    
    keywords = ["hieuvilai2007", "honguynvn04"]  # Replace with actual keywords
    for keyword in keywords:
        yt_thread = threading.Thread(target=run_thread, args=(keyword,))
        yt_thread.start()
        threads.append(yt_thread)

    # Start all threads for run_command
    for thread in threads:
        thread.start()



    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All threads have completed.")

if __name__ == "__main__":
    main()
