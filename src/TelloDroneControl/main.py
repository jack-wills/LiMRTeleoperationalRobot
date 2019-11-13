import tello as tello
import tkinter

def takeSnapshot(drone, outputPath):
    """
    save the current frame of the video as a jpg file and put it into outputpath
    """
    frame = drone.read()

    # grab the current timestamp and use it to construct the filename
    ts = datetime.datetime.now()
    filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))

    p = os.path.sep.join((outputPath, filename))

    # save the file
    cv2.imwrite(p, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    print("[INFO] saved {}".format(filename))

def main():

    drone = tello.Tello('', 8889)  
    drone.enable_mp()
    window = tkinter.Tk()
    # to rename the title of the window
    window.title("GUI")
    # pack is used to show the object in the window
    label = tkinter.Label(window, text = "Hello World!").pack()
    btn1 = tkinter.Button(window, text = "Take Off", fg = "red", command=drone.takeoff).pack()
    btn2 = tkinter.Button(window, text = "Land", fg = "red", command=drone.land).pack()
    btn3 = tkinter.Button(window, text = "Move up", fg = "red", command=lambda:drone.move_up(1)).pack()
    btn4 = tkinter.Button(window, text = "Move down", fg = "red", command=lambda:drone.move_down(1)).pack()
    btn6 = tkinter.Button(window, text = "MP Land 1", fg = "red", command=lambda:drone.move_to_mp(0,0,10,10,'m1')).pack()
    btn7 = tkinter.Button(window, text = "MP Land 2", fg = "red", command=lambda:drone.move_to_mp(0,0,10,10,'m2')).pack()
    btn8 = tkinter.Button(window, text = "MP Land nearest", fg = "red", command=lambda:drone.move_to_mp(0,0,10,10,'m-2')).pack()
    window.update()
    window.mainloop()

if __name__ == "__main__":
    main()
