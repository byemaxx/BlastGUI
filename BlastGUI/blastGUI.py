#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Wu Qing
# E-mail: cipn@qq.com

import os
import re
import subprocess
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
import tkinter.filedialog
import tkinter.simpledialog
from tkinter.ttk import Style
import shutil


def make_db():
    def make_db_button_cmd():
        if fndb == '':
            return showinfo(title='warning', message='The build database file is not selected!')
        if mkdb_type.get() != 'Nucleic acid sequence' and mkdb_type.get() != 'Protein sequence':
            return showinfo(title='warning', message='The database type is not selected!')
        if db_name_input.get() == '':
            return showinfo(title='warning', message='Database name is not set!')
        if mkdb_type.get() == 'Nucleic acid sequence':
            t = 'nucl'
        if mkdb_type.get() == 'Protein sequence':
            t = 'prot'
        n = db_name_input.get()
        p = subprocess.Popen(
            "makeblastdb -parse_seqids -in " + fndb + " -dbtype " + t + " -title " + n + " -out " + n,
            shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.stdout.readlines()
        if p.returncode == 0:
            showinfo(title="info", message="Database builded successfully!")
            makedb_state.delete(0.0, END)
            for line in out:
                makedb_state.insert("insert", line)
        else:
            showinfo(title="info", message="Database creation failed!")

    def select_fadb_button_cmd():
        global fndb
        fndb = tkinter.filedialog.askopenfilename()
        make_db_label.config(text="The files you selected:\n" + fndb)

    def mkdb_instruction():
        makedb_state.insert('1.0', "1. Click select file button to select FASTA file \n\n2. Select database type \n\
            \n3. Enter the name of the database (no Spaces)\n\
            \n4. Click Build database button to start database building \n\
            \n5.After the database construction is completed, please restart this program to refresh the database list")

    dbwindow = Tk()
    dbwindow.title('Build database')
    dbwindow.geometry('600x400')

    mkdb_typeList = ['Nucleic acid sequence', 'Protein sequence', ]
    mkdb_type = Combobox(dbwindow, text='Nucleic acid sequence', values=mkdb_typeList, font=('', 13))
    mkdb_type.place(relx=0.394, rely=0.192, relwidth=0.251)

    makedb_stateFont = Font(font=('', 13))
    makedb_state = Text(dbwindow, font=makedb_stateFont)
    makedb_state.place(relx=0.041, rely=0.505, relwidth=0.915, relheight=0.435)
    mkdb_instruction()

    style.configure('Tmake_db_button.TButton', font=('', 13))
    make_db_button = Button(dbwindow, text='Build database', command=make_db_button_cmd, style='Tmake_db_button.TButton')
    make_db_button.place(relx=0.705, rely=0.216, relwidth=0.251, relheight=0.219)

    db_name_inputVar = StringVar(value='db')
    db_name_input = Entry(dbwindow, textvariable=db_name_inputVar, font=('', 13))
    db_name_input.place(relx=0.394, rely=0.336, relwidth=0.251, relheight=0.099)

    style.configure('Tselect_fadb_button.TButton', font=('', 13))
    select_fadb_button = Button(dbwindow, text='Select file', command=select_fadb_button_cmd, style='Tselect_fadb_button.TButton')
    select_fadb_button.place(relx=0.705, rely=0.048, relwidth=0.251, relheight=0.123)

    style.configure('Tdb_type_label.TLabel', anchor='w', font=('', 13))
    db_type_label = Label(dbwindow, text='Select database type', style='Tdb_type_label.TLabel')
    db_type_label.place(relx=0.041, rely=0.192, relwidth=0.272, relheight=0.099)

    style.configure('Tdb_name.TLabel', anchor='w', font=('', 13))
    db_name = Label(dbwindow, text='Set database name', style='Tdb_name.TLabel')
    db_name.place(relx=0.041, rely=0.336, relwidth=0.272, relheight=0.099)

    style.configure('Tmake_db_label.TLabel', anchor='center', font=('', 13))
    make_db_label = Label(dbwindow, text='You did not select any files', style='Tmake_db_label.TLabel')
    make_db_label.place(relx=0.041, rely=0.048, relwidth=0.602, relheight=0.105)

    dbwindow.mainloop()


def get_fasta():
    input = fa_input.get()
    tmp = ''.join(re.findall(r'[A-Za-z]', input))
    if tmp == '':
        showinfo(title='warning', message='Please enter the correct sequence')
        return 1
    else:
        #tmp = str.upper(tmp)
        with open("tmp.txt", "w+") as f:
            f.write(tmp)
        return 0



# get database name list
def get_db_name():
    namelist = []
    for fn in os.listdir(os.getcwd()):
        if os.path.splitext(fn)[1] == '.phr' or os.path.splitext(fn)[1] == '.nhr':
            fn = os.path.splitext(fn)[0]
            namelist.append(fn)
    return namelist


# blast process
def star():
    fnfa_stat = "The files you selected:" + fnfa
    fain_stat = fa_input.get()

    if fnfa_stat == fain_stat:
        fa = fnfa
    else:
        fa = 'tmp.txt'

    b = subprocess.Popen(blast_type.get() + " -out result.txt -query " + fa + " -outfmt " + outfmt_input.get() +
                         " -evalue " + evalue.get() + " -db " + db_type.get() + ' -num_threads ' + threat_input.get() + 
                         ' ' + othercmd_input.get(),
                         shell=True, stdout=subprocess.PIPE)
    b.wait()

    if b.returncode == 0:
        result_output.delete(0.0, END)
        with open("result.txt", "r") as result:
            for line in result:
                result_output.insert('insert', line)
    else:
        showinfo(title='warning', message='Wrong alignment!\nPlease make sure the parameters are set correctly!')


def star_blast_cmd():
    try:
        os.remove((os.path.join(os.getcwd(), 'tmp.txt')))
        os.remove((os.path.join(os.getcwd(), 'result.txt')))
    finally:
        if get_fasta() == 1:
            return 1
        if get_fasta() == 0:
            star()
            return 0


def select_fa_button_Cmd():
    global fnfa
    fnfa = tkinter.filedialog.askopenfilename()
    fa_input.delete(0, END)
    if fnfa != '':
        fa_input.insert(END, "The files you selected:" + fnfa)
    else:
        fa_input.insert(END, "Enter a sequence here or select a sequence file:")
    pass



def about_cmd():
    showinfo(title='Abount', message='BlstaGUI\n\nAuthor：Wu Qing\n\nSichuan agricultural university,China\n\nVersion:V1.0')


def main_instructions():
    result_output.insert('1.0', 'Instructions:\n\n1. Please click the [Build database] button to set up the database for the first time\n \
    \n2.Input the sequence to be aligned into the text box or select the sequence file through the [Select file] button \
     \n\n3.Select the database to be compared and the comparison method.\n\n4.Set the e-value Value, output format and number of threads.The default e-value =1e-5, and the default output format is 0 and the default of threads is 4\n \
     \n5.(Optional) Any other command of BLAST like: -max_target_seqs 20 \n\n6.Click [Start] button for comparison, and the comparison results will be displayed here and saved in result.txt\n\n7.Alignment time depends on sequence size and computer performance \
     \n')


def mkdb_window_cmd():
    make_db()


top = Tk()
top.title('BlastGUI')
top.geometry('960x640')

style = Style()
fnfa = ''
fndb = ''

db_typeList = get_db_name()
db_type = Combobox(top, text='Select', values=db_typeList, font=('', 13))
db_type.place(relx=0.129, rely=0.106, relwidth=0.11)

blast_typeList = ['blastn', 'blastp', 'blastx', 'tblastn', 'tblastx', ]
blast_typeVar = StringVar(value='blastn')
blast_type = Combobox(top, textvariable=blast_typeVar, values=blast_typeList, font=('', 13))
blast_type.place(relx=0.386, rely=0.1, relwidth=0.08)

reault_scroll1 = Scrollbar(top, orient='vertical')
reault_scroll1.place(relx=0.959, rely=0.212, relwidth=0.031, relheight=0.758)

evalueVar = StringVar(value='1e-5')
evalue = Entry(top, textvariable=evalueVar, font=('', 12))
evalue.place(relx=0.129, rely=0.166, relwidth=0.11, relheight=0.034)

result_outputFont = Font(font=('', 13))
result_output = Text(top, yscrollcommand=reault_scroll1.set, font=result_outputFont)
result_output.place(relx=0.02, rely=0.212, relwidth=0.931, relheight=0.773)
main_instructions()
reault_scroll1['command'] = result_output.yview

star_blastVar = StringVar(value='Start')
style.configure('Tstar_blast.TButton', background='#000000', font=('', 13))
star_blast = Button(top, text='Start', textvariable=star_blastVar, command=star_blast_cmd, style='Tstar_blast.TButton')
star_blast.place(relx=0.791, rely=0.015, relwidth=0.08, relheight=0.138)


style.configure('Tselect_fa_button.TButton', background='#000000', font=('', 13))
select_fa_button = Button(top, text='Select\n   file', command=select_fa_button_Cmd,
                          style='Tselect_fa_button.TButton')
select_fa_button.place(relx=0.692, rely=0.015, relwidth=0.09, relheight=0.138)

fa_inputVar = StringVar(value='Enter a sequence here or select a sequence file:')
fa_input = Entry(top, textvariable=fa_inputVar, font=('', 13))
fa_input.place(relx=0.02, rely=0.015, relwidth=0.654, relheight=0.078)

aboutVar = StringVar(value='About')
style.configure('Tabout.TButton', font=('', 13))
about = Button(top, text='About', textvariable=aboutVar, command=about_cmd, style='Tabout.TButton')
about.place(relx=0.88, rely=0.015, relwidth=0.11, relheight=0.065)

mkdb_windowVar = StringVar(value=' Build\ndatabase')
style.configure('Tmkdb_window.TButton', font=('', 13))
mkdb_window = Button(top, text='Build database', textvariable=mkdb_windowVar, command=mkdb_window_cmd, style='Tmkdb_window.TButton')
mkdb_window.place(relx=0.88, rely=0.091, relwidth=0.11, relheight=0.065)

evalue_labelVar = StringVar(value='E-value：')
style.configure('Tevalue_label.TLabel', anchor='w', font=('', 12))
evalue_label = Label(top, text='E-value', textvariable=evalue_labelVar, style='Tevalue_label.TLabel')
evalue_label.place(relx=0.02, rely=0.166, relwidth=0.09, relheight=0.032)

blast_select_labelVar = StringVar(value='Methods：')
style.configure('Tblast_select_label.TLabel', anchor='w', font=('', 12))
blast_select_label = Label(top, text='Methods', textvariable=blast_select_labelVar, style='Tblast_select_label.TLabel')
blast_select_label.place(relx=0.267, rely=0.106, relwidth=0.09, relheight=0.032)

db_selectVar = StringVar(value='Database:')
style.configure('Tdb_select.TLabel', anchor='w', font=('', 12))
db_select = Label(top, text='Database', textvariable=db_selectVar, style='Tdb_select.TLabel')
db_select.place(relx=0.02, rely=0.106, relwidth=0.09, relheight=0.032)

outfmt_labelVar = StringVar(value='Outfmt:')
style.configure('Toutfmt_label.TLabel', anchor='w', font=('', 12))
outfmt_label = Label(top, text='Outfmt', textvariable=outfmt_labelVar, style='Toutfmt_label.TLabel')
outfmt_label.place(relx=0.267, rely=0.166, relwidth=0.09, relheight=0.032)

outfmt_inputVar = StringVar(value='0')
outfmt_input = Entry(top, textvariable=outfmt_inputVar, font=('', 12))
outfmt_input.place(relx=0.386, rely=0.166, relwidth=0.08, relheight=0.034)

threat_labelVar = StringVar(value='Threads:')
style.configure('Tthreat_label.TLabel', anchor='w', font=('', 12))
threat_label = Label(top, text='Threads:', textvariable=threat_labelVar, style='Tthreat_label.TLabel')
threat_label.place(relx=0.494, rely=0.106, relwidth=0.08, relheight=0.032)

threat_inputVar = StringVar(value='4')
threat_input = Entry(top, textvariable=threat_inputVar, font=('', 12))
threat_input.place(relx=0.593, rely=0.106, relwidth=0.08, relheight=0.034)

othercmd_labelVar = StringVar(value='Other cmd:')
style.configure('Tothercmd_label.TLabel', anchor='w', font=('', 12))
othercmd_label = Label(top, text='other cmd', textvariable=othercmd_labelVar, style='Tothercmd_label.TLabel')
othercmd_label.place(relx=0.494, rely=0.166, relwidth=0.08, relheight=0.032)

othercmd_inputVar = StringVar(value=' ')
othercmd_input = Entry(top, textvariable=othercmd_inputVar, font=('', 12))
othercmd_input.place(relx=0.593, rely=0.166, relwidth=0.19, relheight=0.034)

top.mainloop()
