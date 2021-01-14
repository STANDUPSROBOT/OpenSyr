import tkinter
from tkinter import * 
from tkinter import LabelFrame,Label,Entry,Button 

from main import OpenSryMain
#le * est a a eviter
										# definition des fonctions #

class Interface():


		def __init__(self):
			win=Tk()
			win.title("Syringe Pump")
			win.configure(background="light blue")
			
			self.x=OpenSryMain()
			# Partie 1 :  SYRINGE DATA #
			self.frame1=LabelFrame(win,width=5000,height=5000,bg="light blue")
			self.frame1.grid(row=0,column=0)
			self.l1=Label(self.frame1,text="SYRINGE DATA",fg="dark green",font=25,bg="light blue")
			self.l1.grid(row=0,column=1,padx=20,pady=20)
			self.l2=Label(self.frame1,text="SYRINGE DIAMETER (cm)",fg="black",font=12,bg="light blue")
			self.l2.grid(row=2,column=0,padx=10,pady=10,sticky=E)
			self.textbox_DIAMETER=Entry(self.frame1,fg="black",font=12)
			self.textbox_DIAMETER.grid(row=2,column=1)
			self.l3=Label(self.frame1,text="LENGTH OF THE EXPERIENCE (s)",fg="Black",font=12,bg="light blue")
			self.l3.grid(row=3,column=0,padx=10,pady=10,sticky=E)
			self.textbox_LENGTH=Entry(self.frame1,fg="black",font=12)
			self.textbox_LENGTH.grid(row=3,column=1)
			self.l4=Label(self.frame1,text="VOLUME TO INJECT (mL)",fg="Black",font=12,bg="light blue")
			self.l4.grid(row=4,column=0,padx=10,pady=10,sticky=E)
			self.textbox_FLOW=Entry(self.frame1,fg="black",font=12)
			self.textbox_FLOW.grid(row=4,column=1)
			

			# Partie 2 : CONTROL PUMP #
			self.l11=Label(self.frame1,text="PUMP CONTROL",fg="dark green",font=25,bg="light blue")
			self.l11.grid(row=6,column=1,padx=20,pady=20)
			self.button1=Button(self.frame1,text="RUN PUMP",font=12)
			self.button1['command']=lambda : self.rechange_bg_RUN()
			self.button1.grid(row=9,column=0,padx=10,pady=10)
			self.button2=Button(self.frame1,text="STOP PUMP",font=12)
			self.button2['command']=lambda : self.change_bg_STOP()
			self.button2.grid(row=9,column=1,padx=10,pady=10)
			self.button3=Button(self.frame1,text="RESET",font=12)
			self.button3['command']=lambda : self.rechange_bg_RESET()
			self.button3.grid(row=9,column=2,padx=10,pady=10)
			self.label22=Label(self.frame1,text="TIME ELAPSED",font=12,bg="light blue")
			self.label22.grid(row=7,column=0,padx=10,pady=10,sticky=E)
			self.label2=Label(self.frame1,text="TIME ELAPSED",font=12,bg="light blue")
			self.label2.grid(row=7,column=1,padx=10,pady=10)
			self.label11=Label(self.frame1,text="INJECTED VOLUME",font=12,bg="light blue")
			self.label11.grid(row=8,column=0,padx=10,pady=10,sticky=E)
			self.label1=Label(self.frame1,text="INJECTED VOLUME",font=12,bg="light blue")
			self.label1.grid(row=8,column=1,padx=10,pady=10)
			self.volume()

			# loop #
			win.mainloop()


		def update_parameters(self):
			serynge_diam = float(self.textbox_DIAMETER.get())
			length_of_exp = float(self.textbox_LENGTH.get())
			total_ml = float(self.textbox_FLOW.get())

			self.x.set_parameters(serynge_diam,total_ml,length_of_exp)
			
		def change_bg_STOP(self):
			self.frame1['bg']="brown1"
			self.x.stop()

		def rechange_bg_RUN(self):
			self.frame1['bg']="light blue"
			self.update_parameters()
			self.x.run()
			self.clock()
			self.volume()

		def rechange_bg_RESET(self):
			self.frame1['bg']="light blue"
			self.update_parameters()
			self.x.reset()	

		def clock(self):
			h,m,s=self.x.get_elapsed_time()	
			self.label2.config(text="{:d}:{:02d}:{:02d}".format(h, m, s))
			self.label2.after(1000,self.clock)


		def volume(self):
			self.label1.config(text=str(self.x.get_injected_volume()))
			self.label1.after(1000,self.volume)

											# fonction interface #


# programme principale #
Interface()