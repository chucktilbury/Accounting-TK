#!/usr/bin/env python3
import sys, uuid
import tkinter as tk
import tkinter.ttk as ttk

class EventHandler(object):
    '''
    This class implements a simple way to handle communications between classes.
    It could be used generically, but it was designed for this purpose. It
    operates by making lists of callbacks that can be called from any other
    class. When a callback is registered by multiple classes, every instance is
    called in the order that it was created.

    This is a singleton class. When you instantiate it for another class, use the
    x.get_instance() method. It must never be instantiated directly. When the
    get_instance() method is called for the first time, the object is created.
    '''
    __instance = None

    @staticmethod
    def get_instance():
        '''
        This static method is used to get the singleton object for this class.
        '''
        if EventHandler.__instance == None:
            EventHandler()
        return EventHandler.__instance

    def __init__(self):

        # gate the access to __init__()
        if EventHandler.__instance != None:
            raise Exception("EventHandler class is a singleton. Use get_instance() instead.")
        else:
            EventHandler.__instance = self

        self.__event_list__ = {}

    def register_event(self, name, callback):
        '''
        Store the event in the internal storage.
        '''
        # print("%s: %s: %s.%s"%(
        #             sys._getframe().f_code.co_name,
        #             name,
        #             callback.__self__.__class__.__name__,
        #             callback.__name__))

        if not name in self.__event_list__:
            self.__event_list__[name] = []
        self.__event_list__[name].append(callback)


    def raise_event(self, name, *args):
        '''
        Call all of the callbacks that have been registered.
        '''
        # print("%s: %s"%(sys._getframe().f_code.co_name, name))
        if name in self.__event_list__:
            for cb in self.__event_list__[name]:
                if len(args) != 0:
                    cb(*args)
                else:
                    cb()
        # print("%s: %s"%(sys._getframe().f_code.co_name, "returning"))

    def dump_events(self):
        for item in self.__event_list__:
            print("%s:"%item)
            for cb in self.__event_list__[item]:
                print("\t%s.%s"%(cb.__self__.__class__.__name__, cb.__name__))


class ScrollableFrame(ttk.Frame):
    '''
    This is the scrollable frame class that is used by the NoteBk class. It
    could be used generically, but it was designed for use here.

    To get the frame to bind widgets to, call the object directly.

    The scrolling functionality supports both a scroll bar as well as the
    mouse wheel.
    '''

    def __init__(self, container, height=300, width=500, *args, **kwargs):

        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self, height=height, width=width)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollwindow = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollwindow, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.configure(yscrollincrement='20')

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollwindow.bind("<Configure>", self.configure_window)
        self.scrollwindow.bind("<Enter>", self.enter_handler)
        self.scrollwindow.bind("<Leave>", self.leave_handler)
        self.scrollwindow.bind('<Button-4>', self.mouse_wheel)
        self.scrollwindow.bind('<Button-5>', self.mouse_wheel)
        self.canvas.focus_set()

    def __call__(self):
        ''' Get the master frame for embedded widgets. '''
        #print('here')
        return self.scrollwindow

    # PORTABILITY! This may not be the same on every platform. It works under
    # linux using xfce. Other must be tested. The problem that this solves is
    # that mousewheel events are only routed to the widget that the mouse is
    # pointing to. If the mouse is hovering over a label or something, the
    # canvas never gets the event. Surprisingly, the enter and leave events
    # are both sent when the mousewheel is rolled. I am sure that this is an
    # "unsupported" feature. If the mousewheel stops working, this is where
    # to look for a fix.
    def enter_handler(self, event):
        #print('enter', event.state)
        state = (event.state & 0x1800) >> 11
        direction = 0
        if state == 2:
            direction = 1
        if state == 1:
            direction = -1
        #print(direction)
        self.canvas.yview_scroll(direction, tk.UNITS)

    def leave_handler(self, event):
        #print('leave', event.state)
        pass

    def configure_window(self, event):
        #print('here', self.mark)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def mouse_wheel(self, event):
        direction = 0
        if event.num == 5:
            direction = 1
        if event.num == 4:
            direction = -1
        #print(direction)
        self.canvas.yview_scroll(direction, tk.UNITS)

class NoteBkBtn(tk.Button):
    '''
    This Button class keeps track of the state is relation to the NoteBk
    class. It makes no sense outside of that context.
    '''

    def __init__(self, master, title, uuid, *args, **kargs):
        super().__init__(master, *args, **kargs)
        self.configure(width=10)
        self.configure(command=self.btn_cmd)
        self.configure(text=title)
        self.last_state = True
        self.title = title
        self.uuid = uuid
        self.events = EventHandler.get_instance()

    def btn_cmd(self):
        #print('here', self.title)
        self.events.raise_event('clearButtons_%s'%(self.uuid))
        self.set_state(False)
        self.events.raise_event('show_frame_%s'%(self.title), self.title)

    def set_state(self, state):
        if state:
            self.configure(relief=tk.RAISED)
        else:
            self.configure(relief=tk.SUNKEN)
        self.last_state = state

    def set_last_state(self):
        #print('here1')
        self.set_state(self.last_state)

class NoteBk(tk.Frame):
    '''
    Build a frame where there are buttons on the left and a area for widgets
    on the right. Pressing a button on the left activates a frame that is
    connected to it. The frames on the right are passed in as references to a
    class constructor. NoteBk frames can be nested such that the higher level
    NoteBk can hide and display a lower level NoteBk.

    Frames are kept as a list and are not destroyed during use. They are
    hidden and displayed using the grid layout manager.

    To properly use this container, first instantiate the class, then add
    all of the tabs. The tab name is used for the button and also internally
    to coordinate the tab buttons and display the frames connected to the
    tabs. The tab names are used to connect the widgets in the frame to the
    frame itself.
    '''

    def __init__(self, master, height=500, width=500, *args, **kargs):

        super().__init__(master, *args, **kargs)
        self.master = master
        self.width = width
        self.height = height
        self.btn_frame = tk.LabelFrame(self.master, height=height, width=20, bd=1)
        self.wid_frame = tk.LabelFrame(self.master, height=height, width=width, bd=1)
        self.uuid = uuid.uuid4().hex

        self.btn_frame.grid(row=0, column=0, sticky=tk.N)
        self.wid_frame.grid(row=0, column=1)

        self.frame_list = {}
        self.frame_index = 0

        self.events = EventHandler.get_instance()
        self.events.register_event('clearButtons_%s'%(self.uuid), self.clear_buttons)

    def clear_buttons(self):
        #print('here2')
        for item in self.frame_list:
            self.frame_list[item]['btn'].set_state(True)

    def get_uuid(self):
        return self.uuid

    def show_frame(self, title):
        for item in self.frame_list:
            #print(item)
            self.frame_list[item]['frame'].grid_forget()
            self.frame_list[item]['btn'].set_last_state()

        #print(self.frame_list[title]['frame'])
        self.frame_list[title]['frame'].grid(row=0, column=1)

        # call the callback when the tab button is pressed, if it was
        # specified when the tab was added.
        if not self.frame_list[title]['callback'] is None:
            self.frame_list[title]['callback']()


    def get_frame(self, title):
        '''
        Use this to get the frame to bind widgets to.
        '''
        return self.frame_list[title]['frame']()

    def add_tab(self, title, callback=None):
        '''
        Add a new tab to the notebook.
        '''
        self.events.register_event('show_frame_%s'%(title), self.show_frame)
        panel_frame = {}
        btn = NoteBkBtn(self.btn_frame, title, self.uuid)
        btn.grid(row=self.frame_index)
        panel_frame['btn'] = btn
        panel_frame['frame'] = ScrollableFrame(self.wid_frame, height=self.height, width=self.width)
        panel_frame['callback'] = callback
        self.frame_list[title] = panel_frame

        if self.frame_index == 0:
            btn.set_state(True)
            self.show_frame(title)

        self.frame_index += 1


if __name__ == '__main__':
    master = tk.Tk()
    n = NoteBk(master)

    # add the tabs
    n.add_tab('tab1')
    n.add_tab('tab2')
    n.add_tab('tab3')

    # connect the widgets to them
    tk.Label(n.get_frame('tab1'), text='this is tab1').grid(row=0, column=0)
    tk.Label(n.get_frame('tab2'), text='this is tab2').grid(row=0, column=0)
    tk.Label(n.get_frame('tab3'), text='this is tab3').grid(row=0, column=0)

    # retrieve the frame of the second tab
    f1 = n.get_frame('tab2')

    # embed a nested notebook in the second tab.
    n1 = NoteBk(f1)
    # create the tabs for the embedded notebook
    n1.add_tab('tab2.1')
    n1.add_tab('tab2.2')
    n1.add_tab('tab2.3')

    # add widgets to the tabs.
    tk.Label(n1.get_frame('tab2.1'), text='this is tab2.1').grid(row=0, column=0)
    tk.Label(n1.get_frame('tab2.2'), text='this is tab2.2').grid(row=0, column=0)
    tk.Label(n1.get_frame('tab2.3'), text='this is tab2.3').grid(row=0, column=0)

    master.mainloop()