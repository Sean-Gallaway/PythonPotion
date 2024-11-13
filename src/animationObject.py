# import os
# from os import walk
# import tkinter
# import gobject

# class animationObject ():
#     currentImage = None
#     directory = None
#     label = None
#     loop = False
#     currentIndex = 0
#     frames = {}
#     window = None


#     def __init__ (self, path: str, w, loopAnim = False):

#         self.loop = loopAnim
#         self.directory = path
#         self.window = w
        
#         index = 0
#         for (dirpath, dirnames, files) in walk(path):
#             for item in files:
#                 # exclude this file, if this file is in the base folder. exclude all non py files
#                 if ".png" in item:
#                     print(item)
#                     self.frames[index] = tkinter.PhotoImage(file = path+"//"+item)
#                     # self.frames[index].resize((1920, 1080))
#                 break
#             break

#         self.currentImage = self.frames[0]
#         self.render()
        

#     def render (self):
#         global window
#         self.label = tkinter.Label(self.window, image = self.frames[0], borderwidth = -1, highlightthickness = -1)
#         self.label.place(x = 0, y = 0)
