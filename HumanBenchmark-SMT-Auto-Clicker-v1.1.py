import os
import sys
import threading
from datetime import datetime
from PIL import ImageGrab
from pynput import mouse
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
from time import sleep

script_version = 1.1

# Global 'bool' vars
config_done = False
in_config_a = False
in_config_b = False
config_b_done = False
listening_in_pause = False
in_test_config = False
in_playing_seq = False
in_autoplay_mode = False
saving_seq = False

# Global 'list' var for the sequence
saved_seq = []

# Global 'tuple' var for the configuration
saved_config = ()

# Global 'tuple' vars for cases position
case_1_pos = ()
case_2_pos = ()
case_3_pos = ()
case_4_pos = ()
case_5_pos = ()
case_6_pos = ()
case_7_pos = ()
case_8_pos = ()
case_9_pos = ()

def reset_config():
    global config_done
    config_done = False
    global config_b_done
    config_b_done = False

def get_case_pos(n):
    match n:
        case 1:
            return case_1_pos
        case 2:
            return case_2_pos
        case 3:
            return case_3_pos
        case 4:
            return case_4_pos
        case 5:
            return case_5_pos
        case 6:
            return case_6_pos
        case 7:
            return case_7_pos
        case 8:
            return case_8_pos
        case 9:
            return case_9_pos
        case _:
            print("")
            print("Unknown case number! How is it even possible???")
            print("")
            os.system("pause")
            sys.exit(1)

def set_case_pos(x1, x2, x3, y1, y2, y3):
    global case_1_pos
    case_1_pos = (x1, y1)
    global case_2_pos
    case_2_pos = (x2, y1)
    global case_3_pos
    case_3_pos = (x3, y1)
    global case_4_pos
    case_4_pos = (x1, y2)
    global case_5_pos
    case_5_pos = (x2, y2)
    global case_6_pos
    case_6_pos = (x3, y2)
    global case_7_pos
    case_7_pos = (x1, y3)
    global case_8_pos
    case_8_pos = (x2, y3)
    global case_9_pos
    case_9_pos = (x3, y3)

def set_config(c, cx, cy):
    global saved_config
    if c == 1:
        x1 = cx
        x2 = x1 + 130
        x3 = x2 + 130
        y1 = cy
        y2 = y1 - 130
        y3 = y2 - 130
        saved_config = (x1, y1)
    else: # c == 2
        x3 = cx
        x1 = saved_config[0]
        x2 = (x1 + x3) / 2
        y3 = cy
        y1 = saved_config[1]
        y2 = (y1 + y3) / 2
        saved_config = (x1, y1, x3, y3)
    set_case_pos(x1, x2, x3, y1, y2, y3)
    if c == 2:
        global config_b_done
        config_b_done = True

def test_config():
    m = MouseController()
    global in_test_config
    while in_test_config:
        for case_num in range(1, 10):
            if not in_test_config: return
            m.position = get_case_pos(case_num)
            sleep(1)

def play_seq(autoplay_mode = False):
    m = MouseController()
    if autoplay_mode:
        global in_autoplay_mode
    else:
        global in_playing_seq
    global saved_seq
    for case_num in saved_seq:
        if autoplay_mode:
            if not in_autoplay_mode: return
        else:
            if not in_playing_seq: return
        m.position = get_case_pos(case_num)
        m.press(Button.left)
        m.release(Button.left)
        sleep(0.2)
    if not autoplay_mode:
        m.position = (0, 0)
        print("")
        print("== Sequence ended! ==")
        print("")
        print("Now add the last case of the new level before playing again")
        print("")
        print("==============================================")
        print("")
        print("Press 'A' Key to Automatically play the game!(*)")
        print("")
        print("(*) manually start the game then press 'A' immediatly")
        print("")
        print("Press 'E' Key to Export the configuration")
        print("")
        print("Press 'P' Key to Play the saved sequence")
        print("Press 'V' Key to View the saved sequence")
        print("Press 'U' Key to Undo the last case of the saved sequence")
        print("Press 'D' Key to Delete the saved sequence")
        print("")
        print("Press 'R' Key to Restart the configuration")
        print("")
        print("==============================================")
        in_playing_seq = False

def autoplay_seq(lvl):
    global in_autoplay_mode
    if not in_autoplay_mode: return
    print("")
    print(f"== Playing level: {lvl}")
    play_seq(True)
    if not in_autoplay_mode: return
    if lvl % 10 == 5 or lvl % 10 == 0:
        print("")
        print("Reminder: Press 'A' Key again to stop the auto-play")
    print("")
    print(f"== Reading level: {lvl + 1}")

def autoplay_mode():
    m = MouseController()
    print("")
    print("== Reading level: 1")
    m.position = (0, 0)
    rec_seq = []
    lvl = 1
    d = 0
    last_time = datetime.now()
    global in_autoplay_mode, saving_seq, saved_seq
    while in_autoplay_mode:
        for case_num in range(1, 10):
            if not in_autoplay_mode: return
            now = datetime.now()
            if (now - last_time).total_seconds() >= 3:
                if d > 1:
                    if d + 1 == lvl:
                        end_string = "]"
                    else:
                        end_string = ", ...]"
                    print(f", ?{end_string}")
                    print("")
                    print("== Incomplete sequence detected! Playing may fail... ==")
                    saving_seq = True
                    saved_seq.append(rec_seq[-1])
                    saving_seq = False
                    autoplay_seq(lvl)
                    m.position = (0, 0)
                    rec_seq.clear()
                    lvl += 1
                    d = 0
                    last_time = datetime.now()
                    break
                else:
                    if lvl == 1:
                        print("")
                        print("== No sequence detected! Misconfiguration? Game was not started? ==")
                    elif d == 1:
                        print("]")
                        print("")
                        print("== Incomplete sequence detected! Misconfiguration? Or maybe a bug? ==")
                    else:
                        print("")
                        print("== No sequence detected! Misconfiguration? Or maybe a bug? ==")
                    print("")
                    print("Press 'A' Key to continue...")
                    kb = KeyboardController()
                    kb.press("a")
                    kb.release("a")
                    return
            try:
                px_color = ImageGrab.grab().getpixel(get_case_pos(case_num))
            except:
                px_color = (0, 0, 0)
            if px_color == (255, 255, 255):
                # print(f"== Case {case_num} detected!")
                if d > 0:
                    if case_num == rec_seq[-1]: continue
                rec_seq.append(case_num)
                d += 1
                if d == 1:
                    print("")
                    print(f"Sequence: [{case_num}", end="", flush=True)
                elif d != lvl:
                    print(f", {case_num}", end="", flush=True)
                if d == lvl:
                    if lvl > 1:
                        print(f", {case_num}]")
                        if saved_seq != rec_seq[:-1]:
                            print("")
                            print("== Bad sequence detected! Can't play this level... ==")
                            print("")
                            print("Press 'A' Key to continue...")
                            kb = KeyboardController()
                            kb.press("a")
                            kb.release("a")
                            return
                        saving_seq = True
                        saved_seq.append(rec_seq[-1])
                    else: # lvl == 1
                        print("]")
                        saving_seq = True
                        saved_seq = rec_seq.copy()
                    saving_seq = False
                    sleep(0.8)
                    autoplay_seq(lvl)
                    m.position = (0, 0)
                    rec_seq.clear()
                    lvl += 1
                    d = 0
                last_time = datetime.now()

def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        # print(f"({x}, {y})")
        global in_config_b, config_done, in_config_a
        if (in_config_b or (not config_done and in_config_a)) and not pressed:
            if not in_config_b:
                set_config(1, x, y)
            else:
                set_config(2, x, y)
            print("")
            print("== End of configuration ==")
            print("")
            print("==============================================")
            print("Press 'T' Key to Test the configuration")
            print("==============================================")
            print("")
            print("IMPORTANT:")
            print("")
            print("== How to test the configuration ==")
            print("")
            print("1 - Launch the game to see the 9 cases")
            print("2 - Press 'T' Key")
            print("3 - Check if the cursor is switching on each case of the game")
            print("")
            if not in_config_b:
                print("If the test is failing for you:")
                print("")
                print("1 - Press 'Y' Key")
                print("2 - Click on the Middle of the UPPER-RIGHT case of the game")
            else:
                print("If the test is still failing for you, press 'R' Key to Restart the configuration")
            print("")
            print("==============================================")
            print("You can now use your Keyboard Numpad to save sequences")
            print("==============================================")
            print("")
            print("Press 'A' Key to Automatically play the game!(*)")
            print("")
            print("(*) manually start the game then press 'A' immediatly")
            print("")
            print("Press 'E' Key to Export the configuration")
            print("")
            print("Press 'P' Key to Play the saved sequence")
            print("Press 'V' Key to View the saved sequence")
            print("Press 'U' Key to Undo the last case of the saved sequence")
            print("Press 'D' Key to Delete the saved sequence")
            print("")
            print("Press 'R' Key to Restart the configuration")
            print("")
            print("==============================================")
            config_done = True
            in_config_a = False
            in_config_b = False
            return

def on_release(key):
    global config_done, in_config_a, in_config_b, listening_in_pause, in_test_config, in_playing_seq, in_autoplay_mode, saved_seq
    if listening_in_pause: return
    if hasattr(key, "vk"):
        # print(key.vk)
        if not in_config_b and not config_done:
            if key.vk == 67: # 'C' Key
                print("")
                if not in_config_a:
                    in_config_a = True
                    print("== Configuration ==")
                    print("")
                    print("Now click on the Middle of the BOTTOM-LEFT case")
                    print("")
                    print("Press 'C' Key again to abort configuration")
                    return
                print("== Configuration aborted! ==")
                in_config_a = False
                return
            if not in_config_a:
                if key.vk == 73: # 'I' Key
                    listening_in_pause = True
                    os.system("cls")
                    print("")
                    print("")
                    print(f"==== HumanBenchmark SMT Auto-Clicker v{script_version} ====")
                    print("")
                    print("== Import configuration ==")
                    print("")
                    input("Press 'Enter' Key to continue...\n\n")
                    os.system("cls")
                    print("")
                    print("")
                    print(f"==== HumanBenchmark SMT Auto-Clicker v{script_version} ====")
                    print("")
                    print("== Import configuration ==")
                    print("")
                    print("Type or paste the exportation code (spaces between numbers are important!)")
                    print("")
                    conf_line = input("Code: ")
                    print("")
                    if conf_line:
                        try:
                            pos_list = conf_line.strip().split(" ")
                            for i, pos in enumerate(pos_list):
                                if not pos: del pos_list[i]
                            has_two_pos = len(pos_list) == 2
                            has_four_pos = len(pos_list) == 4
                            if has_two_pos or has_four_pos:
                                set_config(1, int(pos_list[0]), int(pos_list[1]))
                                if has_four_pos:
                                    set_config(2, int(pos_list[2]), int(pos_list[3]))
                                print("== Configuration imported! ==")
                            else:
                                conf_line = ""
                                print("== Failed to import configuration! ==")
                        except:
                            reset_config()
                            conf_line = ""
                            print("== Failed to import configuration! ==")
                    else:
                        print("== No exportation code entered! ==")
                    print("")
                    print("==============================================")
                    if conf_line:
                        print("Press 'T' Key to Test the configuration")
                    else:
                        print("Press 'I' Key to Import the configuration")
                    print("==============================================")
                    print("")
                    if conf_line:
                        print("IMPORTANT:")
                        print("")
                        print("== How to test the configuration ==")
                        print("")
                        print("1 - Launch the game to see the 9 cases")
                        print("2 - Press 'T' Key")
                        print("3 - Check if the cursor is switching on each case of the game")
                        print("")
                        print("If the test is failing for you:")
                        print("")
                        print("Press 'R' Key to Restart the configuration")
                        print("")
                        print("==============================================")
                        print("You can now use your Keyboard Numpad to save sequences")
                        print("==============================================")
                        print("")
                        print("Press 'A' Key to Automatically play the game!(*)")
                        print("")
                        print("(*) manually start the game then press 'A' immediatly")
                        print("")
                        print("Press 'E' Key to Export the configuration")
                        print("")
                        print("Press 'P' Key to Play the saved sequence")
                        print("Press 'V' Key to View the saved sequence")
                        print("Press 'U' Key to Undo the last case of the saved sequence")
                        print("Press 'D' Key to Delete the saved sequence")
                        print("")
                        print("Press 'R' Key to Restart the configuration")
                        print("")
                        print("==============================================")
                        config_done = True
                    else:
                        print("== Configuration in 3 Steps ==")
                        print("")
                        print("1 - Launch the game to see the 9 cases")
                        print("2 - Press 'C' Key")
                        print("3 - Click on the Middle of the BOTTOM-LEFT case of the game")
                        print("")
                        print("==============================================")
                    listening_in_pause = False
                    return
        elif config_done:
            if not in_config_b and not in_test_config and not in_playing_seq and key.vk == 65: # 'A' Key
                print("")
                if not in_autoplay_mode:
                    in_autoplay_mode = True
                    print("== Auto-play started! ==")
                    print("")
                    print("Press 'A' Key again to stop the auto-play")
                    thread = threading.Thread(target=autoplay_mode)
                    thread.start()
                    return
                info_displayed = False
                global saving_seq
                while saving_seq:
                    if not info_displayed:
                        info_displayed = True
                        print("")
                        print("== Sequence is being saved! Please wait... ==")
                    sleep(0.2)
                else:
                    print("")
                    print("== Auto-play stopped! ==")
                    print("")
                    print("==============================================")
                    print("")
                    print("Press 'A' Key to Automatically play the game!(*)")
                    print("")
                    print("(*) manually start the game then press 'A' immediatly")
                    print("")
                    print("Press 'E' Key to Export the configuration")
                    print("")
                    print("Press 'P' Key to Play the saved sequence")
                    print("Press 'V' Key to View the saved sequence")
                    print("Press 'U' Key to Undo the last case of the saved sequence")
                    print("Press 'D' Key to Delete the saved sequence")
                    print("")
                    print("Press 'R' Key to Restart the configuration")
                    print("")
                    print("==============================================")
                    in_autoplay_mode = False
                    return
            if not in_config_b and not in_test_config and not in_autoplay_mode and key.vk == 80: # 'P' Key
                print("")
                if not in_playing_seq:
                    if len(saved_seq) == 0:
                        print("== No sequence saved! ==")
                        return
                    in_playing_seq = True
                    print("== Playing the saved sequence! ==")
                    print("")
                    print("Press 'P' Key again to stop playing")
                    thread = threading.Thread(target=play_seq)
                    thread.start()
                    return
                print("== Playing stopped! ==")
                print("")
                print("==============================================")
                print("")
                print("Press 'A' Key to Automatically play the game!(*)")
                print("")
                print("(*) manually start the game then press 'A' immediatly")
                print("")
                print("Press 'E' Key to Export the configuration")
                print("")
                print("Press 'P' Key to Play the saved sequence")
                print("Press 'V' Key to View the saved sequence")
                print("Press 'U' Key to Undo the last case of the saved sequence")
                print("Press 'D' Key to Delete the saved sequence")
                print("")
                print("Press 'R' Key to Restart the configuration")
                print("")
                print("==============================================")
                in_playing_seq = False
                return
            if not in_test_config and not in_playing_seq and not in_autoplay_mode and key.vk == 89: # 'Y' Key
                print("")
                if not in_config_b:
                    in_config_b = True
                    print("== Advanced configuration ==")
                    print("")
                    print("Now click on the Middle of the UPPER-RIGHT case")
                    print("")
                    print("Press 'Y' Key again to abort configuration")
                    return
                print("== Configuration aborted! ==")
                in_config_b = False
                return
            if not in_config_b and not in_playing_seq and not in_autoplay_mode:
                if key.vk == 84: # 'T' Key
                    print("")
                    if not in_test_config:
                        in_test_config = True
                        print("== Test configuration started! ==")
                        print("")
                        print("You should see the cursor switching on each case of the game")
                        print("")
                        print("Press 'T' Key again to stop the test")
                        thread = threading.Thread(target=test_config)
                        thread.start()
                        return
                    print("== Test configuration stopped! ==")
                    in_test_config = False
                    return
                if not in_test_config:
                    if key.vk == 69: # 'E' Key
                        print("")
                        print("== Export configuration ==")
                        print("")
                        print("Save this exportation code (spaces between numbers are important!):")
                        print("")
                        if not config_b_done:
                            print(f"{saved_config[0]} {saved_config[1]}")
                        else:
                            print(f"{saved_config[0]} {saved_config[1]} {saved_config[2]} {saved_config[3]}")
                        print("")
                        print("==============================================")
                        return
                    if key.vk == 97: # Numpad 1
                        saved_seq.append(1)
                        print("")
                        print("== BOTTOM-LEFT case added in the sequence! ==")
                        return
                    if key.vk == 98: # Numpad 2
                        saved_seq.append(2)
                        print("")
                        print("== BOTTOM-CENTER case added in the sequence! ==")
                        return
                    if key.vk == 99: # Numpad 3
                        saved_seq.append(3)
                        print("")
                        print("== BOTTOM-RIGHT case added in the sequence! ==")
                        return
                    if key.vk == 100: # Numpad 4
                        saved_seq.append(4)
                        print("")
                        print("== MIDDLE-LEFT case added in the sequence! ==")
                        return
                    if key.vk == 101: # Numpad 5
                        saved_seq.append(5)
                        print("")
                        print("== MIDDLE-CENTER case added in the sequence! ==")
                        return
                    if key.vk == 102: # Numpad 6
                        saved_seq.append(6)
                        print("")
                        print("== MIDDLE-RIGHT case added in the sequence! ==")
                        return
                    if key.vk == 103: # Numpad 7
                        saved_seq.append(7)
                        print("")
                        print("== UPPER-LEFT case added in the sequence! ==")
                        return
                    if key.vk == 104: # Numpad 8
                        saved_seq.append(8)
                        print("")
                        print("== UPPER-CENTER case added in the sequence! ==")
                        return
                    if key.vk == 105: # Numpad 9
                        saved_seq.append(9)
                        print("")
                        print("== UPPER-RIGHT case added in the sequence! ==")
                        return
                    if key.vk == 86: # 'V' Key
                        print("")
                        n = len(saved_seq)
                        if n == 0:
                            print("== No sequence saved! ==")
                            return
                        print("== View the sequence ==")
                        print("")
                        print(f"This following line is the saved sequence of {n} case(s):")
                        print("")
                        print(saved_seq)
                        print("")
                        print("==============================================")
                        return
                    if key.vk == 85: # 'U' Key
                        print("")
                        if len(saved_seq) == 0:
                            print("== No sequence saved! ==")
                            return
                        del saved_seq[-1]
                        print("== Last case of the sequence deleted! ==")
                        return
                    if key.vk == 68: # 'D' Key
                        saved_seq.clear()
                        print("")
                        print("=== Sequence reset! ===")
                        return
                    if key.vk == 82: # 'R' Key
                        reset_config()
                        print("")
                        print("=== Configuration reset! ===")
                        print("")
                        print("==============================================")
                        print("Press 'I' Key to Import the configuration")
                        print("==============================================")
                        print("")
                        print("== Configuration in 3 Steps ==")
                        print("")
                        print("1 - Launch the game to see the 9 cases")
                        print("2 - Press 'C' Key")
                        print("3 - Click on the Middle of the BOTTOM-LEFT case of the game")
                        print("")
                        print("==============================================")
                        return

def main():
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 10):
        print("")
        print("")
        print(f"==== HumanBenchmark SMT Auto-Clicker v{script_version} ====")
        print("")
        print("Please run this script using Python 3.10 or higher...")
        print("")
        os.system("pause")
        sys.exit(1)
    print("")
    print("")
    print(f"==== HumanBenchmark SMT Auto-Clicker v{script_version} ====")
    print("")
    print("==============================================")
    print("Press 'I' Key to Import the configuration")
    print("==============================================")
    print("")
    print("== Configuration in 3 Steps ==")
    print("")
    print("1 - Launch the game to see the 9 cases")
    print("2 - Press 'C' Key")
    print("3 - Click on the Middle of the BOTTOM-LEFT case of the game")
    print("")
    print("==============================================")
    mouse_listener = MouseListener(on_click=on_click)
    keyboard_listener = KeyboardListener(on_release=on_release)
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()

main()
