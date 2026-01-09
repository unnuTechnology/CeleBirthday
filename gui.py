def control_panel(_1, _2):
    panel = Tk()
    panel.title('CeleBirthday 控制面板')
    panel.geometry('600x400')
    panel.iconbitmap('./resources/cake_logo.ico')

    log.info(f'打开了 CeleBirthday 控制面板')
    panel.mainloop()
