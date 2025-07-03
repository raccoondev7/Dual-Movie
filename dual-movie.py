import vlc
import time
import sys
import os
import keyboard 

# Get video files in current directory
VIDEO_EXTS = (
    '.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm', '.wmv', '.mpeg', '.mpg', '.m4v', '.3gp'
)
AUDIO_EXTS = (
    '.mp3', '.wav', '.ogg', '.opus', '.aac', '.flac', '.m4a', '.wma'
)

ALL_EXTS = VIDEO_EXTS + AUDIO_EXTS
all_files = [f for f in os.listdir('.') if f.lower().endswith(ALL_EXTS)]

# if len(all_files) < 2:
#     print("Need at least two video files in the current directory.")
#     sys.exit(1)

# Show files to user
print("\nFound video files:")
for i, f in enumerate(all_files):
    print(f"{i + 1}: {f}")

# Ask for choices
def ask_choice(prompt, exclude=None):
    while True:
        try:
            choice = int(input(prompt)) - 1
            if 0 <= choice < len(all_files) and choice != exclude:
                return choice
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

i1 = ask_choice("\nSelect video 1 (enter number): ")
i2 = ask_choice("Select video 2 (enter number): ", exclude=i1)

video_paths = [all_files[i1], all_files[i2]]
positions = [0.0, 0.0]

# VLC setup
instance = vlc.Instance("--no-video-title-show", "--quiet")
players = [instance.media_player_new(), instance.media_player_new()]
media_objects = [instance.media_new(path) for path in video_paths]

for i in range(2):
    players[i].set_media(media_objects[i])
    players[i].play()
    time.sleep(0.3)
    players[i].pause()
    players[i].set_position(0.0)

current_video = 0
players[current_video].play()
is_paused = False

def skip_time(player, seconds):
    length = player.get_length() / 1000
    if length <= 0:
        return
    current_time = player.get_time() / 1000
    new_time = max(0, min(current_time + seconds, length))
    player.set_time(int(new_time * 1000))

try:
    step = 0.05       # 5% speed step
    min_rate = 0.25   # Minimum allowed speed
    max_rate = 4.0    # Maximum allowed speed
    
    print("Controls:")
    print("[Tab]    - Switch video")
    print("[Space]  - Pause/Play")
    print("[W]/[E]  - Rewind/Forward 5 sec")
    print("[[ ]]]   - Decrease/Increase speed by 5%")
    print("[\\]      - Reset speed to 1.0x")

    while True:
        if keyboard.is_pressed("tab"):
            positions[current_video] = players[current_video].get_position()
            players[current_video].pause()

            current_video = 1 - current_video
            players[current_video].set_position(positions[current_video])
            players[current_video].play()
            is_paused = False

            while keyboard.is_pressed("tab"):
                time.sleep(0.1)

        if keyboard.is_pressed("space"):
            if is_paused:
                players[current_video].play()
                is_paused = False
            else:
                players[current_video].pause()
                is_paused = True

            while keyboard.is_pressed("space"):
                time.sleep(0.1)

        if keyboard.is_pressed("w"):
            skip_time(players[current_video], -5)
            while keyboard.is_pressed("w"):
                time.sleep(0.1)

        if keyboard.is_pressed("e"):
            skip_time(players[current_video], 5)
            while keyboard.is_pressed("e"):
                time.sleep(0.1)
                
        if keyboard.is_pressed("["):
            current_rate = players[current_video].get_rate()
            new_rate = max(min_rate, round(current_rate - step, 2))
            players[0].set_rate(new_rate)
            players[1].set_rate(new_rate)
            print(f"Speed: {new_rate:.2f}x")
            while keyboard.is_pressed("["):
                time.sleep(0.1)

        if keyboard.is_pressed("]"):
            current_rate = players[current_video].get_rate()
            new_rate = min(max_rate, round(current_rate + step, 2))
            players[0].set_rate(new_rate)
            players[1].set_rate(new_rate)
            print(f"Speed: {new_rate:.2f}x")
            while keyboard.is_pressed("]"):
                time.sleep(0.1)

        if keyboard.is_pressed("\\"):
            players[0].set_rate(1.0)
            players[1].set_rate(1.0)
            print("Speed: 1.00x")
            while keyboard.is_pressed("\\"):
                time.sleep(0.1)
  

        time.sleep(0.05)

except KeyboardInterrupt:
    for p in players:
        p.stop()
    sys.exit()
