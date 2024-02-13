#!/usr/bin/env python3
from tkinter import *  # python 3.x
from cmath import log, rect, polar, pi, e, sin, cos

class ComplexCalculator(Frame):

    digits = [str(i) for i in range(10)] + ["."] + ["E"]
    operators = ["+", "-", "*", "/", "1/x", "i", "y\u02e3", "e\u02e3", "ln(x)", "\u221Ax", "x<>y", "\u03c0","delX"]
    others = ["Enter", "prec", "cplx", "+/-"]
#    font1 = "Verdana 11"    
#    font2 = "Verdana 16" 
    font1 = "helv36 11"    
    font2 = "helv36 16" 
    buttons = dict()
    overrideFlag = False
    numOk = True
    preciseFlag = True # prec 15 (True) or 4 (False) Nachkommastellen
    # Der Stack mit Tiefe = 4, d.h. numX, numY, numU und numT Register
    numX = 0.0000
    numY = 0.0000
    numU = 0.0000
    numT = 0.0000

    def __init__(self, master):
        Frame.__init__(self, master)
        master.wm_title("RPN ComplexCalc V 1.00")
        master.resizable(width=False, height=False)
        self.pack()
        self.create_widgets()
        self.bind_keys(master)

    def create_widgets(self):
        self.onDisplayX = StringVar()
        self.onDisplayX.set("0.0000")
        self.onDisplayY = StringVar()
        self.onDisplayY.set("0.0000")
        self.isDeg = BooleanVar()
        self.isDeg.set(True)
        self.isPolar = BooleanVar()
        self.isPolar.set(False)

        self.displayY = Label(self,
                             textvariable=self.onDisplayY,
                             font=self.font2,
                             bg="white",
                             borderwidth=5,
                             relief="groove",
                             width=28,
                             height=2,
                             anchor=E)
        self.displayX = Label(self,
                             textvariable=self.onDisplayX,
                             font=self.font2,
                             bg="white",
                             borderwidth=5,
                             relief="groove",
                             width=28,
                             height=2,
                             anchor=E)
        for digit in self.digits:
            self.buttons[digit] = Button(self,
                                         text=digit,
                                         font=self.font1,
                                         command=lambda d=digit: self.add_to_display(d),
                                         width=8,
                                         height=2)
        for operator in self.operators:
            self.buttons[operator] = Button(self,
                                            text=operator,
                                            font=self.font1,
                                            command=lambda o=operator: self.calculate(o),
                                            width=8,
                                            height=2)

        for other in self.others:
            if other == "Enter":
                command = self.enterNum
            elif other == "prec":
                command = self.showPreciseDisplay
            elif other == "cplx":
                command = self.press_complex
            elif other == "+/-":
                command = self.plusMinus

            self.buttons[other] = Button(self,
                                       text=other,
                                       font=self.font1,
                                       command=command,
                                       width=8,
                                       height=2)

        self.degRadioButton = Radiobutton(self,
                                              text="Deg",
                                              command=self.calcDeg,
                                              width=8,
                                              height=2,
                                              variable=self.isDeg,
                                              value=True
                                              )


        self.radRadioButton = Radiobutton(self,
                                              text="Rad",
                                              command=self.calcRad,
                                              width=8,
                                              height=2,
                                              variable=self.isDeg,
                                              value=False
                                              )
        
        self.polarRadioButton = Radiobutton(self,
                                              text="Polar",
                                              command=self.calcPolar,
                                              width=8,
                                              height=2,
                                              variable=self.isPolar,
                                              value=True
                                              )


        self.rectRadioButton = Radiobutton(self,
                                              text="Rect",
                                              command=self.calcRect,
                                              width=8,
                                              height=2,
                                              variable=self.isPolar,
                                              value=False
                                              )

        self.render_layout()

    def render_layout(self):

        self.displayY.grid(row=0, column=0, columnspan=4, sticky=W)
        self.displayX.grid(row=1, column=0, columnspan=4, sticky=W)
        
        self.degRadioButton.grid(row=3, column=0, sticky=W)
        self.radRadioButton.grid(row=3, column=1, sticky=W)
        self.rectRadioButton.grid(row=3, column=2, sticky=W)
        self.polarRadioButton.grid(row=3, column=3, sticky=W)


        self.buttons["0"].grid(row=10, column=0, sticky=W)       
        self.buttons["."].grid(row=10, column=1, sticky=W)
        self.buttons["E"].grid(row=10, column=2, sticky=W)
        self.buttons["Enter"].grid(row=10, column=3, sticky=W)

        self.buttons["1"].grid(row=9, column=0, sticky=W)
        self.buttons["2"].grid(row=9, column=1, sticky=W)
        self.buttons["3"].grid(row=9, column=2, sticky=W)
        self.buttons["+"].grid(row=9, column=3, sticky=W)

        self.buttons["4"].grid(row=8, column=0, sticky=W)
        self.buttons["5"].grid(row=8, column=1, sticky=W)
        self.buttons["6"].grid(row=8, column=2, sticky=W)
        self.buttons["-"].grid(row=8, column=3, sticky=W)

        self.buttons["7"].grid(row=7, column=0, sticky=W)
        self.buttons["8"].grid(row=7, column=1, sticky=W)
        self.buttons["9"].grid(row=7, column=2, sticky=W)
        self.buttons["*"].grid(row=7, column=3, sticky=W)

        self.buttons["\u03c0"].grid(row=6, column=0, sticky=W) # pi
        self.buttons["\u221Ax"].grid(row=6, column=1, sticky=W) # sqrt(x)
        self.buttons["e\u02e3"].grid(row=6, column=2, sticky=W) # e^x
        self.buttons["/"].grid(row=6, column=3, sticky=W)

        self.buttons["+/-"].grid(row=5, column=0, sticky=W)
        self.buttons["y\u02e3"].grid(row=5, column=1, sticky=W) #y^x
        self.buttons["ln(x)"].grid(row=5, column=2, sticky=W)
        self.buttons["1/x"].grid(row=5, column=3, sticky=W)

        self.buttons["delX"].grid(row=4, column=0, sticky=W)
        self.buttons["prec"].grid(row=4, column=1, sticky=W)
        self.buttons["x<>y"].grid(row=4, column=2, sticky=W)
        self.buttons["cplx"].grid(row=4, column=3, sticky=W)

        
        
    def bind_keys(self, master):
        for digit in self.digits:
            master.bind(digit, self.add_to_display)

        master.bind(".", self.add_to_display)
        master.bind("e", self.add_to_display)
        master.bind("<Return>", self.enterNum)
        master.bind('c', self.press_complex)
        master.bind('p', self.calcPolar)
        master.bind('r', self.calcRect)
        master.bind('g', self.calcDeg) # Degree: German --> Grad
        master.bind('b', self.calcRad) # Radian: German --> Bogenmaß
        master.bind('a', self.showPreciseDisplay) # a from accurate
        master.bind('s', self.plusMinus) # +/- --> sign

        master.bind("+", self.calculate)
        master.bind("-", self.calculate)
        master.bind("m", self.calculate) # multipication
        master.bind("d", self.calculate) # division
        master.bind('i', self.calculate) # 1/x --> inversion
        master.bind('x', self.calculate) # e^x --> x sounds like ex
        master.bind('w', self.calculate) # Square root: German --> Wurzel ziehen
        master.bind('t', self.calculate) # y^x --> to the power
        master.bind('l', self.calculate) # ln(x)
        master.bind('k', self.calculate) # pi --> German --> Kreiszahl
        master.bind('o', self.calculate) # delx --> rub out
        master.bind('v', self.calculate) # x<>y --> vice versa

    def calcRad(self, event=None):
        self.radRadioButton.select()
        if self.isDeg.get() == False:
            conversionFactor = pi/180
            if isinstance(self.numX, tuple):
                phi = self.numX[1] * conversionFactor
                self.numX = self.numX[0], phi
            if isinstance(self.numY, tuple):
                phi = self.numY[1] * conversionFactor
                self.numY = self.numY[0], phi
            if isinstance(self.numU, tuple):
                phi = self.numU[1] * conversionFactor
                self.numU = self.numU[0], phi
            if isinstance(self.numT, tuple):
                phi = self.numT[1] * conversionFactor
                self.numT = self.numT[0], phi
            self.checkDisplayInput(self.onDisplayX.get())
            self.showDisplays()

    def calcDeg(self, event=None):
        self.degRadioButton.select()
        if self.isDeg.get() == True:
            conversionFactor = 180/pi
            if isinstance(self.numX, tuple):
                phi = self.numX[1] * conversionFactor
                self.numX = self.numX[0], phi
            if isinstance(self.numY, tuple):
                phi = self.numY[1] * conversionFactor
                self.numY = self.numY[0], phi
            if isinstance(self.numU, tuple):
                phi = self.numU[1] * conversionFactor
                self.numU = self.numU[0], phi
            if isinstance(self.numT, tuple):
                phi = self.numT[1] * conversionFactor
                self.numT = self.numT[0], phi
            self.checkDisplayInput(self.onDisplayX.get())
            self.showDisplays()

    def polar2rect(self,betrag, phi):  # cmath.rect, WEGEN COS(90) NICHT NULL!
        if phi == pi/2:
            return betrag * (0.0 + sin(phi)*1j)
        elif phi == pi:
            return betrag * (cos(phi) + 0.0*1j)
        else:
            return betrag * (cos(phi) + sin(phi)*1j)

    def calcRect(self, event=None):
        self.rectRadioButton.select()
        conversionFactor = pi/180 if self.isDeg.get() else 1
        if isinstance(self.numX, tuple):
            self.numX = self.polar2rect(self.numX[0], self.numX[1] * conversionFactor)
        if isinstance(self.numY, tuple):
            self.numY = self.polar2rect(self.numY[0], self.numY[1] * conversionFactor)
        if isinstance(self.numU, tuple):
            self.numU = self.polar2rect(self.numU[0], self.numU[1] * conversionFactor)
        if isinstance(self.numT, tuple):
            self.numT = self.polar2rect(self.numT[0], self.numT[1] * conversionFactor)
        self.checkDisplayInput(self.onDisplayX.get())
        self.showDisplays()

    def calcPolar(self, event=None):
        self.polarRadioButton.select()
        conversionFactor = 180/pi if self.isDeg.get() else 1
        if isinstance(self.numX, complex):
            self.numX = polar(self.numX)
            self.numX = self.numX[0], self.numX[1] * conversionFactor
        if isinstance(self.numY, complex):
            self.numY = polar(self.numY)
            self.numY = self.numY[0], self.numY[1] * conversionFactor
        if isinstance(self.numU, complex):
            self.numU = polar(self.numU)
            self.numU = self.numU[0], self.numU[1] * conversionFactor
        if isinstance(self.numT, complex):
            self.numT = polar(self.numT)
            self.numT = self.numT[0], self.numT[1] * conversionFactor
        self.checkDisplayInput(self.onDisplayX.get())
        self.showDisplays()

    def checkDisplayInput(self, displayValue):
        if self.numOk == False:
            try:
                self.numX = float(displayValue)
            except ValueError:
                displayValue = displayValue + "0"
                self.numX = float(displayValue)
            self.numOk = True

    def showPreciseDisplay(self, event=None):
        self.checkDisplayInput(self.onDisplayX.get())
        formatE = ".15e"
        formatF = ".15f"
        if isinstance(self.numX, tuple):
            strFormat = formatE if ((abs(self.numX[0]) > 1E12 or abs(self.numX[0]) < 1E-4) and self.numX[0] != 0.0) else formatF
        else:
            strFormat = formatE if ((abs(self.numX.real) > 1E12 or abs(self.numX.real) < 1E-4) and self.numX.real != 0.0) else formatF
        if self.preciseFlag:
            if isinstance(self.numX, float):
                    self.onDisplayX.set(str(format(self.numX, strFormat)))
                    if isinstance(self.numY, float):
                        self.onDisplayY.set(str(format(self.numY, strFormat)))
            elif isinstance(self.numX, complex):
                realTeil = self.numX.real
                imagTeil = self.numX.imag
                self.onDisplayY.set(str(format(realTeil, strFormat)))
                self.onDisplayX.set(str(format(imagTeil, strFormat)))
            elif isinstance(self.numX, tuple):
                betrag = self.numX[0]
                phase = self.numX[1]
                self.onDisplayY.set(str(format(betrag, strFormat)))
                self.onDisplayX.set(str(format(phase, strFormat)))
            self.preciseFlag = False
        else:
            self.preciseFlag = True
            self.showDisplays()

    def showDisplays(self):
        formatE = ".4e"
        formatF = ".4f"
        self.preciseFlag = True
        if isinstance(self.numX, tuple):
            strFormat = formatE if ((abs(self.numX[0]) > 1E6 or abs(self.numX[0]) < 1E-4) and self.numX[0] != 0.0) else formatF
        else:
            strFormat =  formatE if ((abs(self.numX.real) > 1E6 or abs(self.numX.real) < 1E-4) and self.numX.real != 0.0) else formatF
        if  isinstance(self.numX, float):
            self.onDisplayX.set(str(format(self.numX, strFormat)))
        elif isinstance(self.numX, complex):
            if self.numX.imag != 0.0:
                self.onDisplayX.set(str(format(self.numX.real, strFormat))+ " i"+str(format(self.numX.imag, strFormat)))
            else:
                self.numX = self.numX.real
                self.onDisplayX.set(str(format(self.numX.real, strFormat)))
        elif isinstance(self.numX, tuple):
            self.onDisplayX.set(str(format(self.numX[0], strFormat)) +  " \u2220"  +  str(format(self.numX[1], ".4f")))
        if  isinstance(self.numY, float):
            self.onDisplayY.set(str(format(self.numY, strFormat)))
        elif isinstance(self.numY, complex):
            if self.numY.imag != 0.0:
                self.onDisplayY.set(str(format(self.numY.real, strFormat))+ " i"+str(format(self.numY.imag, strFormat)))
            else:
                self.onDisplayY.set(str(format(self.numY.real, strFormat)))
        elif isinstance(self.numY, tuple):
            self.onDisplayY.set(str(format(self.numY[0], strFormat)) +  " \u2220"  +  str(format(self.numY[1], ".4f")))

    def shiftStack(self):
        self.numT = self.numU
        self.numU = self.numY
        self.numY = self.numX

    def dropStack(self):
        self.numY = self.numU
        self.numU = self.numT

    def plusMinus(self, event=None):
        if self.numOk == True:
            if self.isPolar.get():
                self.calcRect()
                self.numX = -self.numX
                self.calcPolar()
            else:
               self.numX = -self.numX 
            self.showDisplays()
        else:
            val = self.onDisplayX.get()
            if "E" in val:
                exponent = val.split("E")
                if exponent[1]:
                    exponent[1] = "-"+exponent[1] if float(exponent[1]) > 0 else exponent[1].replace("-","")
                    val = exponent[0]+"E"+exponent[1]
            else:
                val = "-"+val if float(val) > 0 else val.replace("-","")
            self.onDisplayX.set(val)
        
    def calculate(self, op):
        if isinstance(op, Event): # Input via keyboard
            if op.char == "t":
                op = "y\u02e3"
            elif op.char == "w":
                op = "\u221Ax"
            elif op.char == "x":
                op = "e\u02e3"
            elif op.char == "k":
                op = "\u03c0"
            elif op.char == "o":
                op = "delX"
            elif op.char == "l":
                op = "ln(x)"
            elif op.char == "v":
                op = "x<>y"
            elif op.char == "d":
                op = "/"
            elif op.char == "m":
                op = "*"
            elif op.char == "i":
                op = "1/x"
            else:
                op = op.char
        if op and self.onDisplayX.get():
            self.checkDisplayInput(self.onDisplayX.get())
            if self.isPolar.get():
                self.calcRect()
                self.polarRadioButton.select()
            try:
                if op == "/":
                    self.numX = self.numY / self.numX
                if op == "*":
                    self.numX = self.numY * self.numX
                if op == "-":
                    self.numX = self.numY - self.numX
                if op == "+":
                    self.numX = self.numY + self.numX
                if op == "1/x":
                    self.numX = 1.0/self.numX
                if op == "y\u02e3":                   
                    self.numX = self.numY**self.numX
                if op == "x<>y":
                    bufferX = self.numX 
                    self.numX = self.numY
                    self.numY = bufferX
                if op == "\u03c0":
                    self.shiftStack()
                    self.numX = pi
                if op == "e\u02e3":
                    self.numX = e**self.numX
                if op == "ln(x)":
                    self.numX = log(self.numX)
                if op == "\u221Ax":
                    self.numX = self.numX**0.5
                if self.isPolar.get():
                    self.calcPolar()
                if op in ["/","*","-","+","y\u02e3"]:
                    self.dropStack()
                self.numOk = True
                self.overrideFlag = False
                if op == "delX":
                    self.numX = 0.0000
                    self.overrideFlag = True
                self.showDisplays()
            except Exception:
                valX = "Error"
                self.onDisplayX.set(valX)
                
    def add_to_display(self, value):
        if isinstance(value, Event): # Input via keyboard 
            if value.char == "e":
                value = "E"
            else:
                value = value.char
        if self.numOk == True:
            if self.overrideFlag == False:
                self.shiftStack()
            self.showDisplays()
            self.operationFlag = False
            self.numOk = False
            self.overrideFlag = False
            self.onDisplayX.set("")
        if self.onDisplayX.get() == "":
            if value =="E":
                value = "1E"
            elif value == ".":
                value = "0."
        if self.onDisplayX.get().find(".") >= 1  and value == ".":
            self.onDisplayX.set(self.onDisplayX.get())
        elif self.onDisplayX.get().find("E") >= 1 and (value == "E" or value == "."):
            self.onDisplayX.set(self.onDisplayX.get())
        else:
            self.onDisplayX.set(self.onDisplayX.get() + value)

    def enterNum(self, event=None):
        self.checkDisplayInput(self.onDisplayX.get())
        self.shiftStack()
        self.overrideFlag = True
        self.showDisplays()

    def angleCorrection(self, value):
        if self.isDeg.get():
            degRadValue = 360.0
        else:
            degRadValue = 2*pi
        if abs(value) >= degRadValue:
            return value%degRadValue
        if abs(value) >= degRadValue/2 and abs(value) < degRadValue:
           return value%(degRadValue/2) - degRadValue/2
        return value

    def press_complex(self, event=None):
        self.checkDisplayInput(self.onDisplayX.get())
        if isinstance(self.numX, complex):
            compNum = self.numX
            self.numX = compNum.real
            self.shiftStack()
            self.numX = compNum.imag
        elif isinstance (self.numX, tuple):
            compNum = self.numX
            self.numX = compNum[0]
            self.shiftStack()
            self.numX = compNum[1]
        elif isinstance (self.numX, float) and isinstance (self.numY, float):
            try:
                if not self.isPolar.get():
                    self.numX = complex(float(self.numY), float(self.numX))
                else:
                    self.numX = self.numY, self.angleCorrection(self.numX)
                self.dropStack() # U = T, Y = U
            except Exception:
                valX = "Error"
                self.onDisplayX.set(valX)
                self.overrideFlag = True
                return
        self.showDisplays()
        self.overrideFlag = False           




if __name__ == "__main__":
    root = Tk()
    app = ComplexCalculator(root)
    app.mainloop()

