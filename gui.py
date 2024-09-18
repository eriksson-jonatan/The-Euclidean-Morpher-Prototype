import tkinter as tk
from tkinter import font
from tkinter import filedialog

import controller as ctr
from seq import euc


class GUI:
    def __init__(self):
        self.controller = ctr.Controller(self)
        self.root = tk.Tk()
        self.root.geometry('525x400')
        self.root.title('Euclidean Morpher Prototype')
        self.root.configure(background='gray77')

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=14)

        # Morpher variables
        self.onsets = tk.IntVar()
        self.length = tk.IntVar()
        self.length.set(16)
        self.rotation = tk.IntVar()
        self.amount = tk.IntVar()

        self.euc = tk.StringVar()
        temp = euc(self.onsets.get(), self.length.get(), self.rotation.get())
        temp = ''.join(str(x) for x in temp)
        self.euc.set(temp)

        # Sequencer variables
        self.sequence = tk.StringVar()
        self.sequence.set('1000100010001000')
        self.tempo = tk.IntVar()
        self.tempo.set(120)
        self.subdivisions = tk.IntVar()
        self.subdivisions.set(4)
        self.note = tk.IntVar()
        self.note.set(48)

        # Generator variables
        self.num_bars = tk.IntVar()
        self.num_bars.set(1)
        self.morpher = tk.StringVar()
        self.morpher_options = list(self.controller.morphers.keys())
        self.morpher.set(self.morpher_options[0])

        # Debug/print things
        self.log_option = tk.StringVar()
        self.log_options = (
            "off",
            "print rhythm",
            "print all"
        )
        self.log_option.set(self.log_options[1])

        self.add_morpher()
        self.add_euc()
        self.add_sequencer()
        self.add_options()
        self.add_filechooser()
        self.add_generator()

        # TODO: Extra stuff like "restart" or "clear" and info, credit and stuff

    def add_morpher(self):
        # MORPHER FRAME
        mframe = tk.Frame(self.root, bd=3, bg='pink1')
        mframe.pack(side=tk.TOP, anchor=tk.E)
        tk.Label(mframe, text='MORPHER', bd=5, relief=tk.SUNKEN).grid(row=0, column=0, rowspan=2, sticky='news')

        tk.Label(mframe, text='onsets', width=6, anchor='e').grid(row=0, column=2)
        onsetbox = tk.Spinbox(mframe, from_=0, to=100, width=3,
                              textvariable=self.onsets, font=self.default_font, command=self.update_morpher)
        onsetbox.grid(row=0, column=3, sticky='news')

        tk.Label(mframe, text='length', width=6, anchor='e').grid(row=0, column=4)
        lengthbox = tk.Spinbox(mframe, from_=0, to=32, width=3,
                               textvariable=self.length, font=self.default_font, command=self.update_morpher)
        lengthbox.grid(row=0, column=5, sticky='news')

        tk.Label(mframe, text='rotation', width=6, anchor='e').grid(row=0, column=6)
        rotationbox = tk.Spinbox(mframe, from_=0, to=100, width=3,
                                 textvariable=self.rotation, font=self.default_font, command=self.update_morpher)
        rotationbox.grid(row=0, column=7, sticky='news')

        tk.Label(mframe, text='morph', width=6, anchor='se').grid(row=1, column=1, sticky='news', columnspan=2)
        amountscale = tk.Scale(mframe, from_=0, to=100, width=8, orient=tk.HORIZONTAL, variable=self.amount)
        amountscale.grid(row=1, column=3, sticky='news', columnspan=5)

    def update_morpher(self):
        if self.rotation.get() > (self.length.get() - 1):
            self.rotation.set(self.length.get() - 1)
        if self.onsets.get() > self.length.get():
            self.onsets.set(self.length.get())
        temp = euc(self.onsets.get(), self.length.get(), self.rotation.get())
        temp = ''.join(str(x) for x in temp)
        self.euc.set(temp)

    def add_euc(self):
        eucframe = tk.Frame(self.root, bd=3, bg='pink1')
        eucframe.pack(side=tk.TOP, anchor=tk.E)
        tk.Label(eucframe, text='EUCLIDEAN', bd=3, relief=tk.SUNKEN).pack(side=tk.LEFT)
        tk.Entry(eucframe, width=32, font=('Arial', 16), fg='gray26', textvariable=self.euc, state='readonly').pack(side=tk.RIGHT)

    def add_sequencer(self):
        # SEQUENCER FRAME
        seqframe = tk.Frame(self.root, bd=3, bg='skyblue1')
        seqframe.pack(side=tk.TOP, anchor=tk.E)
        (tk.Label(seqframe, text='SEQUENCER', bd=5, relief=tk.SUNKEN)
         .grid(row=0, column=0, rowspan=2, sticky='news'))

        seqentry = tk.Entry(seqframe, width=32, font=('Arial', 16), textvariable=self.sequence)
        seqentry.grid(row=0, column=1, sticky='w', columnspan=20)

        tk.Label(seqframe, text='tempo', width=6, anchor='e').grid(row=1, column=1, sticky='news')
        tempobox = tk.Spinbox(seqframe, from_=30, to=300, width=3,
                              textvariable=self.tempo, font=self.default_font)
        tempobox.grid(row=1, column=2, sticky='news')

        tk.Label(seqframe, text='subdivisions', width=10, anchor='e').grid(row=1, column=3, sticky='news')
        subdivisionsbox = tk.Spinbox(seqframe, from_=1, to=6, width=1,
                                     textvariable=self.subdivisions, font=self.default_font)
        subdivisionsbox.grid(row=1, column=4, sticky='news')

        tk.Label(seqframe, text="note", width=4, anchor='e').grid(row=1, column=5, sticky='news')
        notebox = tk.Spinbox(seqframe, from_=36, to=56, width=2,
                             textvariable=self.note, font=self.default_font)
        notebox.grid(row=1, column=6, sticky='news')

        tk.Label(seqframe, text='').grid(row=1, column=7, sticky='news', columnspan=20)

    def add_options(self):
        optionsframe = tk.Frame(self.root, bd=3, bg='seagreen')
        optionsframe.pack(side=tk.TOP, anchor=tk.E)
        tk.Label(optionsframe, text='OPTIONS', font=("TkDefaultFont", 8), bd=5, relief=tk.SUNKEN).grid(row=0, column=0, rowspan=2, sticky='news')

        tk.Label(optionsframe, text='morpher:', font=("TkDefaultFont", 8), width=7, anchor='e').grid(row=0, column=3, sticky='news', rowspan=2)
        mselect = tk.OptionMenu(optionsframe, self.morpher, *self.morpher_options)
        mselect.grid(row=0, column=4, sticky='news', rowspan=2)
        mselect.configure(font=("TkDefaultFont", 8))

        tk.Label(optionsframe, text='print', font=("TkDefaultFont", 8), width=5, anchor='e').grid(row=0, column=5, sticky='news', rowspan=2)
        printselect = tk.OptionMenu(optionsframe, self.log_option, *self.log_options)
        printselect.grid(row=0, column=6, sticky='news', rowspan=2)
        printselect.configure(font=("TkDefaultFont", 8))

    def add_generator(self):
        generatorframe = tk.Frame(self.root, bd=3, bg='green2')
        generatorframe.pack(side=tk.BOTTOM)
        (tk.Button(generatorframe, text='-GENERATE-', bd=5, command=self.generate)
         .grid(row=0, column=0, rowspan=2, sticky='news'))

        tk.Label(generatorframe, text='bars', width=4, anchor='e').grid(row=0, column=1, sticky='news', rowspan=2)
        numbarsbox = tk.Spinbox(generatorframe, from_=0, to=8, width=2,
                                textvariable=self.num_bars, font=self.default_font)
        numbarsbox.grid(row=0, column=2, sticky='news', rowspan=2)

    def generate(self):
        self.controller.handle_generate()
        if self.num_bars.get() == 0:
            info = "Generated HYPERPERIOD of bars!"
        else:
            info = "Generated " + str(self.num_bars.get()) + " bars!"
        infolabel = tk.Label(self.root, text=info)
        infolabel.pack(side=tk.TOP)
        infolabel.after(2000, lambda: infolabel.destroy())

    def add_filechooser(self):
        fcframe = tk.Frame(self.root, bd=3, bg='gold2')
        fcframe.pack(side=tk.BOTTOM)
        tk.Button(fcframe, text='-SAVE MIDI FILE-', bd=5, command=self.save_file).grid(row=0, column=0, sticky='news')
        tk.Button(fcframe, text='-CLEAR MIDI FILE-', bd=5, command=self.clear_file).grid(row=0, column=1, sticky='news')

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension='.mid', filetypes=[('.mid', '*.mid')])
        if path:
            self.controller.handle_save(path)
            infolabel = tk.Label(self.root, text="Saved and cleared MIDI")
            infolabel.pack(side=tk.TOP)
            infolabel.after(2000, lambda: infolabel.destroy())

    def clear_file(self):
        self.controller.handle_clear()
        infolabel = tk.Label(self.root, text='Cleared MIDI file')
        infolabel.pack(side=tk.TOP)
        infolabel.after(2000, lambda: infolabel.destroy())

    def run(self):
        self.root.mainloop()
