import tkinter
import tkinter.font
from login_window import open_login_window
from word_description_window import open_description_window

window = tkinter.Tk()

window.title("TOEICVOCAMACA")
window.geometry("400x500+100+100")
window.resizable(False, False)

font=tkinter.font.Font(family="맑은 고딕", size=20)

label=tkinter.Label(window, text="TOEICVOCAMACA", width=20, height=2, font=font)
label.pack()

# 로그인 버튼
button_login=tkinter.Button(window, relief="flat" ,overrelief="groove",width=10, bd=2, text="로그인", command=lambda:open_login_window(window))
button_login.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

# 단어장 설명 버튼
button_description=tkinter.Button(window, relief="flat" ,overrelief="groove",width=10, bd=2, text="단어장 설명", command=lambda:open_description_window(window))
button_description.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)



window.mainloop()