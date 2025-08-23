from pyboy import PyBoy
import os
from PIL import Image
import time

from config import ROM_PATH, SAVESTATE_PATH, COUNTER_PATH, FRAME_RESOLUTION

def countfile(path:str):
    val = -1
    if os.path.exists(path) and os.path.isfile(path):
        with open(path, "r") as count:
            val = int(count.read())
        with open(path, "w") as count:
            count.write(str(val+1))
    else:
        with open(path, "w") as count:
            count.write(str(1))
            val = 0
    return val

def gen_video(pyboy:PyBoy, duration:int, output:os.PathLike|str, fps:int=60):   
    frames:list[Image.Image] = []
    emulationTime = 0
    resizeTime = 0
    for _ in range(duration*fps):
        t1 = time.time()
        frames.append(pyboy.screen.image.copy().resize(FRAME_RESOLUTION, resample=Image.Resampling.BOX)) # pyright: ignore[reportOptionalMemberAccess]
        t2 = time.time()
        pyboy.tick()
        t3 = time.time()
        resizeTime += t2-t1
        emulationTime += t3-t2
    startSave = time.time()
    id = countfile(COUNTER_PATH)
    frames[0].save(f"{output}/out_{id:06d}.webp", 
                    save_all=True,
                    interlace=False,
                    optimize=True,
                    append_images=frames[1:],
                    duration=1000 // fps,
                    loop=1,
                    quality=80)
    endSave = time.time()

    print(f"Stats: Emulation time:{emulationTime:.2f}, ResizeTime:{resizeTime:.2f}, saveTime: {endSave-startSave:.2f} ")
    return id


def input_manager(pyboy:PyBoy, pressDuration:int=5):
    actionDone = False
    while not actionDone:
        action = input("Action: ")
        match action:
            case "up":
                pyboy.button("up", pressDuration)
                actionDone = True
            case "down":
                pyboy.button("down", pressDuration)
                actionDone = True
            case "left":
                pyboy.button("left", pressDuration)
                actionDone = True
            case "right":
                pyboy.button("right",pressDuration)
                actionDone = True
            case "a":
                pyboy.button("a", pressDuration)
                actionDone = True
            case "b":
                pyboy.button("b", pressDuration)
                actionDone = True
            case "st":
                pyboy.button("start", pressDuration)
                actionDone = True
            case "sl":
                pyboy.button("select", pressDuration)
                actionDone = True
            case "p":
                print("Pass")
                actionDone = True
            case "q":
                return False
    return True

def savestate(pyboy:PyBoy, savestatePath:str = SAVESTATE_PATH):
    with open(savestatePath, "wb") as stateFile:
        pyboy.save_state(stateFile)

def startEmulator(rom_path: str, state_path: str | None = None) -> PyBoy:
    pyboy = PyBoy(ROM_PATH, sound_emulated=False, window="null")

    if state_path is not None:
        with open(SAVESTATE_PATH, "rb") as state:
            pyboy.load_state(state)

    pyboy.set_emulation_speed(0)

    return pyboy

def EmuMain():
    pyboy = startEmulator(ROM_PATH, SAVESTATE_PATH)
    videoDuration = 2

    while True:
        gen_video(pyboy, videoDuration, "out.webp")
        if not input_manager(pyboy):
            break
        savestate(pyboy)

    savestate(pyboy)
    pyboy.stop()