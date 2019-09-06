import cseqGui
import cseqGui_support
import tkFileDialog
import os
import VerticalScrolledFrame
from re import search

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

'''
Da questa classe e' sono accessibili tutti gli elementi della classe in cseqGui
per accedervi ci sono due attributi (top e w)
top: istanza della classe Toplevel1 
w: istanza della classe tk.Toplevel

ci sono alcune cose da sistemare (leggere TODO), inoltre quando si avvia control.py
si apre anche un altra finestra piu piccola, ignoratela per il momento.


Altri Task (oltre ai TODO):

    -Definizione valori di Default dei parametri (va fatto in cseqGui_support.py impostando tutti i value) [FATTO]

    -Definizione metodo che disabilita tutte le opzioni riguardanti CBMC 
        (No Simplify, Refine Arrays, show Countrexample, etc.) 
        quando viene selezionato un altro model-checker nei radiobutton

    -Definizione metodo per Apertura finestra di dialogo per salvataggio 
        file quando si clicca sulle checkbox 'show Countrexample trace' [FATTO]

'''

class state():

    #color_set = dict() #TODO: controllare se serve color_set
    global_var = set()

    current_state = 0

    def __init__(self, id, thread, istruction, filepath=None, line=None):
        self.id = id
        self.thread = thread
        self.istruction = istruction
        self.filepath = filepath
        self.line = line
        self.thread_set = dict()


class RunCseq():
    win_list = {}

    def __init__(self):
        self.cmd = []
        self.states = list()
        (self.w, self.top) = self.vp_start_gui()#self.create_root_window(None)

        # Button1 -> Browse File -> OpenFileDialog
        self.top.Button1.configure(command=lambda: self.open_file())
        # Checkbutton2 -> Get Path to save Trace
        #self.top.Checkbutton2.configure(command=lambda: self.save_file(self.top.Entry2, "trace"))

        self.focus_radio(cseqGui_support.rb_bd_md_chk.get())
        self.top.Radiobutton1.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.top.Radiobutton1_8.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.top.Radiobutton1_9.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.top.Radiobutton1_10.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.top.Radiobutton1_11.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.top.Radiobutton1_12.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.top.Radiobutton1_13.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.top.Radiobutton1_14.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.top.Radiobutton1_15.configure(command=lambda: self.focus_radio(cseqGui_support.rb_bd_md_chk.get()))
        self.check_robin(cseqGui_support.cb_robin.get())
        self.top.Checkbutton4_13.configure(command=lambda: self.check_robin(cseqGui_support.cb_robin.get()))
        self.check_show_counterexample(cseqGui_support.cb_countre_ex.get())
        self.top.Checkbutton2.configure(
            command=lambda: self.check_show_counterexample(cseqGui_support.cb_countre_ex.get()))
        # Default value for Error Label (ERROR)
        self.top.Entry1.insert(0, "ERROR")
        # Default value for Config Label
        try:
            conf = open("config.cfg", "r")
            lines = (conf.read()).split('\n')
        except:
            print "ERROR: config.cfg missing!\n"
            exit(-1)

        self.default_conf = lines[0][9:-1] #"lazy"
        self.global_path = lines[1][17:-1]# os.getcwd()  # "/home/qwerty/cseq/lazy-cseq-2.0/cseq-feeder.py"

        # top.Entry2_8.configure(command=lambda: self.save_file(top.Entry2_8, "txt"))
        self.top.Button2.configure(command=lambda: self.lunch())
        # MenuBar
        self.top.sub_menu.entryconfig(0, command=lambda: self.open_file())
        self.top.sub_menu1.entryconfig(0, command=lambda: self.showInfo())
        self.top.sub_menu1.entryconfig(1, command=lambda: self.show_config())
        self.top.sub_menu1.entryconfig(2, command=lambda: self.showSettings())
        #self.load_countrexample(None)
        #self.save_visual_Trace()
        #self.load_visual_Trace()
        # self.drwawTrace()
        self.w.mainloop()

    def vp_start_gui(self):
        '''Starting point when module is the main routine.'''
        global val, w, root
        root = tk.Tk()
        cseqGui_support.set_Tk_var()
        top = cseqGui.Toplevel1(root)
        cseqGui_support.init(root, top)
        return (root, top)


    def check_robin(self, var):
        if var == 1:
            self.top.Label6_12.configure(state=tk.NORMAL)
            self.top.Spinbox1_15.configure(state=tk.NORMAL)
        else:
            self.top.Label6_12.configure(state=tk.DISABLED)
            self.top.Spinbox1_15.configure(state=tk.DISABLED)

    def check_show_counterexample(self, var):

        if var == 1:
            self.top.Checkbutton6.configure(state=tk.NORMAL)
            self.top.Label3.configure(state=tk.NORMAL)
            self.top.Entry2.configure(state=tk.NORMAL)
            self.chose_trace_path(self.top.Entry2, "trace")
        else:
            self.top.Checkbutton6.configure(state=tk.DISABLED)
            self.top.Label3.configure(state=tk.DISABLED)
            self.top.Entry2.configure(state=tk.DISABLED)

    def focus_radio(self, var):
        if var == 0:
            self.top.Checkbutton3.configure(state=tk.NORMAL)
            self.top.Checkbutton3_17.configure(state=tk.NORMAL)
            self.top.Label5.configure(state=tk.NORMAL)
            self.top.Checkbutton2.configure(state=tk.NORMAL)
            self.top.Entry2.configure(state=tk.NORMAL)
            self.top.Checkbutton6.configure(state=tk.NORMAL)
            self.top.Label8.configure(state=tk.DISABLED)
            self.top.Entry4.configure(state=tk.DISABLED)
            self.top.Entry3.configure(state=tk.NORMAL)
            self.top.Label3.configure(state=tk.NORMAL)
            self.top.Label7_16.configure(state=tk.DISABLED)
            self.top.Spinbox2_17.configure(state=tk.DISABLED)
            self.check_show_counterexample(cseqGui_support.cb_countre_ex.get())


        elif var == 1:
            self.top.Checkbutton3.configure(state=tk.DISABLED)
            self.top.Checkbutton3_17.configure(state=tk.DISABLED)
            self.top.Label5.configure(state=tk.DISABLED)
            self.top.Checkbutton2.configure(state=tk.DISABLED)
            self.top.Label3.configure(state=tk.DISABLED)
            self.top.Entry2.configure(state=tk.DISABLED)
            self.top.Checkbutton6.configure(state=tk.DISABLED)
            self.top.Label8.configure(state=tk.DISABLED)
            self.top.Entry4.configure(state=tk.DISABLED)
            self.top.Entry3.configure(state=tk.DISABLED)
            self.top.Label7_16.configure(state=tk.DISABLED)
            self.top.Spinbox2_17.configure(state=tk.DISABLED)

        elif var == 2:
            self.top.Checkbutton3.configure(state=tk.DISABLED)
            self.top.Checkbutton3_17.configure(state=tk.DISABLED)
            self.top.Label5.configure(state=tk.DISABLED)
            self.top.Checkbutton2.configure(state=tk.DISABLED)
            self.top.Label3.configure(state=tk.DISABLED)
            self.top.Entry2.configure(state=tk.DISABLED)
            self.top.Checkbutton6.configure(state=tk.DISABLED)
            self.top.Label8.configure(state=tk.DISABLED)
            self.top.Entry4.configure(state=tk.DISABLED)
            self.top.Entry3.configure(state=tk.DISABLED)
            self.top.Label7_16.configure(state=tk.DISABLED)
            self.top.Spinbox2_17.configure(state=tk.DISABLED)

        elif var == 3:
            self.top.Checkbutton3.configure(state=tk.DISABLED)
            self.top.Checkbutton3_17.configure(state=tk.DISABLED)
            self.top.Label5.configure(state=tk.DISABLED)
            self.top.Checkbutton2.configure(state=tk.DISABLED)
            self.top.Label3.configure(state=tk.DISABLED)
            self.top.Entry2.configure(state=tk.DISABLED)
            self.top.Checkbutton6.configure(state=tk.DISABLED)
            self.top.Label8.configure(state=tk.NORMAL)
            self.top.Entry3.configure(state=tk.DISABLED)
            self.top.Entry4.configure(state=tk.NORMAL)
            self.top.Label7_16.configure(state=tk.DISABLED)
            self.top.Spinbox2_17.configure(state=tk.DISABLED)

        elif var == 4:
            self.top.Checkbutton3.configure(state=tk.DISABLED)
            self.top.Checkbutton3_17.configure(state=tk.DISABLED)
            self.top.Label5.configure(state=tk.DISABLED)
            self.top.Checkbutton2.configure(state=tk.DISABLED)
            self.top.Label3.configure(state=tk.DISABLED)
            self.top.Entry2.configure(state=tk.DISABLED)
            self.top.Checkbutton6.configure(state=tk.DISABLED)
            self.top.Label8.configure(state=tk.DISABLED)
            self.top.Entry4.configure(state=tk.DISABLED)
            self.top.Entry3.configure(state=tk.DISABLED)
            self.top.Label7_16.configure(state=tk.DISABLED)
            self.top.Spinbox2_17.configure(state=tk.DISABLED)

        elif (var == 5 or var == 6 or var == 8):
            self.top.Checkbutton3.configure(state=tk.DISABLED)
            self.top.Checkbutton3_17.configure(state=tk.DISABLED)
            self.top.Label5.configure(state=tk.DISABLED)
            self.top.Checkbutton2.configure(state=tk.DISABLED)
            self.top.Label3.configure(state=tk.DISABLED)
            self.top.Entry2.configure(state=tk.DISABLED)
            self.top.Checkbutton6.configure(state=tk.DISABLED)
            self.top.Label8.configure(state=tk.DISABLED)
            self.top.Entry4.configure(state=tk.DISABLED)
            self.top.Entry3.configure(state=tk.DISABLED)
            self.top.Label7_16.configure(state=tk.DISABLED)
            self.top.Spinbox2_17.configure(state=tk.DISABLED)

        elif (var == 7):
            self.top.Checkbutton3.configure(state=tk.DISABLED)
            self.top.Checkbutton3_17.configure(state=tk.DISABLED)
            self.top.Label5.configure(state=tk.DISABLED)
            self.top.Checkbutton2.configure(state=tk.DISABLED)
            self.top.Label3.configure(state=tk.DISABLED)
            self.top.Entry2.configure(state=tk.DISABLED)
            self.top.Checkbutton6.configure(state=tk.DISABLED)
            self.top.Label8.configure(state=tk.DISABLED)
            self.top.Entry4.configure(state=tk.DISABLED)
            self.top.Entry3.configure(state=tk.DISABLED)
            self.top.Label7_16.configure(state=tk.NORMAL)
            self.top.Spinbox2_17.configure(state=tk.NORMAL)

    def check_Textbox(self, textBox_1, textBox_2):
        self.cmd.append("--output")

        if textBox_2.get() != "":
            self.cmd.append(textBox_2.get())
        else:
            file_name = self.build_file_name(textBox_1.get())
            self.cmd.append(file_name)

    def build_file_name(self, name):
        list = name.split('/')
        list[-1] = "seq_" + list[-1]
        i = 1
        file_name = list[0]
        while i < len(list):
            file_name = file_name + "/" + list[i]
            i = i + 1
        return file_name

    def open_dir(self, entry):
        path = tkFileDialog.askdirectory() + "/"
        entry.delete(0, tk.END)
        entry.update()
        entry.insert(0, path)

    def open_file(self):
        path = str(tkFileDialog.askopenfilename(initialdir=str(os.getcwd()), title="Select file",
                                            filetypes=(("c source files", "*.c"), ("visual trace files", "*.vtrace"), ("all files", "*.*"))))
        if path.endswith(".vtrace"):
            self.load_visual_Trace(path)

        elif path.endswith(".c"):
            self.top.Text2.delete(0, tk.END)
            self.top.Text2.update()
            self.top.Text2.insert(0, path)

    def chose_trace_path(self, entry, type):
        path = str(tkFileDialog.asksaveasfilename(initialdir=os.getcwd(), title="Chose trace path",
                                              filetypes=((type + " files", "*." + type), ("all files", "*.*"))))
        if path.endswith(".trace"):
            entry.delete(0, tk.END)
            entry.update()
            entry.insert(0, path)
        elif path != "":
            entry.delete(0, tk.END)
            entry.update()
            entry.insert(0, path+".trace")

    def lunch(self):

        for win in self.win_list.values():
            try:
                win.destroy()
            except:
                pass

        self.check_Textbox(self.top.Text2, self.top.Entry2_8)
        self.checkEntry()
        self.checkCheckbox()
        self.checkSpinbox()
        self.check_setting()
        output = self.run(self.cmd)

        l = search('UNSAFE', output)
        if l is not None:

            # SALVO TRACCIA SU FILE DI TESTO
            if cseqGui_support.cb_countre_ex.get():
                if self.top.Entry2.get() != "":
                    file = open(self.top.Entry2.get(), 'w')
                else:
                    file = open('traccia.trace', 'w')

                file.write(output)
                file.close()

            self.showTrace(output)
            if cseqGui_support.cb_countre_ex_trace.get():
                self.load_countrexample(output)

            self.top.Labe_res.configure(text="VERIFICATION FAILED: UNSAFE\n"+l.group(0))

        elif search('SAFE', output) is not None:
            self.top.Labe_res.configure(text="VERIFICATION SUCCESSFULLY: SAFE")

        else:
            self.top.Labe_res.configure(text="UNEXPECTED OUTPUT\nControl Terminal output")

        print "\n\n----------------------- ***** OUTPUT ***** -------------------------------\n"
        print "\n\n" + output
        print "\n\n--------------------------------------------------------------------------\n"

    def run(self, argument):
        import subprocess

        os.chdir(self.global_path)

        cmd = ["python", self.global_path+"cseq-feeder.py"] + argument

        try:
            print "CMD: " + str(cmd)
            # print "GLOBAL PATH: " + str(self.global_path)
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print str(e.output)
            print "RETURN CODE: " + str(e.returncode)
            exit()

        return output

    def getSymTable(self):
        import subprocess

        cmd = ["cbmc", str(self.top.Text2.get()), "--show-symbol-table"]

        try:
            # print "CMD: " + str(cmd)
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except subprocess.CalledProcessError as e:
            print str(e.output)
            print "RETURN CODE: " + str(e.returncode)
            exit()

    #Visualizza la traccia testuale su una finestra
    def showTrace(self, output):

        self.win_list["Textual Trace"] = tk.Tk()
        self.win_list["Textual Trace"].wm_title("Textual Trace")
        self.win_list["Textual Trace"].frame = VerticalScrolledFrame.VerticalScrolledFrame(self.win_list["Textual Trace"])
        self.win_list["Textual Trace"].frame.pack(fill=tk.BOTH, expand=1)

        sep = ttk.Separator(self.win_list["Textual Trace"], orient="horizontal")
        sep.pack(fill=tk.X, padx=5, pady=2)

        b = ttk.Button(self.win_list["Textual Trace"], text="Close", command=self.win_list["Textual Trace"].destroy)
        b.pack(side=tk.RIGHT, padx=5, pady=5)

        text = tk.Label(self.win_list["Textual Trace"].frame.interior)
        text.grid(row=0, column=0)
        text.configure(width=100, justify=tk.LEFT, anchor=tk.NW, text=output)

    def showInfo(self):
        win = tk.Toplevel()
        win.wm_title("Info")

        l = tk.Label(win, text=self.run(["-h"]))
        l.grid(row=0, column=0)

        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=1, column=0)

    def close_win(self, path, conf, win):
        if path != self.global_path:
            self.global_path = path

        if conf != self.default_conf:
            self.default_conf = conf

        win.destroy()

    def showSettings(self):
        win = tk.Toplevel()
        win.wm_title("Settings")
        win.geometry("+100+30")

        Label = tk.Label(win, text="Global Path")
        Label.grid(row=0, column=0)

        Label1 = tk.Label(win, text="Config file")
        Label1.grid(row=2, column=0)

        Entry_Global = tk.Entry(win)
        Entry_Global.place(relx=0.364, rely=0.162, height=23, relwidth=0.503, bordermode='ignore')
        Entry_Global.configure(background="white")
        Entry_Global.configure(font="TkFixedFont")
        Entry_Global.configure(selectbackground="#c4c4c4")
        Entry_Global.grid(row=0, column=1)
        Entry_Global.insert(0, self.global_path)

        Entry_Config = tk.Entry(win)
        Entry_Config.place(relx=0.364, rely=0.162, height=23, width=900, relwidth=0.503, bordermode='ignore')
        Entry_Config.configure(background="white")
        Entry_Config.configure(font="TkFixedFont")
        Entry_Config.configure(selectbackground="#c4c4c4")
        Entry_Config.grid(row=2, column=1)
        Entry_Config.insert(0, self.default_conf)

        Button_browse = tk.Button(win)
        Button_browse.place(relx=0.453, rely=0.943, height=29, width=331)
        Button_browse.configure(activebackground="#d9d9d9")
        Button_browse.configure(text='''Browse''')
        Button_browse.grid(row=0, column=2)
        Button_browse.configure(command=lambda: self.open_dir(Entry_Global))


        Button_save = tk.Button(win)
        Button_save.place(relx=0.453, rely=0.943, height=29, width=331)
        Button_save.configure(activebackground="#d9d9d9")
        Button_save.configure(text='''Save''')
        Button_save.grid(row=3, column=3)
        Button_save.configure(command=lambda: self.close_win(Entry_Global.get(), Entry_Config.get(), win))

    def show_config(self):
        win = tk.Toplevel()
        win.wm_title("config")

        l = tk.Label(win, text=self.run(["-L"]))
        l.grid(row=0, column=0)

        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=1, column=0)

    def checkSpinbox(self):
        ''' TODO: Aggiungere nella condizione degli 'if' il confronto con il valore di default dei parametri
                per capire se quella spinbox e' stata settata o meno (altrimenti il parametro non
                va proprio inserito)
        '''
        if cseqGui_support.sb_unwind.get() != 1:
            self.cmd.append("--unwind")
            self.cmd.append(str(cseqGui_support.sb_unwind.get()))
        if cseqGui_support.sb_unwind_while.get() != 0:
            self.cmd.append("--unwind-while")
            self.cmd.append(str(cseqGui_support.sb_unwind_while.get()))
        if cseqGui_support.sb_unwind_for.get() != 0:
            self.cmd.append("--round-for")
            self.cmd.append(str(cseqGui_support.sb_unwind_for.get()))
        if cseqGui_support.sb_unwind_for_max.get() != 0:
            self.cmd.append("--unwind-for-max")
            self.cmd.append(str(cseqGui_support.sb_unwind_for_max.get()))
        if cseqGui_support.cb_robin.get() == 1:
            if cseqGui_support.sb_rounds.get() != 1:
                self.cmd.append("--rounds")
                self.cmd.append(str(cseqGui_support.sb_rounds.get()))
        if cseqGui_support.sb_lim_ser_depth.get() != 0:
            self.cmd.append("--depth")
            self.cmd.append(str(cseqGui_support.sb_lim_ser_depth.get()))
        if cseqGui_support.sb_sem_lev.get() != 1:
            self.cmd.append("--slevel")
            self.cmd.append(str(cseqGui_support.sb_sem_lev.get()))
        if cseqGui_support.sb_Time.get() != 86400:
            self.cmd.append("--time")
            self.cmd.append(str(cseqGui_support.sb_Time.get()))

    def checkCheckbox(self):
        # TODO: mancano alcune stringhe!!
        if cseqGui_support.cb_keep_stat.get():
            self.cmd.append('--keepstaticarray')
        if cseqGui_support.cb_atom_param.get():
            self.cmd.append('--atomicparameter')
        if cseqGui_support.cb_dec_pc.get():
            self.cmd.append('--decomposepc')
        if cseqGui_support.cb_guess_cs.get():
            self.cmd.append('--guess-cs-only')
        if cseqGui_support.cb_svcomp.get():
            self.cmd.append('--svcomp')
        if cseqGui_support.cb_round_int.get():
            self.cmd.append('--roundint')
        if cseqGui_support.cb_bit_pthr.get():
            self.cmd.append('--bit-pthread')
        if cseqGui_support.cb_nondet_stat.get():
            self.cmd.append('--nondet-static')
        if cseqGui_support.cb_stop_fail.get():
            self.cmd.append('--stop-on-fail')
        if cseqGui_support.cb_show_linem.get():
            self.cmd.append('--linemap')
        if cseqGui_support.cb_deadlock.get():
            self.cmd.append('--deadlock')
        if cseqGui_support.cb_bounds.get():
            self.cmd.append('--bounds-check')
        if cseqGui_support.cb_div_zero.get():
            self.cmd.append('--div-by-zero-check')
        if cseqGui_support.cb_pointer.get():
            self.cmd.append('--pointer-check')
        if cseqGui_support.cb_mem_leak.get():
            self.cmd.append('--memory-leak-check')
        if cseqGui_support.cb_sign_overfl.get():
            self.cmd.append('--signed-overflow-check')
        if cseqGui_support.cb_un_overfl.get():
            self.cmd.append('--unsigned-overflow-check')
        if cseqGui_support.cb_nan.get():
            self.cmd.append('--nan-check')
        if cseqGui_support.cb_overfl.get():
            self.cmd.append('--overflow-check')
        if cseqGui_support.cb_float_overfl.get():
            self.cmd.append('--float-overflow-check')
        if cseqGui_support.cb_sof_unwind.get():
            self.cmd.append('--softunwindbound')
        if cseqGui_support.cb_robin.get():
            self.cmd.append('--robin')
        if cseqGui_support.cb_no_chek_var_pointer.get():
            self.cmd.append('--donotcheckvisiblepointer')
        if cseqGui_support.rb_bd_md_chk.get() == 0:  # CBMC
            # if :
            #    self.cmd.append('')
            if cseqGui_support.cb_countre_ex.get():
                self.cmd.append('--cex')
            if cseqGui_support.cb_no_simpl.get():
                self.cmd.append('--no-simplify')
            if cseqGui_support.cb_ref_arr.get():
                self.cmd.append('--refine-arrays')

    def checkEntry(self):
        if cseqGui_support.rb_bd_md_chk.get() == 0:  # CBMC
            if self.top.Entry3.get() != "":
                self.cmd.append('--path-backend')
                self.cmd.append(self.top.Entry3.get())
        if (self.top.Entry1.get() != "ERROR" and self.top.Entry1.get() != ""):
            self.cmd.append('--error-label')
            self.cmd.append(self.top.Entry1.get())
        if cseqGui_support.rb_bd_md_chk.get() == 3:
            if self.top.Entry4.get() != "":
                print(self.top.Entry4.get())
                self.cmd.append('--llvm')
                self.cmd.append(self.top.Entry4.get())
        if (self.top.Text2.get() != '' and self.top.Entry2_8.get() == ''):
            file_name = self.build_file_name(self.top.Text2.get())
            self.top.Entry2_8.insert(0, file_name)

        if self.top.Text2.get() != "":
            self.cmd.append("-i")
            self.cmd.append(self.top.Text2.get())

    def check_setting(self):
        if self.default_conf != "lazy":
            self.cmd.append('-l')
            self.cmd.append(self.default_conf)

    def load_countrexample(self, my_trace):
        # DEBUG: ELIMINARE QUESTE RIGHE
        #my_trace = cseqGui_support.trace.read()

        #sym_table_file = open("mysymbletable.txt",'r')
        sym_table = self.getSymTable()#sym_table_file.read()

        ####################################
        print "----------------------"
        print "TRACE: " + my_trace
        print "----------------------"
        lines = my_trace.split('\n')
        k = my_trace[:my_trace.find('Counterexample:')].count('\n') + 1 + 1
        separator = ["----------------------------------------------------",
                     "- - - - - - - - - - - - - - - - - - - - - - - - - - "]

        while k < len(lines):
            if lines[k].startswith('State ') and (lines[k + 1] == separator[0] or
                                                  lines[k + 1] == separator[1]):
                A, C = lines[k], lines[k + 2]
                k += 4

                var = search('[A-Za-z_][A-Za-z0-9_]*=', C) #TODO: puo esserci lo spazio prima dell uguale?

                if var is not None:
                    #aggiungi SE presente in symbolTable
                    regex = "Symbol......: "+var.group(0)[:-1]
                    var_glob = search(regex, sym_table)
                    if var_glob is not None:
                        self.states[0].global_var.add(var.group(0)[:-1])

                id = search('[0-9]+', A)
                thread = search('thread [0-9]+', A)
                if thread is None: thread = search('thread [0-9]+', C)

                filepath = search('file (.)+ line', A)

                line = search('line [0-9]+', A)

                if filepath is not None:
                    self.states.append(
                        state(id.group(0), thread.group(0), C, filepath.group(0)[5:-5], int(line.group(0)[5:])))
                else:
                    self.states.append(state(id.group(0), thread.group(0), C))

                # Aggiungo nome del thread al set 'thread set' (statico -> uguale per tutti gli state della lista)
                color = self.random_color()
                self.states[0].thread_set[thread.group(0)] = color
                #self.states[0].color_set[thread.group(0)] = [color, 0]

            else:
                k += 1

        self.createWindowTrace("Trace Window", len(self.states[0].thread_set))
        self.drwawTrace(self.states, self.win_list["Trace Window"].frame.interior)
        print "VARIABILI GLOBALI: "
        print self.states[0].global_var

    def createWindowTrace(self, title, n):

        width = str(n * 200 + 50)
        # print "WIIDTH " + str(width)
        # print "LEN " + str(len(self.states[0].thread_set))
        self.win_list[title] = tk.Tk()
        self.win_list[title].wm_title(title)
        self.win_list[title].geometry(width+"x650+20+10")

        f = tk.Frame(self.win_list[title])
        f.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=2)

        l = tk.Label(f)
        text = "Shared Variable:    "
        for x in self.states[0].global_var:
            text += x + "   "
        l.configure(text=text, relief=tk.RIDGE)
        l.pack(side=tk.TOP, anchor=tk.NW)

        sep = ttk.Separator(self.win_list[title], orient="horizontal")
        sep.pack(fill=tk.X, padx=5, pady=2)

        self.win_list[title].frame = VerticalScrolledFrame.VerticalScrolledFrame(self.win_list[title])
        self.win_list[title].frame.pack(fill=tk.BOTH, expand=1)

        sep2 = ttk.Separator(self.win_list[title], orient="horizontal")
        sep2.pack(fill=tk.X, padx=5, pady=2)

        b = ttk.Button(self.win_list[title], text="Exit", command=self.win_list[title].destroy)
        b.pack(side=tk.RIGHT, padx=5, pady=5)

        b = ttk.Button(self.win_list[title], text="Save", command=lambda: self.save_visual_Trace())

        b.pack(side=tk.RIGHT, padx=5, pady=5)

        b = ttk.Button(self.win_list[title], text="Restart", command=lambda: self.resetTrace(title))
        b.pack(side=tk.LEFT, padx=5, pady=5)

        b = ttk.Button(self.win_list[title], text="Previus", command=lambda: self.PrintPreviusState(title))
        b.pack(side=tk.LEFT, padx=5, pady=5)

        b = ttk.Button(self.win_list[title], text="Next", command=lambda: self.PrintNextState(title))
        b.pack(side=tk.LEFT, padx=5, pady=5)

        l = tk.Label(self.win_list[title])
        l.configure(text="|  Next For: ")
        l.pack(side=tk.LEFT, padx=5, pady=5)

        OPTIONS = [
            "Istruction",
            "Context Switch",
            "Round"
        ]

        self.step_mode = tk.StringVar(self.win_list[title])
        self.step_mode.set(OPTIONS[0])  # default value
        #variable.trace("w", self.PrintNextState())

        w = apply(tk.OptionMenu, (self.win_list[title], self.step_mode) + tuple(OPTIONS))
        w.pack(side=tk.LEFT, padx=5, pady=5)

    def createWindowCode(self, path):

        self.win_list[path] = tk.Tk()
        self.win_list[path].wm_title(path)
        self.win_list[path].geometry("520x650+10+600")

        self.win_list[path].frame = VerticalScrolledFrame.VerticalScrolledFrame(self.win_list[path])
        self.win_list[path].frame.pack(fill=tk.BOTH, expand=1)

        sep = ttk.Separator(self.win_list[path], orient="horizontal")
        sep.pack(fill=tk.X, padx=5, pady=2)

        b = ttk.Button(self.win_list[path], text="Exit", command=self.win_list[path].destroy)
        b.pack(side=tk.RIGHT, padx=5, pady=5)

        source = open(path, "r")
        lines = (source.read()).split('\n')
        i = 0
        for line in lines:
            text = tk.Label(self.win_list[path].frame.interior)
            text.grid(row=i, column=0)
            if i % 2 == 0: text.configure(bg="#D3D3D3")
            text.configure(width=100, justify=tk.LEFT, anchor=tk.NW, text=str(i + 1) + "|\t" + line)
            i = i + 1

    def drwawTrace(self, states, win):

        col_thread = list()
        col_thread.append(tk.LabelFrame(win))
        col_thread[0].grid(row=0, column=0, sticky="N")

        col_thread[0].configure(relief='groove')
        col_thread[0].configure(text="State")

        i = 1
        for thread_name, color in states[0].thread_set.items():
            col_thread.append(tk.LabelFrame(win))
            col_thread[i].grid(row=0, column=i, sticky="N")
            col_thread[i].configure(relief='groove')
            col_thread[i].configure(text=thread_name, bg = color)
            i += 1

        self.printStates(states, win)
        '''
        for col in col_thread:
            column, row = col.grid_size()
            col.grid_columnconfigure(0, minsize=row)
            print "colum: " + str(col) + "  row: " + str(row)'''

    def printStates(self, states, win):

        i =self.states[0].current_state
        #win = self.win_list[win].frame.interior
        col_thread = list()

        for labelFrame in win.winfo_children():
            col_thread.append(labelFrame)

        for state in states:
            # Aggiungo numero stato in colonna State
            current_state_label = tk.Label(col_thread[0])
            current_state_label.grid(row=i, column=0)
            current_state_label.configure(text=state.id)

            col = search('[0-9]+', state.thread)
            col = int(col.group())

            current_istruction_label = list()
            for j in range(len(self.states[0].thread_set)):
                current_istruction_label.append(tk.Label(col_thread[j + 1]))
                current_istruction_label[j].grid(row=i, column=0)
                current_istruction_label[j].configure(bg=self.states[0].thread_set[self.states[0].thread_set.keys()[j]])

            if state.istruction.endswith("scheduled"):
                current_istruction_label[col].configure(fg='#ff0000')

            var = search('[A-Za-z_][A-Za-z0-9_]*=', state.istruction)
            if var is not None:
                if var.group(0)[:-1] in self.states[0].global_var:
                    current_istruction_label[col].configure(fg='#ff0000', relief=tk.RIDGE)


            current_istruction_label[col].configure(text=state.istruction)

            if state.filepath is not None:
                '''print "FILE: " + state.filepath
                print "LINE: "
                print state.line'''
                show_line = lambda x, y, z: (lambda p: self.show_line(x, y, z))
                current_istruction_label[col].bind("<Button-1>", show_line(state.filepath, state.line,
                                                                          self.states[0].thread_set[state.thread]))
            i += 1

        self.states[0].current_state = i - 1
        # print "END CURRENT STATE = " + str(self.states[0].current_state)

    def show_line(self, filepath, line, color):

        try:
            self.win_list[filepath]
            # TODO: EVIDENZIA LINEA (DA AGGIUNGERE COME PARAMETRO)
            print "esiste: "
            win = self.win_list[filepath].frame.interior
            labels = win.winfo_children()
            for label in labels:
                if color == label.cget("bg"):
                    if line % 2:
                        label.configure(bg="#D3D3D3")
                    else:
                        label.configure(bg="#d9d9d9")

            labels[line-1].configure(bg=color)

        except KeyError:
            print "non esiste"
            # TODO: RICHIAMA CREATE WINDOW ED EVIDENZIA LINEA
            self.createWindowCode(filepath)

    def resetTrace(self, title):
        win = self.win_list[title].frame.interior
        self.states[0].current_state = - 1
        for labelFrame in win.winfo_children():
            for label in labelFrame.winfo_children():
                label.destroy()

    def PrintNextState(self, title):

        curr_state = self.states[0].current_state + 1

        if curr_state < len(self.states):
            self.states[0].current_state = curr_state
            local_states = list()
            i = curr_state

            if self.step_mode.get() == "Context Switch":
                current_thread = self.states[i].thread
                while i < len(self.states) and current_thread == self.states[i].thread:
                    local_states.append(self.states[i])
                    i += 1

            elif self.step_mode.get() == "Round":
                last_thread = (self.states[0].thread_set.keys())[-1]
                while i < len(self.states) and last_thread != self.states[i].thread:
                    local_states.append(self.states[i])
                    i += 1

                # STAMPO I RIMANENTI
                while i < len(self.states) and last_thread == self.states[i].thread:
                    local_states.append(self.states[i])
                    i += 1
            else:
                local_states.append(self.states[i])
                i += 1

            local_states[0].current_state = curr_state
            self.printStates(local_states, self.win_list[title].frame.interior)
            self.states[0].current_state = i - 1

    def random_color(self):
        import random
        r = lambda: random.randint(128, 255)
        return '#%02X%02X%02X' % (r(), r(), r())

    def PrintPreviusState(self, title):

        win = self.win_list[title].frame.interior
        curr_state = self.states[0].current_state

        if curr_state >= 0:
            i = curr_state

            if self.step_mode.get() == "Context Switch":
                current_thread = self.states[curr_state].thread
                while i >= 0 and current_thread == self.states[i].thread:
                    i -= 1

            elif self.step_mode.get() == "Round":

                first_thread = (self.states[0].thread_set.keys())[0]
                while i >= 0 and first_thread != self.states[i].thread:
                    i -= 1

                while i >= 0 and first_thread == self.states[i].thread:
                    i -= 1

            else:
                i -= 1

            for labelFrame in win.winfo_children():
                label = labelFrame.winfo_children()
                for j in range(i+1 , curr_state+1):
                    label[j].destroy()  # .grid_forget()

            print curr_state
            self.states[0].current_state = i

    def save_visual_Trace(self):
        import pickle

        path = str(tkFileDialog.asksaveasfilename(initialdir="/", title="Chose trace path",
                                                  filetypes=((" files", "*.vtrace"), ("all files", "*.*"))))

        if not path.endswith(".vtrace") and path != "":
            path += ".vtrace"

        self.states[0].current_state = 0 #TODO: AZZERO LO STATO, FACCIO RESET?
        with open(path, 'wb') as handle:
            pickle.dump(self.states, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_visual_Trace(self, path):
        import pickle

        with open(path, 'rb') as handle:
            self.states = pickle.load(handle)

        for win in self.win_list.values():
            try:
                win.destroy()
            except:
                pass

        self.createWindowTrace(path, len(self.states[0].thread_set))
        self.drwawTrace(self.states, self.win_list[path].frame.interior)


prova = RunCseq()
