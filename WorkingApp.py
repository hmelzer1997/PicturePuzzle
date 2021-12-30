from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFile
import random, os, sys


ImageFile.LOAD_TRUNCATED_IMAGES = True
Alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l",
            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
#frames
root = Tk()
#root.title("Coordly")
root.title("Henry's Picture Puzzle")
root.geometry('2000x1000')
#root.iconbitmap('Icon.ico')

save_window = Frame(root, width=300, bd=3, bg="#F0F0F0", height=1000,
                    highlightbackground="black", highlightthickness=2)
save_window.pack(side=LEFT, expand=False, fill=BOTH)

input_window = Frame(root, width=1700, height=50, bg="#F0F0F0",
                     highlightbackground="black", highlightthickness=2)
input_window.pack(side=BOTTOM, expand=False, fill=BOTH)

action_window = Frame(root, height=950, width=1700, bg="#BAECE9",
                      highlightbackground="black", highlightthickness=2)
action_window.pack(side=TOP, expand=False, fill=BOTH)
button_space = Frame(action_window)
button_space.place(relx=0.5, rely=0.5, anchor=CENTER)

#Get relative file
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#Input Window Widget Actions
input_pic = Image.open('/Users/henrymelzer/PycharmProjects/CoordinateMath/sample.jpg')

def uploadImage():
    global input_pic
    filetypes = (
        ('Pictures','*.png'),
        ('Pictures','*.jpg')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    if filename:
        showinfo(title="Upload Completed!", message="Your picture will be divided after you submit.")
        input_pic = Image.open(filename)
        input_pic = input_pic.convert('RGB')
        InputSubmitButt.config(state=NORMAL)
    else:
        showinfo(title="No File Included", message="Please reclick button and try again.")



Ordered_xCoord = []
Ordered_yCoord = []
F_Crop = []
BackList = []
F_Button = []
ImageButtonList = []
DefaultCoordinates = 0
PaperOrientation = -1
def Submit():
    global Ordered_xCoord, Ordered_yCoord, F_Crop, ImageButtonList, F_Button, DefaultCoordinates, PaperOrientation
    root.update()
    DefaultCoordinates = Coord_Number.get()
    Paper_Count = Section_Number.get()
    if isinstance(int(DefaultCoordinates), int) and isinstance(int(Paper_Count), int):
        DefaultCoordinates = abs(int(Coord_Number.get()))
        Paper_Count = abs(int(Section_Number.get()))
        w = input_pic.width
        h = input_pic.height
        ## +1 (landscape) and -1 (portrait) will designate orientation
        if w > h:
            PhotoOrientation = 1
        elif w == h:
            PhotoOrientation = 1
        else:
            PhotoOrientation = -1
        PapPort_w = w % 85
        PapPort_h = h % 110
        PaperLandscape_w = w % 110
        PaperLandscape_h = h % 85
        ## +1 (landscape) and -1 (portrait) will designate orientation
        if PaperLandscape_w + PaperLandscape_h < PapPort_w + PapPort_h:
            PaperOrientation = 1
            add_topbot = int((85 - PaperLandscape_h) / 2)
            add_lefrig = int((110 - PaperLandscape_w) / 2)
            PaddedWidth = w + (2 * add_lefrig)
            PaddedHeight = h + (2 * add_topbot)
            PaddedImage = Image.new(input_pic.mode, (PaddedWidth, PaddedHeight), (0, 0, 0))
            PaddedImage.paste(input_pic, (add_lefrig, add_topbot))
            PaddedImage.save('Padded.png')
        elif PaperLandscape_w + PaperLandscape_h == PapPort_w + PapPort_h:
            PaperOrientation = -1
            add_topbot = int((110 - PapPort_h) / 2)
            add_lefrig = int((85 - PapPort_w) / 2)
            PaddedWidth = w + (2 * add_lefrig)
            PaddedHeight = h + (2 * add_topbot)
            PaddedImage = Image.new(input_pic.mode, (PaddedWidth, PaddedHeight), (0, 0, 0))
            PaddedImage.paste(input_pic, (add_lefrig, add_topbot))
            PaddedImage.save('Padded.png')
        else:
            PaperOrientation = -1
            add_topbot = int((110 - PapPort_h) / 2)
            add_lefrig = int((85 - PapPort_w) / 2)
            PaddedWidth = w + (2 * add_lefrig)
            PaddedHeight = h + (2 * add_topbot)
            PaddedImage = Image.new(input_pic.mode, (PaddedWidth, PaddedHeight), (0, 0, 0))
            PaddedImage.paste(input_pic, (add_lefrig, add_topbot))
            PaddedImage.save('Padded.png')

        # Pixels in 8.5 x 11' Paper
        # 1063 x 1375 for 125 pixels per inch
        # 2550 x 3300 for 300 Pixels per Inch

        k = ((PaddedHeight * PaddedWidth) / (85 * 110 * Paper_Count)) ** (1 / 2)
        if PaperOrientation == +1:
            PaperWidth = 110 * k
            PaperHeight = 85 * k
        elif PaperOrientation == -1:
            PaperWidth = 85 * k
            PaperHeight = 110 * k
        else:
            showinfo("Error: No Paper Orientation Found")

        x_PaperCount = round(PaddedWidth / PaperWidth)
        y_PaperCount = round(PaddedHeight / PaperHeight)

        # Number of sections to make variable matrix
        SectionCount = []
        for i in range(1, (x_PaperCount * y_PaperCount) + 1):
            SectionCount.append(i)

        Ordered_xCoord = []
        Ordered_yCoord = []

        # Order x-Coords for sections
        for i in range(x_PaperCount * y_PaperCount):
            if SectionCount[i] % x_PaperCount == 0:
                Ordered_xCoord.append(x_PaperCount)
            else:
                Ordered_xCoord.append(SectionCount[i] % x_PaperCount)

        # Order y-Coords for sections
        for i in range(x_PaperCount * y_PaperCount):
            if SectionCount[i] % x_PaperCount != 0:
                Ordered_yCoord.append(int(SectionCount[i] / x_PaperCount) + 1)
            else:
                Ordered_yCoord.append(int(SectionCount[i] / x_PaperCount))

        F_Button = []
        F_Crop = []

        for i in range((x_PaperCount * y_PaperCount)):
            BackList.append(i)
            cropped = PaddedImage.crop(((i % (x_PaperCount)) * PaperWidth, int(i / (x_PaperCount)) * PaperHeight,
                                        (i % (x_PaperCount)) * PaperWidth + PaperWidth,
                                        int(i / (x_PaperCount)) * PaperHeight + PaperHeight))
            if PaperOrientation == 1:
                largesave = cropped.save('{}.png'.format(i))
                F_Crop.append(largesave)
                x = cropped.resize((110, 85))
                y = x.save('Button{}.png'.format(i))
                z = ImageTk.PhotoImage(Image.open('Button{}.png'.format(i)))
                F_Button.append(z)
            elif PaperOrientation == -1:
                largesave = cropped.save('{}.png'.format(i))
                F_Crop.append(largesave)
                x = cropped.resize((85, 110))
                y = x.save('Button{}.png'.format(i))
                z = ImageTk.PhotoImage(Image.open('Button{}.png'.format(i)))
                F_Button.append(z)
            else:
                showinfo("Error on Resize")

        if (x_PaperCount * y_PaperCount) != Paper_Count:
            Error_Message = "The closest we could get to your requested section number was " + \
                            str(x_PaperCount*y_PaperCount) + "."
            showinfo(title="We tried our best!",
                     message=Error_Message)
        DimensionMessage = "Your picture is " + str(x_PaperCount) + " (across) by " + str(y_PaperCount) + " (down)."
        showinfo(title="Dimensions", message=DimensionMessage)
        showinfo(title="Finished!", message="Click on a section to edit its back.")
        ImageButtonList = []
        #Button Orientation (1: Landscape)
        if PaperOrientation == 1:
            for i in range(len(Ordered_xCoord)):
                InitButtonPhoto = F_Button[i]
                ButtonPhoto = InitButtonPhoto
                ImageButtonList.append(Button(button_space, command= lambda i=i: EditBack(i), bd=3, width=110,
                                  height=85, image=ButtonPhoto))
                ImageButtonList[i].grid(row=Ordered_yCoord[i], column=Ordered_xCoord[i])
        else:
            for i in range(len(Ordered_xCoord)):
                InitButtonPhoto = F_Button[i]
                ButtonPhoto = InitButtonPhoto
                ImageButtonList.append(Button(button_space, command= lambda i=i: EditBack(i), bd=3, width=85,
                                  height=110, image=ButtonPhoto))
                ImageButtonList[i].grid(row=Ordered_yCoord[i], column=Ordered_xCoord[i])
    else:
        showinfo(title="Error: Non-Integer Input", message="Oh no! It looks like one or two of the inputs aren't "
                                                           "integers. Try again.")

#Input Widgets
Image_Upload = Button(input_window, text="Select an Image", command=uploadImage)
SectionPrompt = Label(input_window, text="How many sections do you want?")
Section_Number = Entry(input_window)
CoordPrompt = Label(input_window, text="How many coordinate options do you want?")
Coord_Number = Entry(input_window)
InputSubmitButt = Button(input_window, text="Submit",command=Submit, state=DISABLED)
IBlank_Label = Label(input_window, text="    ")

#Input Grid Layouts
Image_Upload.grid(row=0, column=0)
SectionPrompt.grid(row=0, column=2)
Section_Number.grid(row=0, column=3)
IBlank_Label.grid(row=0, column=4)
CoordPrompt.grid(row=0, column=5)
Coord_Number.grid(row=0, column=6)
InputSubmitButt.grid(row=0, column=8)

#Save Window Widget Actions
def DeeperInstructions():
    showinfo(title="More in Depth", message="Your printer options will determine what to check. "
                                            "If you have front and back printing, I suggest checking "
                                            "both front and back printing. If you only have front "
                                            "printing, I suggest saving front and back separately "
                                            "with different names.")

def SaveFile():
    global F_Crop, BackList, PaperOrientation, Pic_PerPage, Ordered_xCoord, Ordered_yCoord
    FinalFileName = str(FileNamer.get())
    InstructionsPrint = Instructions_CheckVal.get()
    FrontPrint = Front_CheckVal.get()
    BackPrint = Back_CheckVal.get()
    Pic_PerPage = ValPic_PerPage.get()
    ConfirmDoubleSided = ValDoublesided.get()
    if ConfirmDoubleSided == 1:
        FrontPrint == 1
        BackPrint == 1
    else:
        pass
    PrintOrder =[]
#Add instructions
    if InstructionsPrint == 1:
        PrintOrder.append(Image.open('PBU Printed Instructions.png'))
        if FrontPrint == 1 and BackPrint == 1:
            if PaperOrientation == -1:
                BlankPiece = Image.new(mode="RGBA", size=(2550,3300), color=(255,255,255))
                BlankPiece.save('Blank.png')
                PrintOrder.append(Image.open('Blank.png'))
            else:
                BlankPiece = Image.new(mode="RGBA", size=(3300,2550), color=(255,255,255))
                BlankPiece.save('Blank.png')
                PrintOrder.append(Image.open('Blank.png'))
        else:
            pass
    else:
        pass
    if FrontPrint == 0 and BackPrint == 0:
        pass
#four per page
    elif Pic_PerPage == 4:
#if portrait
        if PaperOrientation == -1:
    #Resize sides
            for i in range(len(BackList)):
                resizeFront = Image.open('{}.png'.format(i))
                resizeBack = Image.open('Back{}.png'.format(i))
                backsave = resizeBack.resize((1273,1648))
                backsave.save('Back{}.png'.format(i))
                frontsave = resizeFront.resize((1273,1648))
                frontsave.save('{}.png'.format(i))
    #Front Only
            if FrontPrint == 1 and BackPrint == 0:
                for d in range(int((len(BackList))/4)):
                    f1 = Image.open('{}.png'.format(d))
                    f2 = Image.open('{}.png'.format((d + 1)))
                    f3 = Image.open('{}.png'.format((d + 2)))
                    f4 = Image.open('{}.png'.format((d + 3)))
                    AddtoFront = Image.new(mode="RGBA", size=(2550, 3300), color=(241, 231, 64))
                    AddtoFront.paste(f1, box=(1, 1, 1274, 1649))
                    AddtoFront.paste(f2, box=(1276, 1, 2549, 1649))
                    AddtoFront.paste(f3, box=(1, 1651, 1274, 3299))
                    AddtoFront.paste(f4, box=(1276, 1651, 2549, 3299))
                    AddtoFront.save('Front{}.png'.format(d))
                    PrintOrder.append(Image.open('Front{}.png'.format(d)))
                if (len(BackList))%4 != 0:
                    Extras = (len(BackList))%4
                    d = int(len(BackList) / 4)
                    if Extras == 1:
                        LastFront = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        LastFront.paste('{}.png'.format((4 * d)), box=(1, 1, 1274, 1649))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))
                    elif Extras == 2:
                        LastFront = Image.new(mode="RGB", size=(2550, 3300), color=(255, 255, 255))
                        LastFront.paste('{}.png'.format((4 * d)), box=(0,0,1275,1650))
                        LastFront.paste('{}.png'.format((4*d + 1)), box=(1275,0,2550,3300))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append('Front{}.png'.format((d + 1)))
                    else:
                        LastFront = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        LastFront.paste('Back{}.png'.format((4 * d)), box=(1, 1, 1274, 1649))
                        LastFront.paste('Back{}.png'.format((4 * d + 1)), box=(1276, 1, 2549, 1649))
                        LastFront.paste('Back{}.png'.format((4 * d + 2)), box=(1, 1651, 1274, 3299))
                        LastFront.save('BackPage{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                else:
                    pass
    #Back only
            elif FrontPrint == 0 and BackPrint == 1:
                for d in range(int((len(BackList))/4)):
                    b1 = Image.open('Back{}.png'.format(d))
                    b2 = Image.open('Back{}.png'.format((d + 1)))
                    b3 = Image.open('Back{}.png'.format((d + 2)))
                    b4 = Image.open('Back{}.png'.format((d + 3)))
                    AddtoBack = Image.new(mode="RGBA", size=(2550, 3300), color=(241, 231, 64))
                    AddtoBack.paste(b1, box=(1, 1, 1274, 1649))
                    AddtoBack.paste(b2, box=(1276, 1, 2549, 1649))
                    AddtoBack.paste(b3, box=(1, 1651, 1274, 3299))
                    AddtoBack.paste(b4, box=(1276, 1651, 2549, 3299))
                    AddtoBack.save('BackPage{}.png'.format(d))
                    PrintOrder.append(Image.open('BackPage{}.png'.format(d)))
                if (len(BackList))%4 != 0:
                    Extras = (len(BackList))%4
                    d = int(len(BackList) / 4)
                    if Extras == 1:
                        LastFront = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        LastFront.paste('Back{}.png'.format((4 * d)), box=(1, 1, 1274, 1649))
                        LastFront.save('BackPage{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                    elif Extras == 2:
                        LastFront = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        LastFront.paste('{}.png'.format((4 * d)), box=(1, 1, 1274, 1649))
                        LastFront.paste('{}.png'.format((4 * d + 1)), box=(1276, 1, 2549, 1649))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))
                    else:
                        LastFront = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        LastFront.paste('Back{}.png'.format((4 * d)), box=(1, 1, 1274, 1649))
                        LastFront.paste('Back{}.png'.format((4 * d + 1)), box=(1276, 1, 2549, 1649))
                        LastFront.paste('Back{}.png'.format((4 * d + 2)), box=(1, 1651, 1274, 3299))
                        LastFront.save('BackPage{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                else:
                    pass
    #Front and Back
            elif FrontPrint == 1 and BackPrint == 1:
                for d in range(int((len(BackList)) / 4)):
                    f1 = Image.open('{}.png'.format(d))
                    f2 = Image.open('{}.png'.format((d + 1)))
                    f3 = Image.open('{}.png'.format((d + 2)))
                    f4 = Image.open('{}.png'.format((d + 3)))
                    AddtoFront = Image.new(mode="RGBA", size=(2550, 3300), color=(241, 231, 64))
                    AddtoFront.paste(f1, box=(1,1,1274,1649))
                    AddtoFront.paste(f2, box=(1276,1,2549,1649))
                    AddtoFront.paste(f3, box=(1,1651, 1274,3299))
                    AddtoFront.paste(f4, box=(1276,1651, 2549, 3299))
                    AddtoFront.save('Front{}.png'.format(d))
                    PrintOrder.append(Image.open('Front{}.png'.format(d)))
#break here with if statement
                    if ConfirmDoubleSided == 1:
                        b1 = Image.open('Back{}.png'.format(d))
                        b2 = Image.open('Back{}.png'.format((d + 1)))
                        b3 = Image.open('Back{}.png'.format((d + 2)))
                        b4 = Image.open('Back{}.png'.format((d + 3)))
                        AddtoBack = Image.new(mode="RGBA", size=(2550, 3300), color=(241, 231, 64))
                        AddtoBack.paste(b2, box=(1, 1, 1274, 1649))
                        AddtoBack.paste(b1, box=(1276, 1, 2549, 1649))
                        AddtoBack.paste(b4, box=(1, 1651, 1274, 3299))
                        AddtoBack.paste(b3, box=(1276, 1651, 2549, 3299))
                        AddtoBack.save('BackPage{}.png'.format(d))
                        PrintOrder.append(Image.open('BackPage{}.png'.format(d)))
                    else:
                        b1 = Image.open('Back{}.png'.format(d))
                        b2 = Image.open('Back{}.png'.format((d + 1)))
                        b3 = Image.open('Back{}.png'.format((d + 2)))
                        b4 = Image.open('Back{}.png'.format((d + 3)))
                        AddtoBack = Image.new(mode="RGBA", size=(2550, 3300), color=(241, 231, 64))
                        AddtoBack.paste(b1, box=(1,1,1274,1649))
                        AddtoBack.paste(b2, box=(1276,1,2549,1649))
                        AddtoBack.paste(b3, box=(1,1651, 1274,3299))
                        AddtoBack.paste(b4, box=(1276,1651, 2549, 3299))
                        AddtoBack.save('BackPage{}.png'.format(d))
                        PrintOrder.append(Image.open('BackPage{}.png'.format(d)))
                if (len(BackList)) % 4 != 0:
                    d = int(len(BackList)/4)
                    Extras = (len(BackList)) % 4
                    if Extras == 1:
                        LastFront = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        lf1 = Image.open('{}.png'.format((4 * d)))
                        LastFront.paste(lf1, box=(1,1,1274,1649))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))

                        if ConfirmDoubleSided == 1:
                            LastBack = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            LastBack.paste(lb1, box=(1276, 1, 2549, 1649))
                            LastBack.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                        else:
                            LastBack = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            LastBack.paste(lb1, box=(1,1,1274,1649))
                            LastBack.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                    elif Extras == 2:
                        LastFront = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        lf1 = Image.open('{}.png'.format((4 * d)))
                        lf2 = Image.open('{}.png'.format((4 * d + 1)))
                        LastFront.paste(lf1, box=(1,1,1274,1649))
                        LastFront.paste(lf2, box=(1276,1,2549,1649))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))

                        if ConfirmDoubleSided == 1:
                            LastBack = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                            LastBack.paste(lb2, box=(1, 1, 1274, 1649))
                            LastBack.paste(lb1, box=(1276, 1, 2549, 1649))
                            LastBack.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                        else:
                            LastBack = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                            LastBack.paste(lb1, box=(1,1,1274,1649))
                            LastBack.paste(lb2, box=(1276,1,2549,1649))
                            LastBack.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                    else:
                        LastFront = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        lf1 = Image.open('{}.png'.format((4 * d)))
                        lf2 = Image.open('{}.png'.format((4 * d + 1)))
                        lf3 = Image.open('{}.png'.format((4 * d + 2)))
                        LastFront.paste(lf1, box=(1,1,1274,1649))
                        LastFront.paste(lf2, box=(1276,1,2549,1649))
                        LastFront.paste(lf3, box=(1,1651,1274,3299))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))

                        LastBack = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
                        lb1 = Image.open('Back{}.png'.format((4 * d)))
                        lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                        lb3 = Image.open('Back{}.png'.format((4 * d + 2)))
                        LastBack.paste(lb2, box=(1,1,1274,1649))
                        LastBack.paste(lb1, box=(1276,1,2549,1649))
                        LastBack.paste(lb3, box=(1276,1651,2549,3299))
                        LastBack.save('BackPage{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                else:
                    pass
            else:
                pass
# landscape 4x4
        else:
            for i in range(len(BackList)):
                resizeFront = Image.open('{}.png'.format(i))
                resizeBack = Image.open('Back{}.png'.format(i))
                backrotate = resizeBack.rotate(90, expand=True)
                backsave = backrotate.resize((1648, 1273))
                backsave.save('Back{}.png'.format(i))
                frontsave = resizeFront.resize((1648, 1273))
                frontsave.save('{}.png'.format(i))
#front only
            if FrontPrint == 1 and BackPrint == 0:
                for d in range(int((len(BackList)) / 4)):
                    f1 = Image.open('{}.png'.format(d))
                    f2 = Image.open('{}.png'.format((d + 1)))
                    f3 = Image.open('{}.png'.format((d + 2)))
                    f4 = Image.open('{}.png'.format((d + 3)))
                    AddtoFront = Image.new(mode="RGBA", size=(3300, 2550), color=(241, 231, 64))
                    AddtoFront.paste(f1, box=(1, 1, 1649, 1274))
                    AddtoFront.paste(f2, box=(1651, 1, 3299, 1274))
                    AddtoFront.paste(f3, box=(1, 1276, 1649, 2549))
                    AddtoFront.paste(f4, box=(1651, 1276, 3299, 2549))
                    AddtoFront.save('Front{}.png'.format(d))
                    PrintOrder.append(Image.open('Front{}.png'.format(d)))
                if (len(BackList)) % 4 != 0:
                    Extras = (len(BackList)) % 4
                    d = int(len(BackList) / 4)
                    if Extras == 1:
                        LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lf1 = Image.open('{}.png'.format((4 * d)))
                        LastFront.paste(lf1, box=(1, 1, 1649, 1274))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))
                    elif Extras == 2:
                        LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lf1 = Image.open('{}.png'.format((4 * d)))
                        lf2 = Image.open('{}.png'.format((4 * d + 1)))
                        LastFront.paste(lf1, box=(1, 1, 1649, 1274))
                        LastFront.paste(lf2, box=(1651, 1, 3299, 1274))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))
                    else:
                        LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lf1 = Image.open('Back{}.png'.format((4 * d)))
                        lf2 = Image.open('Back{}.png'.format((4 * d + 1)))
                        lf3 = Image.open('Back{}.png'.format((4 * d + 2)))
                        LastFront.paste(lf1, box=(1, 1, 1649, 1274))
                        LastFront.paste(lf2, box=(1651, 1, 3299, 1274))
                        LastFront.paste(lf3, box=(1, 1276, 1649, 2549))
                        LastFront.save('BackPage{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                else:
                    pass
            elif FrontPrint == 0 and BackPrint == 1:
                for d in range(int((len(BackList)) / 4)):
                    b1 = Image.open('Back{}.png'.format(d))
                    b2 = Image.open('Back{}.png'.format((d + 1)))
                    b3 = Image.open('Back{}.png'.format((d + 2)))
                    b4 = Image.open('Back{}.png'.format((d + 3)))
                    AddtoBack = Image.new(mode="RGBA", size=(3300, 2550), color=(241, 231, 64))
                    AddtoBack.paste(b1, box=(1, 1, 1649, 1274))
                    AddtoBack.paste(b2, box=(1651, 1, 3299, 1274))
                    AddtoBack.paste(b3, box=(1, 1276, 1649, 2549))
                    AddtoBack.paste(b4, box=(1651, 1276, 3299, 2549))
                    AddtoBack.save('BackPage{}.png'.format(d))
                    PrintOrder.append(Image.open('BackPage{}.png'.format(d)))
                if (len(BackList)) % 4 != 0:
                    Extras = (len(BackList)) % 4
                    d = int(len(BackList) / 4)
                    if Extras == 1:
                        LastBack = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lb1 = Image.open('Back{}.png'.format((4 * d)))
                        LastBack.paste(lb1, box=(1, 1, 1649, 1274))
                        LastBack.save('BackPage{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                    elif Extras == 2:
                        LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lb1 = Image.open('Back{}.png'.format((4 * d)))
                        lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                        LastFront.paste(lb1, box=(1, 1, 1649, 1274))
                        LastFront.paste(lb2, box=(1651, 1, 3299, 1274))
                        LastFront.save('BackPage{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                    else:
                        LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lb1 = Image.open('Back{}.png'.format((4 * d)))
                        lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                        lb3 = Image.open('Back{}.png'.format((4 * d + 2)))
                        LastFront.paste(lb1, box=(1, 1, 1649, 1274))
                        LastFront.paste(lb2, box=(1651, 1, 3299, 1274))
                        LastFront.paste(lb3, box=(1, 1276, 1649, 2549))
                        LastFront.save('BackPage{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
#front and back
            elif FrontPrint == 1 and BackPrint == 1:
                for d in range(int((len(BackList)) / 4)):
                    f1 = Image.open('{}.png'.format(d))
                    f2 = Image.open('{}.png'.format((d + 1)))
                    f3 = Image.open('{}.png'.format((d + 2)))
                    f4 = Image.open('{}.png'.format((d + 3)))
                    AddtoFront = Image.new(mode="RGBA", size=(3300, 2550), color=(241, 231, 64))
                    AddtoFront.paste(f1, box=(1, 1, 1649, 1274))
                    AddtoFront.paste(f2, box=(1651, 1, 3299, 1274))
                    AddtoFront.paste(f3, box=(1, 1276, 1649, 2549))
                    AddtoFront.paste(f4, box=(1651, 1276, 3299, 2549))
                    AddtoFront.save('Front{}.png'.format(d))
                    PrintOrder.append(Image.open('Front{}.png'.format(d)))

                    if ConfirmDoubleSided == 1:
                        b1 = Image.open('Back{}.png'.format(d))
                        b2 = Image.open('Back{}.png'.format((d + 1)))
                        b3 = Image.open('Back{}.png'.format((d + 2)))
                        b4 = Image.open('Back{}.png'.format((d + 3)))
                        AddtoBack = Image.new(mode="RGBA", size=(3300, 2550), color=(241, 231, 64))
                        AddtoBack.paste(b3, box=(1, 1, 1649, 1274))
                        AddtoBack.paste(b4, box=(1651, 1, 3299, 1274))
                        AddtoBack.paste(b1, box=(1, 1276, 1649, 2549))
                        AddtoBack.paste(b2, box=(1651, 1276, 3299, 2549))
                        AddtoBack.save('BackPage{}.png'.format(d))
                        PrintOrder.append(Image.open('BackPage{}.png'.format(d)))
                    else:
                        b1 = Image.open('Back{}.png'.format(d))
                        b2 = Image.open('Back{}.png'.format((d + 1)))
                        b3 = Image.open('Back{}.png'.format((d + 2)))
                        b4 = Image.open('Back{}.png'.format((d + 3)))
                        AddtoBack = Image.new(mode="RGBA", size=(3300, 2550), color=(241, 231, 64))
                        AddtoBack.paste(b1, box=(1, 1, 1649, 1274))
                        AddtoBack.paste(b2, box=(1651, 1, 3299, 1274))
                        AddtoBack.paste(b3, box=(1, 1276, 1649, 2549))
                        AddtoBack.paste(b4, box=(1651, 1276, 3299, 2549))
                        AddtoBack.save('BackPage{}.png'.format(d))
                        PrintOrder.append(Image.open('BackPage{}.png'.format(d)))
                if (len(BackList)) % 4 != 0:
                    d = int(len(BackList) / 4)
                    Extras = (len(BackList)) % 4
                    if Extras == 1:
                        LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lf1 = Image.open('{}.png'.format((4*d)))
                        LastFront.paste(lf1, box=(1, 1, 1649, 1274))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))
                        if ConfirmDoubleSided == 1:
                            LastBack = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            LastBack.paste(lb1, box=(1, 1276, 1649, 2549))
                            LastBack.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                        else:
                            LastBack = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4*d)))
                            LastBack.paste(lb1, box=(1, 1, 1649, 1274))
                            LastBack.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                    elif Extras == 2:
                        LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lf1 = Image.open('{}.png'.format((4 * d)))
                        lf2 = Image.open('{}.png'.format((4 * d + 1)))
                        LastFront.paste(lf1, box=(1, 1, 1649, 1274))
                        LastFront.paste(lf2, box=(1651, 1, 3299, 1274))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))
                        if ConfirmDoubleSided == 1:
                            LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                            LastFront.paste(lb1, box=(1, 1276, 1649, 2549))
                            LastFront.paste(lb2, box=(1651, 1276, 3299, 2549))
                            LastFront.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                        else:
                            LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                            LastFront.paste(lb1, box=(1, 1, 1649, 1274))
                            LastFront.paste(lb2, box=(1651, 1, 3299, 1274))
                            LastFront.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                    else:
                        LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                        lf1 = Image.open('{}.png'.format((4 * d)))
                        lf2 = Image.open('{}.png'.format((4 * d + 1)))
                        lf3 = Image.open('{}.png'.format((4 * d + 2)))
                        LastFront.paste(lf1, box=(1, 1, 1649, 1274))
                        LastFront.paste(lf2, box=(1651, 1, 3299, 1274))
                        LastFront.paste(lf3, box=(1, 1276, 1649, 2549))
                        LastFront.save('Front{}.png'.format((d + 1)))
                        PrintOrder.append(Image.open('Front{}.png'.format((d + 1))))
                        if ConfirmDoubleSided == 1:
                            LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                            lb3 = Image.open('Back{}.png'.format((4 * d + 2)))
                            LastFront.paste(lb3, box=(1, 1, 1649, 1274))
                            LastFront.paste(lb2, box=(1651, 1276, 3299, 2549))
                            LastFront.paste(lb1, box=(1, 1276, 1649, 2549))
                            LastFront.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
                        else:
                            LastFront = Image.new(mode="RGBA", size=(3300, 2550), color=(255, 255, 255))
                            lb1 = Image.open('Back{}.png'.format((4 * d)))
                            lb2 = Image.open('Back{}.png'.format((4 * d + 1)))
                            lb3 = Image.open('Back{}.png'.format((4 * d + 2)))
                            LastFront.paste(lb1, box=(1, 1, 1649, 1274))
                            LastFront.paste(lb2, box=(1651, 1, 3299, 1274))
                            LastFront.paste(lb3, box=(1, 1276, 1649, 2549))
                            LastFront.save('BackPage{}.png'.format((d + 1)))
                            PrintOrder.append(Image.open('BackPage{}.png'.format((d + 1))))
            else:
                pass

#One piece of paper
    else:
        for i in range(len(F_Crop)):
            forresize = Image.open('{}.png'.format(i))
            if PaperOrientation == -1:
                forsave = forresize.resize((2550,3300))
                forsave.save('{}.png'.format(i))
            else:
                forsave = forresize.resize((3300,2550))
                forsave.save('{}.png'.format(i))
        #front only
        if FrontPrint == 1 and BackPrint == 0:
            for i in range(len(F_Crop)):
                Front_Temp = Image.open('{}.png'.format(i))
                PrintOrder.append(Front_Temp)
        #back only
        elif FrontPrint == 0 and BackPrint == 1:
            for i in range(len(BackList)):
                back_temp = Image.open(BackList[i])
                PrintOrder.append(back_temp)
        #front and back
        elif FrontPrint == 1 and BackPrint == 1:
            for i in range(len(F_Crop)):
                Front_Temp = Image.open('{}.png'.format(i))
                PrintOrder.append(Front_Temp)
                back_temp = Image.open(BackList[i])
                PrintOrder.append(back_temp)


# Key picture
    KeyPage = Image.new(mode="RGBA", size=(2550, 3300), color=(255, 255, 255))
    EditableKeyPage = ImageDraw.Draw(KeyPage)
    EditableKeyPage.text((1275, 5), "Key", fill=(0, 0, 0))
    for i in range(len(BackList)):
        global Alphabet
        LoadPicture = Image.open('Button{}.png'.format(i))
        KeyPictures = LoadPicture
        KeyPicWithCoords = ImageDraw.Draw(KeyPictures)
        CorrectCoords = "(" + Alphabet[(Ordered_xCoord[i])-1] + "," + Alphabet[(Ordered_yCoord[i])-1] + ")"
        KeyPicWithCoords.text((5, 5), CorrectCoords, fill=(255, 0, 255))
        KeyPictures = KeyPictures.resize((3 * LoadPicture.width, 3 * LoadPicture.height))
        KeyPage.paste(KeyPictures, box=(Ordered_xCoord[i] * KeyPictures.width + 5,
                                        Ordered_yCoord[i] * KeyPictures.height + 20,
                                        (Ordered_xCoord[i] * KeyPictures.width + 5) + KeyPictures.width,
                                        (Ordered_yCoord[i] * KeyPictures.height + 20) + KeyPictures.height
                                        ))
    KeyPage.save('Key.png')
    PrintOrder.append(Image.open('Key.png'))

#Get ready to print
    for i in range(len(PrintOrder)):
        PrintOrder[i] = PrintOrder[i].convert('RGB')
    FirstPage = PrintOrder[0]
    PrintOrder.pop(0)
    FirstPage.save('{}.pdf'.format(FinalFileName), save_all=True, append_images=PrintOrder)
    showinfo(title="Complete", message="Your request has been completed!")
    End_Program.place(relx=0.3, rely=0.95)

def EndProgram():
    os.remove('Padded.png')
    os.remove('Key.png')
    for i in range(len(BackList)):
        buttonremove = 'Button{}.png'.format(i)
        frontremove = '{}.png'.format(i)
        backremove = 'Back{}.png'.format(i)
        os.remove(buttonremove)
        os.remove(frontremove)
        os.remove(backremove)
    if Pic_PerPage == 4:
        for i in range(int((len(BackList)/4))):
            fourfrontremove = 'Front{}.png'.format(i)
            fourbackremove = 'BackPage{}.png'.format(i)
            os.remove(fourfrontremove)
            os.remove(fourbackremove)
        if (len(BackList))%4 != 0:
            extrafrontremove = 'Front{}.png'.format((int((len(BackList))/4)+1))
            extrabackremove = 'BackPage{}.png'.format((int((len(BackList)) / 4) + 1))
            os.remove(extrabackremove)
            os.remove(extrafrontremove)
    root.destroy()

#Save Window Widgets
SaveTitle = Label(save_window, text="Save Options")
Instructions_CheckVal = IntVar()
Instructions_Check = Checkbutton(save_window, text="Include Instructions in Print", variable=Instructions_CheckVal)
Front_CheckVal = IntVar()
Front_Check = Checkbutton(save_window, text="Include Front Pages in Print", variable=Front_CheckVal)
Back_CheckVal = IntVar()
Back_Check = Checkbutton(save_window, text="Include Back Pages in Print", variable=Back_CheckVal)
Save_Button = Button(save_window, text="Save", command=SaveFile)
Save_Confirm = Label(action_window, text="Save Confirmed")
FileNamePrompt = Label(save_window, text="Filename:")
FileNamer = Entry(save_window)
Explanation = Button(save_window, text="What should I check?", command=DeeperInstructions)
LogoForSaveWindow = ImageTk.PhotoImage(Image.open('Icon.png'))
Logo = Label(save_window, image=LogoForSaveWindow)
ValPic_PerPage = IntVar()
OnePic_PerPage = Radiobutton(save_window, text="One Piece per 8.5x11 page",
                             variable=ValPic_PerPage, value=1)
FourPic_PerPage = Radiobutton(save_window, text="Four Pieces per 8.5x11 page",
                              variable=ValPic_PerPage, value=4)
End_Program = Button(save_window, text="Close Program", command=EndProgram)
ValDoublesided = IntVar()
PrintDoubleSided = Checkbutton(save_window, text="Double-Sided Printing",
                               variable=ValDoublesided)

#Save Grid Layouts
SaveTitle.place(x=5, y=5)
Explanation.place(x=5, y=30)
Instructions_Check.place(relx=0.1, rely=0.15)
Front_Check.place(relx=0.1, rely=0.18)
Back_Check.place(relx=0.1, rely=0.21)
OnePic_PerPage.place(relx=0.1, rely=0.30)
FourPic_PerPage.place(relx=0.1, rely=0.33)
PrintDoubleSided.place(relx=0.1, rely=0.39)
FileNamePrompt.place(relx=0.1, rely=0.45)
FileNamer.place(relx=0.1, rely=0.48)
Save_Button.place(relx=0.1, rely=0.51)
Logo.place(relx=0.3, rely=0.7)

#Action Window Widget Actions

# add coordinate options

ShownCoordinateList = []
OptionalBackImages = []
def EditBack(buttonid):
    global DefaultCoordinates, ImageButtonList, OptionalImageButton
    EditWindow = Tk()
    EditWindow.title("Edit Window")
    EditWindow.geometry('532x688')

    #frames
    EditorArea = Frame(EditWindow, width=532, height=200, bd=2)
    EditorArea.grid(row=1, columnspan=2)
    CoordinateArea = Frame(EditWindow, width=532, height=258, bd=2, bg="grey")
    CoordinateArea.grid(row=6, columnspan=2, rowspan=2, sticky='S')
    OptionalPictureFrame = Frame(EditWindow, width=532, height=230)
    OptionalPictureFrame.grid(row=2, columnspan=2, rowspan=3)

    #widgets
    PromptWriter = Text(EditorArea, bd=2, font=("Arial", 16))
    PromptWriter.pack(side=TOP, expand=False)
    EditorArea.pack_propagate(False)
    PromptWriter.insert(INSERT," ")

    interuserbackpic = Image.open('/Users/henrymelzer/PycharmProjects/CoordinateMath/sample.jpg')
    def UploadBackImage():
        global interuserbackpic, OptionalBackImages, Alphabet
        OptionalImageButton.pack_forget()
        filetypes = (
            ('Pictures', '*.png'),
            ('Pictures', '*.jpg')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        interuserback_pic = Image.open(filename)
        #Biggest over by
        WidthDifference = (interuserback_pic.width - 532)/(interuserback_pic.width)
        HeightDifference = (interuserback_pic.height - 230)/(interuserback_pic.height)
        if WidthDifference and HeightDifference < 0:
            pass
        elif WidthDifference > HeightDifference:
            interuserback_pic = interuserback_pic.resize((532, int((532*interuserback_pic.height)/(
                interuserback_pic.width))))
        else:
            interuserback_pic = interuserback_pic.resize((int((230*interuserback_pic.width)/(
                interuserback_pic.height)), 230))
        interuserback_pic = interuserback_pic.convert('RGB')
        userback_pic = ImageTk.PhotoImage(interuserback_pic, master=EditWindow)
        OptionalBackImages.append(userback_pic)
        PostedBackPic = Label(OptionalPictureFrame, image=userback_pic)
        PostedBackPic.pack(fill=BOTH, expand=NO)
        if filename:
            pass
        else:
            OptionalImageButton.pack()

    OptionalImageButton = Button(OptionalPictureFrame,text="Optional Image (This button will disappear on print)",
                                 command=UploadBackImage)
    OptionalImageButton.pack()


    Correct_XCoordinate = Alphabet[(Ordered_xCoord[buttonid])-1]
    Correct_YCoordinate = Alphabet[(Ordered_yCoord[buttonid])-1]
    Correct_Coordinates = "("+Correct_XCoordinate+","+Correct_YCoordinate+")"
    CoordinateList = []
    for m in range(len(Ordered_xCoord)):
        createXcoords = Alphabet[(Ordered_xCoord[m])-1]
        createYcoords = Alphabet[(Ordered_yCoord[m])-1]
        createcoords = "("+createXcoords+","+createYcoords+")"
        CoordinateList.append(createcoords)
    OffsetCoords = DefaultCoordinates - 1
    ShownCoordinateList.append(Label(CoordinateArea,text=Correct_Coordinates+":", fg="green", font=("Arial", 12)))
    while OffsetCoords > 0:
        if Correct_Coordinates in CoordinateList:
            CoordinateList.pop(CoordinateList.index(Correct_Coordinates))
        else:
            generated_coordinate = random.choice(CoordinateList)
            CoordinateList.pop(CoordinateList.index(generated_coordinate))
            ShownCoordinateList.append(Label(CoordinateArea, text=generated_coordinate+":", font=("Arial", 12)))
            OffsetCoords -= 1
    WidgetPoppers =[]
    AnswerSpaces = []
    CoordinateShownOrder =[]


    def WidgetCoordinatePopper(CoordinateSpace, AnswerSpace,PoppedWidget):
        CoordinateSpace.grid_remove()
        AnswerSpace.grid_remove()
        PoppedWidget.grid_remove()

    #list needed otherwise object can't find itself
    #AddCoordinateRow = []
    #def AddCoordinates():
    #    global AddCoordinateRow
    #    IndexSpot = len(AddCoordinateRow)-1
    #    AddCoordinateRow[IndexSpot].grid_remove()
    #    rownumber = len(CoordinateShownOrder) + 1
    #    anotheroption = random.choice(CoordinateList)
    #    CoordinateList.pop(CoordinateList.index(anotheroption))
    #    postcoord = Label(CoordinateArea,text=anotheroption+ ":", font=("Arial", 12))
    #    postcoord.grid(column=0,row=rownumber)
    #    CoordinateShownOrder.append(postcoord)
    #    ShownCoordinateList.pop(ShownCoordinateList.index(postcoord))
    #    AnswerSpaces.append(Entry(CoordinateArea,font=("Arial", 12), width=60))
    #    AnswerSpaces[rownumber].grid(column=1, row=rownumber)
    #    WidgetPoppers.append(Button(CoordinateArea, text="X", fg="red", bg="red",bd=2, command=
    #                                lambda rownumber=m: WidgetCoordinatePopper(CoordinateShownOrder[m],AnswerSpaces[m],
    #                                                                   WidgetPoppers[m])))
    #    WidgetPoppers[rownumber].grid(column=2,row=rownumber)
    #    AddCoordinateRow = Button(CoordinateArea, text="Add another row", bd=2, fg="yellow", bg="yellow",
    #                              command=AddCoordinates)
    #    AddCoordinateRow.grid(column=1,row=rownumber+1)

    for m in range(DefaultCoordinates):
        postcoord = random.choice(ShownCoordinateList)
        postcoord.grid(column=0,row=m)
        CoordinateShownOrder.append(postcoord)
        ShownCoordinateList.pop(ShownCoordinateList.index(postcoord))
        AnswerSpaces.append(Entry(CoordinateArea,font=("Arial", 12), width=60))
        AnswerSpaces[m].grid(column=1, row=m)
        WidgetPoppers.append(Button(CoordinateArea, text="X", fg="red", bg="red",bd=2, command=
                                    lambda m=m: WidgetCoordinatePopper(CoordinateShownOrder[m],AnswerSpaces[m],
                                                                       WidgetPoppers[m])))
        WidgetPoppers[m].grid(column=2,row=m)

#    AddCoordinateRow.append(Button(CoordinateArea, text="Add another row",bd=2,fg="yellow",bg="yellow",
#                              command=AddCoordinates))
#    AddCoordinateRow[len(AddCoordinateRow)-1].grid(column=1,row=len(CoordinateShownOrder)+1)
    def FinalizeBack():
        global F_Crop, BackList
        for i in range(len(CoordinateShownOrder)):
            CoordinateShownOrder[i].config(fg="black")
        erasedbuttonlist = []
        OptionalImageButton.pack_forget()
        erasedbuttonlist.extend(WidgetPoppers)
        erasedbuttonlist.append(FinalizeEditButton)
        erasedbuttonlist.append(RefreshEditButton)
        for i in range(len(erasedbuttonlist)):
            try:
                erasedbuttonlist[i].grid_forget()
            except Exception:
                try:
                    erasedbuttonlist[i].pack_forget()
                except Exception:
                    try:
                        erasedbuttonlist[i].place_forget()
                    except:
                        pass

        Tk.update(EditWindow)
        WScaleFactor = int((EditWindow.winfo_screenwidth())/(EditWindow.winfo_screenmmwidth()))
        HScaleFactor = int(((EditWindow.winfo_screenheight())/(EditWindow.winfo_screenmmheight())))
        screenregion = [EditWindow.winfo_x(), EditWindow.winfo_y()+20,
                        EditWindow.winfo_x()+EditWindow.winfo_width(), EditWindow.winfo_y()+EditWindow.winfo_height()+20]
        x1 = (screenregion[0])*WScaleFactor
        y1 = ((screenregion[1])*HScaleFactor)
        x2 = (screenregion[2])*WScaleFactor
        y2 = (screenregion[3])*HScaleFactor
        Screencap = ImageGrab.grab()
        BackSave = Screencap.crop((x1, y1, x2, y2))
        BackSave.save('Back{}.png'.format(buttonid))
        BackList[buttonid] = 'Back{}.png'.format(buttonid)
#might need to replace buttonid with buttonid - 1
        (ImageButtonList[buttonid])["state"] = DISABLED
        (ImageButtonList[buttonid]).config(image=PhotoImage(file=''))
        if 'Back{}.png'.format(buttonid) in BackList:
            showinfo(title="Done!", message="This page has been saved.")
            try:
                erasedbuttonlist.pack()
            except Exception:
                try:
                    erasedbuttonlist.grid()
                except Exception:
                    pass
            EditWindow.quit()


    def RefreshEdit():
        showinfo(title="Oh no!", message="This feature is currently being built.")

    FinalizeEditButton = Button(EditWindow, text="Save for Back", command= FinalizeBack,
                                                                        fg="green", bd=2, bg="green")
    FinalizeEditButton.grid(row=0, column=0)
    RefreshEditButton = Button(EditWindow, text="Refresh Window", command=RefreshEdit, fg="red",
                      bd=2, bg="red")
    RefreshEditButton.grid(row=0, column=1)

    EditWindow.resizable(False,False)
    EditWindow.mainloop()

#Action Window Widgets



#Action Grid Layout





root.mainloop()
