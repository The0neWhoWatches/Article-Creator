import os
import tkinter as tk
import webbrowser
from tkinter import filedialog
from guizero import App, MenuBar, PushButton, Text, TextBox, Window, ListBox, ButtonGroup
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
BG = "#ffffff"
startA = App(title="Article Creator Main Menu")
startA.bg = BG
def docs():
  docW = Window(startA, title="Article Creator Editor Documentation",bg=BG)
  Text(docW, text="Documentation",size=30)
  Text(docW,text='''
#T = title
#S = subheading
#t = text
#tB = bold text
#tI = italic text
#tU = underlined text
#tH = highlited text
#tS = strikethrough text
#L = link [link destination] {link title}
[text] = text
[ ] or [] = spacer
  ''')
def create():
  file_name = startA.question("File Name", "What would you like to name your file?")
  if str(file_name).endswith('.txt'):
    if " " in str(file_name):
      file_name = str(file_name).replace(" ", "_")
  else:
    file_name = str(file_name) + '.txt'
    if " " in str(file_name):
      file_name = str(file_name).replace(" ", "_")
  if os.path.exists(str(file_name)):
    startA.error("Error", "File already exists")
  else:
    editW = Window(startA, title="Article Creator Editor", bg=BG)
    file_data = TextBox(editW, multiline=True,scrollbar=True, width=120, height=36)
    PushButton(editW, text="Documentation",pady=7,padx=15,command=docs)
    file_nameS = Text(editW, text="File Name: " + str(file_name))
    def save():
      try:
        with open(str(file_name), "w") as sf:
          sf.write(str(file_data)[28:-1])
          editW.info("Saved", "File saved")
      except FileNotFoundError:
        editW.error("Error","Could not save file")
    def save2():
      try:
        with open(str(file_name), "w") as sf:
          sf.write(str(file_data)[28:-1])
          editW.destroy()
      except FileNotFoundError:
        editW.error("Error","Could not save file")
    def view2():
      v2 = editW.yesno("Warning!", "Did you SAVE your file?")
      if v2 == True:
        editW.destroy()
        view()
      else:
        pass
    def select_all():
      file_data.tk.focus_set()
      file_data.tk.tag_add("sel", "1.0", "end")
    def delete_selected():
      start_index = file_data.tk.index("sel.first")
      end_index = file_data.tk.index("sel.last")
      file_data.tk.delete(start_index, end_index)
    def clear_all():
      ca = editW.yesno("WARNING", "Are you sure? This will clear ALL your progress!")
      if ca == True:
        file_data.tk.delete("1.0", "end")
      else:
        pass
    def open_file():
      of = editW.yesno("WARNING", "Are you sure? This will clear ALL your progress!")
      if of == True:
        file_name = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        file_data.tk.delete("1.0", "end")
        with open(file_name, "r") as sf:
          file_data.tk.insert("1.0", sf.read())
      else:
        pass
    def save_to_file():
      file_name = filedialog.asksaveasfilename(initialdir="/", title="Select File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
      with open(file_name, "w") as sf:
        sf.write(str(file_data)[28:-1])
    def append_file():
      file_name = filedialog.asksaveasfilename(initialdir="/", title="Select File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
      with open(file_name, "a") as sf:
        sf.write(str(file_data)[28:-1])
    def share_email():
      try:
        with open(str(file_name), "w") as sf:
          sf.write(str(file_data)[28:-1])
      except FileNotFoundError:
        editW.error("Error","Could not save file")
      def send_email(sender_email, sender_password, recipient_email, subject, body, file_name):
        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_email
        # Add attachment if a file name is provided
        if file_name:
            with open(file_name, "rb") as f:
                file_data = f.read()
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_name)}"')
            message.attach(attachment)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
      sender_email = editW.question("Email", "What is your email address?")
      sender_password = editW.question("Password", "What is your email password? (This information is not shared, saved, or sold)")
      recipient_email = editW.question("Recipient", "Who are you sending this to (email)?")
      subject = editW.question("Subject", "What is the subject of your email?")
      body = editW.question("Body", "What is the body text of your email?")
      try:
        send_email(sender_email, sender_password, recipient_email, subject, body, file_name)
        #resets variable password so it is not saved
        sender_password = ""
      except smtplib.SMTPAuthenticationError:
        editW.error("Error", "Could not send email")
    def change_file_name():
      file_name = editW.question("Change File Name", "Please enter new File name:")
      if str(file_name).endswith('.txt'):
        if " " in str(file_name):
          file_name = str(file_name).replace(" ", "_")
      else:
        file_name = str(file_name) + '.txt'
        if " " in str(file_name):
          file_name = str(file_name).replace(" ", "_")
      if os.path.exists(str(file_name)):
        startA.error("Error", "File already exists")
      else:
        file_nameS.clear()
        file_nameS.append("File name: " + str(file_name) + " (renamed)")
    MenuBar(editW,
      toplevel=["File", "Edit", "Share"],
      options=[
        [ ["Save", save] , ["Save and Exit", save2], ["View", view2], ["Open File", open_file], ["Overwrite File", save_to_file],["Append to File",append_file], ["Change File Name", change_file_name] ],
        [ ["Select All", select_all] , ["Clear All", clear_all] , ["Delete Selected", delete_selected] ],
        [ ["Share (Email)", share_email] ]
      ])
def view():
  root = tk.Tk()
  root.withdraw()
  file_path = filedialog.askopenfilename(
    initialdir = "/",
    title = "Select a file",
    filetypes = (("Text files", "*.txt"), ("all files", "*.*"))
  )
  if file_path:
    try:
      #Interpreter:
      with open(file_path, "r") as f:
        lines = f.readlines()
        viewW = Window(startA, title="Article",bg=BG)
        for line in lines:
          if line.startswith("#T "):
            t = line
            t = t[3:-1]
            Text(viewW, text=t).tk.config(font="Times 30")
          elif line.startswith("#S "):
            s = line
            s = s[3:-1]
            Text(viewW, text=s).tk.config(font="Times 20")
          elif line.startswith("#t "):
            te = line
            te = te[3:-1]
            Text(viewW, text=te).tk.config(font="Times 12")
          elif line.startswith('#tB '):
            teB = line
            teB = teB[4:-1]
            Text(viewW, text=teB).tk.config(font="Times 12 bold")
          elif line.startswith('#tI '):
            teI = line
            teI = teI[4:-1]
            Text(viewW, text=teI).tk.config(font="Times 12 italic")
          elif line.startswith('#tU '):
            teU = line
            teU = teU[4:-1]
            Text(viewW, text=teU).tk.config(font="Times 12 underline")
          elif line.startswith('#tS '):
            teS = line
            teS = teS[4:-1]
            Text(viewW, text=teS).tk.config(font="Times 12 overstrike")
          elif line.startswith('#tH '):
            teH = line
            teH = teH[4:-1]
            Text(viewW, text=teH, bg="#ebeb05").tk.config(font="Times 12")
          elif line.startswith('#L'):
            def redirectL(Hlink):
              if Hlink.startswith("https://"):
                try:
                  webbrowser.open(Hlink)
                except:
                  viewW.error("Error", "Could not open link")
              else:
                Hlink = "https://" + Hlink
                try:
                  webbrowser.open(Hlink)
                except:
                  viewW.error("Error", "Could not open link")
            link = line
            link = link[3:-1]
            link2 = link
            start_index = link.find("[") + 1
            end_index = link.find("]")
            Hlink = link[start_index:end_index]
            start_index2 = link2.find("{") + 1
            end_index2 = link2.find("}")
            Tlink = link2[start_index2:end_index2]
            PushButton(viewW, text=Tlink, command=lambda:redirectL(Hlink))
          elif line == '' or line == ' ':
            Text(viewW, text=' ').tk.config(font="Times 12")
          else:
            n = line
            Text(viewW, text=n).tk.config(font="Times 12")
    except FileNotFoundError:
      startA.error("File Error", "Could not find file")
def settings():
  setW = Window(startA, title="Settings",bg=BG)
  def changeV():
    setW2 = Window(startA, title="Change Version",bg=BG)
    Text(setW2, text="Change Version",size=30)
    Text(setW2, text="Please Select a Version",size=10)
    Text(setW2, text="Note: when program is closed, you will return back to the newest version",size=10)
    cv = ButtonGroup(setW2, options=[
      ["Article Creator 1.1 (BETA)", "1.1"],
      ["Article Creator 1.0.1 (Current)", "1.0.1"],
      ["Article Creator 1.0","1.0"]
    ],
      selected="1.0.1")
    def runV():
      if cv.value == '1.1':
        setW.destroy()
        setW2.destroy()
        startA.destroy()
        import ac1_1
      if cv.value == "1.0.1":
        setW2.info(setW2, text="You are already running Article Creator 1.0.1")
      if cv.value == '1.0':
        setW.destroy()
        setW2.destroy()
        startA.destroy()
        import ac1_0
    PushButton(setW2, text="Run Now",command=runV)
  Text(setW, text="Settings",size=30)
  Text(setW, text="Version", size=20)
  Text(setW, text="Article Creator Version: v1.0.1", size=10)
  PushButton(setW, text="Change Version",command=changeV)
  Text(setW, text='''Features:
-Updated Documentation
-More secure when using Email sharing
-"Save to File" replaced with "Overwrite File"
-New File feature in Editor: "Append to File"
-Fixed "Share (Email)" bug
-Use Older Versions in Settings''', size=10)
  Text(setW, text="Created With", size=20)
  Text(setW, text='''Made with: Python
GUI used: Guizero
IDE used: Replit''', size=10)
  ListBox(setW, items=['DOCUMENTATION FOR ARTICLE CREATOR', 'For: Version v1.0.1', 'Updated on: October 11, 2024', 'Article Creator is a text editor that allows you to create articles. It has a main menu, an editor, a viewer, and other settings.', 'It was made with Python Programming Language and the GUI library Guizero. The IDE used to make this is Replit IDE. Article Creator is not under copyright or trademark and it is free to use.', 'If Article Creator is asking for money or personal information*, DO NOT ANSWER THE QUESTIONS AND IMMEDIATELY UNINSTALL ARTICLE CREATOR.', 'Since Article Creator is free, DONT BUY ARTICLE CREATOR IF IT COSTS MONEY (unless it is a mod).','*-when sharing with Email, Article Creator WILL ask for your email password.','Article Creator is secure and will not store this password.','HOWEVER, please use caution when using a adjusted or modded Article Creator, since it may not be secure.'], width=1200, height=200)
def main_menu():
  Text(startA, text="Article Creator", size=30)
  Text(startA, text="v1.0.1",size=10)
  PushButton(startA, text="Settings", pady=7, padx=10,command=settings)
  PushButton(startA, text="View",pady=7,padx=21,command=view)
  PushButton(startA, text="Editor",pady=7,padx=17,command=create)
main_menu()
startA.display()