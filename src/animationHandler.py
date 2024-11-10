from tkinter import *
from animationObject import *

def test():
    playAnimation()

frame = 0
def playAnimation ():
    global frame
    if frame > 40:
        return
    else:
        frame += 1
        window.after(100, playAnimation)

# set up our window
window = Tk()
window.title("Potion Game")
window.configure(background="gray")
wsize = {"x": int(window.winfo_screenwidth()*.75), "y": int(window.winfo_screenheight()*.75) }
wpos = {"x": window.winfo_screenwidth()/2 - wsize["x"]/2, "y": window.winfo_screenheight()/2 -wsize["y"]/2}
window.minsize( wsize["x"], wsize["y"] )
window.geometry("%dx%d+%d+%d" % (wsize["x"], wsize["y"], wpos["x"], wpos["y"]) )

print(wsize)
print(wpos)

a = animationObject("potion_game//mix", window)
test = Button(window, text="drink", command=test)
test.place(x=0, y=0)

# start the loop
window.mainloop()