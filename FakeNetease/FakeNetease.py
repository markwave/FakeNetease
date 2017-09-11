
from tkinter import *

from tkinter.ttk import *

from pygame import mixer

from PIL import Image, ImageTk

from tkinter import messagebox

import os

import requests

import json

import threading





def search():

    word = entry.get().encode('utf-8')

    if not word:

        messagebox.showinfo("Duang!",'亲，请输入歌曲名再搜索~')

        return

   
    url = 'http://music.163.com/api/search/pc'

    payload = {'type':1,'s':word}
    
    r = requests.post(url, data = payload).text

    js = json.loads(r)

    listbox.delete(0, END)

    global results

    results = js['result']['songs']

    for i in results:
        
        choice = i['name']+"-"+i['artists'][0]['name']

        listbox.insert(END, choice)



index = 0

def select(self):
    
    global index, fileurl, songname, img1X, lrcUrl

    index = listbox.curselection()[0] #获取点击索引

    i = results[index]

    song_id = i['id']

    mp3Url = 'http://music.163.com/api/song/enhance/download/url?br=320000&id=%s' % song_id

    fileurl =  json.loads(requests.get(mp3Url).text)['data']['url']

    picurl = i['album']['picUrl']

    lrcUrl = 'http://music.163.com/api/song/lyric?os=pc&id=%s&lv=-1&kv=-1&tv=-1' % song_id
    
    songname = '%s.mp3' % (i['name']+"-"+i['artists'][0]['name'])
    
    picname = '%s.jpg' % (i['name']+"-"+i['artists'][0]['name'])

    r0 = requests.get(picurl)

    if os.path.exists(picname) == False:

        with open(picname, 'wb') as pic:

            pic.write(r0.content)

    img1X =ImageTk.PhotoImage(Image.open(picname).resize((200,200)))
    new_img = can.create_image(100,100,image = img1X)
    can.itemconfig(new_img, image = img1X)
    
    
    
def play():
    
    global vol_val, index
    
    if os.path.exists(songname) == False:
        
        if fileurl != None:
            r1 = requests.get(fileurl)
            
            with open(songname,'wb') as file:
                file.write(r1.content)

            mixer.init()
            mixer.music.load(songname)
            vol_var.set(5)
            mixer.music.set_volume(int(vol_var.get())/10)
            mixer.music.play()
            
        
        else:
            
            messagebox.showinfo("Duang!",'应版权方要求，该歌曲暂时下架！')

        return
    
    else:
        mixer.init()
        mixer.music.load(songname)
        vol_var.set(5)
        mixer.music.set_volume(int(vol_var.get())/10)
        mixer.music.play()


click = 0

def pause():
    
    global click
    
    if mixer.music.get_busy() == 1:
        
        if click % 2 == 0:
        
            mixer.music.pause()
            
            click += 1
        
        else:
            
            mixer.music.unpause()
            
            click += 1

        
def stop():
    
    if mixer.music.get_busy() == 1:
        
        mixer.music.stop()
        
def pre():
    
    global index
    stop()
    listbox.selection_clear(index)
    listbox.selection_set(index-1)
    select(index)
    play()
    
def nex():
    
    global index
    stop()
    listbox.selection_clear(index)
    listbox.selection_set(index+1)
    select(index)
    play()
    
def vol_down():
    
    global vol_var
    
    vol_var.set(int(vol_var.get())-1)
    mixer.music.set_volume(int(vol_var.get())/10)
    
def vol_up():
    
    global vol_var
    
    vol_var.set(int(vol_var.get())+1)
    mixer.music.set_volume(int(vol_var.get())/10)

def next_10s():

    mixer.music.set_pos(10)

def show_lrc():

    top = Toplevel()
    top.title('查看歌词')
    

    lrc = json.loads(requests.get(lrcUrl).text)['lrc']['lyric']

    text = Text(top, width = 45, height = 40)

    text.config(background = 'black', foreground = 'green', font = '华文行楷')

    text.pack()

    for rows in lrc.split('\n'):

        row = rows[10:]+'\n'

        text.insert(INSERT, row)


def doplay():

    t = threading.Thread(play())

    t.start()


    
    



if __name__ == '__main__':

    root = Tk()

    root.geometry('+800+200')

    root.title('山寨云音乐播放器')
    
    frm1 = Frame(root)
    
    frm1.pack()
    
    Label(frm1,text = '亲，你要查点啥:').grid(row=0,column=0)

    entry = Entry(frm1)
    
    entry.grid(row=0,column=1)

    Button(frm1, text='试试手气', command=search).grid(row=0,column=2)
    
    frm2 = Frame(root)
    frm2.pack()

    Button(frm2, text = '|<<',command = pre).grid(row=0,column=0)
    Button(frm2, text = '▷', command = play).grid(row=0,column=1)
    Button(frm2, text = '||', command = pause).grid(row=0,column=2)
    Button(frm2, text = '■', command = stop).grid(row=0,column=3)
    Button(frm2, text = '>>|',command = nex).grid(row=0,column=4)
    

    frm3 = Frame(root)
    
    frm3.pack()

    Button(frm3, text = 'LRC', command = show_lrc).grid(row=0,column=0)
    
    vol_var = StringVar()
    
    Button(frm3, text = 'vol-', command = vol_down).grid(row=0,column=1)
    
    lb_vol = Label(frm3, textvariable = vol_var)
    
    lb_vol.grid(row=0,column=2)
    
    Button(frm3, text = 'vol+', command = vol_up).grid(row=0,column=3)
    
    Button(frm3, text = '+10s', command = next_10s).grid(row=0,column=4)
    
    frm4 = Frame(root)
    frm4.pack()
    
    img = 'netease.jpg'
    img1=ImageTk.PhotoImage(Image.open(img))
    
    can = Canvas(frm4, width = 200, height = 200)
    can.config(background = 'white')
    can.grid(row=0,column=0)
    can.create_image(100,100, image = img1)
    #can.itemconfig(img_can,image = img1)
    
    var = StringVar()

    listbox = Listbox(frm4, width = 45, height = 11,listvariable=var)

    listbox.config(background = 'white')

    listbox.grid(row=0,column=1)
    
    listbox.bind('<Double-Button-1>', select)

    root.mainloop()

