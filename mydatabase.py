import wx
import sys
import os
import wx.lib.agw.floatspin as fs
import wx.grid as glib
import sqlite3
from table_def import *
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import wx.lib.agw.hyperlink as hl
import subprocess
import platform

__databasefile__ = os.getcwd() + "\config_file.db"
# This is the popup window used to change the settings
Session = sessionmaker(bind= engine) # create session class
session = Session() # instance of a session

def connect():
    new_connection = sqlite3.connect(__databasefile__)
    return new_connection
def number_of_rows():
    rows = session.query(func.count(GRConfig.ID)).scalar() # get number of rows in database file
    print rows
    return rows


class GRDatabase(wx.Dialog):

    def __init__(self, *args, **kwargs): # allow for non-specific parameter
        kwargs["style"] = wx.DEFAULT_DIALOG_STYLE
        kwargs["size"] = (800, 600)
        kwargs["title"] = "Configuration Database"
        wx.Dialog.__init__(self, *args, **kwargs) # instance of dialog class
        rows = number_of_rows()
        self.panel = wx.Panel(self)
        attr = glib.GridCellAttr() # Generate attribute for grid
        # attr.SetReadOnly(True) # attr is read only
        self.myGrid = glib.Grid(self.panel, -1, size = (1000, 500)) # use grid for database appearance within GUI
        self.myGrid.CreateGrid(rows, 9)
        self.myGrid.SetColLabelValue(0, "ID")
        self.myGrid.SetColLabelValue(1, "Name")
        self.myGrid.SetColSize(1, 100)
        self.myGrid.SetColLabelValue(2, "Input One")
        self.myGrid.SetColLabelValue(3, "Input Two")
        self.myGrid.SetColLabelValue(4, "Input Three")
        self.myGrid.SetColLabelValue(5, "Input Four")
        self.myGrid.SetColSize(5, 100)
        self.myGrid.SetColLabelValue(6, "Input Five")
        self.myGrid.SetColSize(6, 100)
        self.myGrid.SetColLabelValue(7, "Input Six")
        self.myGrid.SetColLabelValue(8, "Input Seven")
        # for each_row in range(0, rows):
        #     self.myGrid.SetRowAttr(each_row, attr) # Set each row to read only
        self.ret_all_data() # extracts data from database
        self.search_val = wx.StaticText(self.panel, wx.ID_ANY, "Search Name:")
        self.search_input = wx.TextCtrl(self.panel, -1,  "")
        self.load_btn = wx.Button(self.panel, wx.ID_ANY, label = "Load Configuration")
        self.delete_btn = wx.Button(self.panel, wx.ID_ANY, label = "Delete Configuration")
        self.cancel_btn = wx.Button(self.panel, wx.ID_ANY, label = "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnLoad, self.load_btn)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.delete_btn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel_btn)
        self.Bind(wx.EVT_TEXT, self.search_data, self.search_input)
        bottom_row_sizer = wx.BoxSizer(wx.HORIZONTAL) # sizer for bottom location of window with grid on it
        bottom_row_sizer.Add(self.search_val, 0, wx.ALIGN_LEFT | wx.LEFT, 100)
        bottom_row_sizer.Add(self.search_input, 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        bottom_row_sizer.Add(self.load_btn,0, wx.ALIGN_LEFT| wx.LEFT, 20)
        bottom_row_sizer.Add(self.delete_btn, 0, wx.ALIGN_LEFT| wx.LEFT, 20 )
        bottom_row_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT | wx.LEFT, 20)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.myGrid, 0, wx.ALL, 5)
        sizer.Add(bottom_row_sizer, 0, wx.ALL, 5)
        self.panel.SetSizer(sizer)




    def OnLoad(self, e):
        try:
            self.select_rows()
            new_two_value = float(self.config_vals[3]) # format proper input vals
            new_three_value = float(self.config_vals[4])
            new_four_value = float(self.config_vals[5])
            new_five_value = float(self.config_vals[6])
            new_six_value = float(self.config_vals[7])
            new_seven_value = float(self.config_vals[8])
            SettingsWindow.choiceone.SetValue(self.config_vals[2])
            SettingsWindow.twovalue.SetValue(new_two_value)
            SettingsWindow.threevalue.SetValue(new_three_value)
            SettingsWindow.four1_value.SetValue(new_four_value)
            SettingsWindow.four2_value.SetValue(new_five_value)
            SettingsWindow.fiveval.SetValue(new_six_value)
            SettingsWindow.sixvalue.SetValue(new_seven_value)
            self.Destroy()
        except IndexError: # catch index error
            wx.MessageBox("No Row Selected")





    def OnCancel(self,e):
        self.Close()
    def select_rows(self):
        x = self.myGrid.GetSelectedRows()[0]
        self.config_vals = []
        for cells in range(9):
            cell_val = self.myGrid.GetCellValue(x, cells) # takes values in row selected and appends to list
            self.config_vals.append(cell_val)


    def OnDelete(self, e):
        try:
            self.select_rows() # connect to database in order to delete there first and foremost
            cnn = connect()
            cur = cnn.cursor()
            cur.execute("DELETE FROM Configuration WHERE ID=" + "'" + self.config_vals[0] + "'")
            cnn.commit()
            cnn.close()
            self.myGrid.DeleteRows(self.myGrid.GetSelectedRows()[0], 1, True)
        except IndexError:
            wx.MessageBox("No Row Selected")
        e.Skip()

    def ret_all_data(self):
        cnn = connect()
        cur = cnn.cursor()
        cur.execute("SELECT * FROM Configuration")
        db_rows = cur.fetchall()
        self.display_data(db_rows)
        cnn.close()
    def display_data(self, rows):
        for i , val in enumerate(rows): # loops through each val and displays on grid
            for j in range(9):
                self.myGrid.SetCellValue(i, j, str(val[j]))
    def search_data(self, e): # connects to specified identifier to search for in database
        attr = glib.GridCellAttr()
        attr.SetBackgroundColour(wx.RED)
        val = self.search_input.GetValue()
        cnn = connect()
        cur = cnn.cursor()
        cur.execute("SELECT * FROM Configuration WHERE name LIKE '%" + val + "%'")
        cnn.commit()
        ind_rows = cur.fetchall()
        self.myGrid.ClearGrid() # clears grid
        self.display_data(ind_rows) # only displays relevant data on grid
        cnn.close()
        e.Skip()
class InfoDialog(wx.Dialog): # dialog to link to db file location
    def __init__(self, parent):
        super(InfoDialog, self).__init__(parent, title="Path to Database File", size=(300, 100)) # GUI implementation
        self.pnl = wx.Panel(self)
        self.container = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.text_directory = wx.StaticText(self.pnl, wx.ID_ANY, "Database File Location:")
        self.text_directory.SetFont(font)
        self.link_text_directory = hl.HyperLinkCtrl(self.pnl, wx.ID_ANY, "\\...\\%s" % os.path.basename(__databasefile__))
        self.okay_btn = wx.Button(self.pnl, wx.ID_ANY, "OK", size = (70, 50))
        self.hbox1.Add(self.text_directory, 0, wx.ALIGN_RIGHT | wx.RIGHT, 5)
        self.hbox1.Add(self.link_text_directory, 0, wx.BOTTOM, 5)
        self.hbox2.Add(self.okay_btn, 0, wx.ALIGN_LEFT | wx.LEFT, 200)
        self.container.Add(self.hbox1, 0, wx.ALL, 5)
        self.container.Add(self.hbox2, 0, wx.ALL, 5)
        self.link_text_directory.AutoBrowse(False)
        self.Bind(hl.EVT_HYPERLINK_LEFT, self.onDirClick, self.link_text_directory)
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.okay_btn)
        self.pnl.SetSizer(self.container)
        self.pnl.Fit()

    def onDirClick(self, e):
        file_path = os.path.dirname(__databasefile__)
        if platform.system() == "Windows":
            subprocess.Popen('explorer %s' % file_path)  # Links directly to where in the directory file is located
        else:
            subprocess.Popen(["xdg-open"], file_path)
    def OnOk(self,e):
        self.Close()
class SettingsWindow(wx.Frame): # frame for main settings window
    def __init__(self, *args, **kwargs): #*args and **kwargs means an unknown amount of parameters will be set within this functionb
        kwargs["style"] = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX
        kwargs["title"] = "Capture Settings"
        kwargs["size"] = (400, 270)
        super(SettingsWindow, self).__init__(*args, **kwargs)
        self.CenterOnScreen()
        self.settings_results = 'config.ini' # default file for settings value
        self.open_database = wx.MenuBar()
        self.CreateStatusBar()
        self.Menu = wx.MenuBar() # setup menu bar
        self.menu_file = wx.Menu()
        self.menu_file.Append(1, "Additional Info")
        self.Bind(wx.EVT_MENU, self.info_dialog, id = 1 )
        self.Menu.Append(self.menu_file, "Help")
        self.SetMenuBar(self.Menu)
        # Create window and sizer
        self.pnl = wx.Panel(self) # initializing panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        gs = wx.GridSizer(1, 4, 5, 10)  #setup for current GUI input layout (row, column, vgap, hgap)
        g2s = wx.GridSizer(2, 2, 20, 5) #could have done all inputs on one gridsizer but preferred the aesthetic layout of varying columns
        g3s = wx.GridSizer(1, 2, 20, 5)
        g4s = wx.GridSizer(1, 2, 20, 5)

        # g3s = wx.GridSizer(1, 2, 20)
        g4s = wx.GridSizer(1, 2, 20)
        sizer_one = wx.BoxSizer(wx.VERTICAL)
        sizer_two = wx.BoxSizer(wx.VERTICAL)
        sizer_three = wx.BoxSizer(wx.VERTICAL)
        sizer_four_l = wx.BoxSizer(wx.VERTICAL)
        sizer_four_h = wx.BoxSizer(wx.VERTICAL)
        sizer_five = wx.BoxSizer(wx.VERTICAL)
        sizer_six = wx.BoxSizer(wx.VERTICAL)
        # linesizer = wx.BoxSizer(wx.VERTICAL)


        self.twotitle = wx.StaticText(self.pnl, -1, 'Input Two')  # Creates static title for input

        SettingsWindow.twovalue = fs.FloatSpin(self.pnl, -1, min_val=10, max_val=900, increment=0.10, value=500,
                                      digits=2, agwStyle=fs.FS_CENTRE)

        SettingsWindow.twovalue.SetFormat("%f")  # Sets type value as float

        self.threetitle = wx.StaticText(self.pnl, -1, 'Input Three')
        SettingsWindow.threevalue = fs.FloatSpin(self.pnl, -1, min_val=100, max_val=1000, increment=.10,
                                      value=200,
                                      digits=3, agwStyle=fs.FS_CENTRE)

        SettingsWindow.threevalue.SetFormat("%f")

        self.four1title = wx.StaticText(self.pnl, -1, 'Input Four')
        SettingsWindow.four1_value = fs.FloatSpin(self.pnl, -1,  min_val= -1.00, max_val=.999, increment=0.0001,
                                          value= .10,
                                          digits=4, agwStyle=fs.FS_CENTRE)


        SettingsWindow.four1_value.SetFormat("%f")

        self.four2title = wx.StaticText(self.pnl, -1, "Input Five")
        SettingsWindow.four2_value = fs.FloatSpin(self.pnl, -1, min_val=-.9999, max_val=1.0, increment=.0001,
                                          value= .40,
                                          digits=4, agwStyle=fs.FS_CENTRE)
        SettingsWindow.four2_value.SetFormat("%f")
        self.fivetitle = wx.StaticText(self.pnl, -1, "Input Six",
                                             pos=(100, 110))  # shows FSK inputs only based on when FSK is clicked
        SettingsWindow.fiveval = fs.FloatSpin(self.pnl, -1, min_val=0, max_val=100, increment=1,
                                          value=30, pos=(100, 130),
                                          digits=4, agwStyle=fs.FS_CENTRE)
        self.sixtitle = wx.StaticText(self.pnl, -1, "Input Seven", pos=(200, 110))
        SettingsWindow.sixvalue = fs.FloatSpin(self.pnl, -1, min_val=-80, max_val=0, increment=10,
                                         value = -10, pos=(200, 130),
                                          digits=3, agwStyle=fs.FS_CENTRE)
        self.st = wx.StaticLine(self.pnl, -1, wx.Point(310, -1), size=(-1, 350), style=wx.LI_VERTICAL)
        self.add_config = wx.Button(self.pnl, -1, pos = (315, 40), size = (71, 50), label = "Add Config")
        self.load_config = wx.Button(self.pnl, -1, pos = (315,120), size = (71, 50), label = "Load Config")

        SettingsWindow.fiveval.Disable()
        SettingsWindow.sixvalue.Disable()
        SettingsWindow.donebtn = wx.Button(self.pnl, -1, 'Continue')
        self.shutdownbtn = wx.Button(self.pnl, -1, 'Cancel')

        options = ['One', 'Two']  # Lists options available for modulation

        # Create widgets





        self.onetitle = wx.StaticText(self.pnl, -1, 'Input One')  # Creates static title for input
        SettingsWindow.choiceone = wx.ComboBox(self.pnl, -1,  choices=options)
        self.Bind(wx.EVT_TEXT, self.onText, self.choiceone)
        self.fivetitle.Bind(wx.EVT_ENTER_WINDOW, self.onEnter) #bound for further info about why disabled
        self.sixtitle.Bind(wx.EVT_ENTER_WINDOW, self.onEnter)
        # Add widgets to sizer
        sizer_one.Add(self.onetitle, 0, border=20)  #adding variables to each sizer
        sizer_one.Add(SettingsWindow.choiceone, 0, border=20)
        sizer_two.Add(self.twotitle, 0, border=20)
        sizer_two.Add(SettingsWindow.twovalue, 0, border=20)
        sizer_three.Add(self.threetitle, 0, border=20)
        sizer_three.Add(SettingsWindow.threevalue, 0, border=20)
        sizer_four_l.Add(self.four1title, 0, border=20)
        sizer_four_l.Add(SettingsWindow.four1_value, 0, border=20)
        sizer_four_h.Add(self.four2title, 0, border=20)
        sizer_four_h.Add(SettingsWindow.four2_value, 0, border=20)
        sizer_five.Add(self.fivetitle, 0, border=20)
        sizer_five.Add(SettingsWindow.fiveval, 0, border=20)
        sizer_six.Add(self.sixtitle, 0, border=20)
        sizer_six.Add(SettingsWindow.sixvalue, 0, border=20)
        # linesizer.Add(self.st, 0, border = 20)

        # linesizer.Add(self.ln, 0, border = 20)
        gs.Add(sizer_one, 0, border=20) #adding adjusted sizers to the overall gridsizer
        gs.Add(sizer_two, 0, border=20)
        gs.Add(sizer_three, 0, border=20)
        # gs.Add(linesizer, 0, border = 20)
        g2s.Add(sizer_four_l, 0, border=20)
        g2s.Add(sizer_four_h, 0, border=20)

        g2s.Add(sizer_five, 0, border=20)
        g2s.Add(sizer_six, 0, border=20)
        g3s.Add(self.donebtn, 0, border=20)
        g3s.Add(self.shutdownbtn, 0, border = 20)

        # g3s.Add(linesizer, 0, border=20)

        sizer.Add(gs, 0, wx.ALIGN_CENTER | wx.ALL, border=5) # adding gridsizer to specific layout within window
        sizer.Add(g2s, 0, wx.ALIGN_CENTER | wx.ALL, border=5)
        sizer.Add(g3s, 0, wx.ALIGN_CENTER | wx.ALL, border = 5)



        self.shutdownbtn.Bind(wx.EVT_BUTTON, self.shutdown)
        self.Bind(wx.EVT_BUTTON, self.onLoad, self.load_config)
        self.Bind(wx.EVT_BUTTON, self.onAdd, self.add_config)
        self.Bind(wx.EVT_BUTTON, self.OnDone, self.donebtn)

        # Sizer is fit to panel
        self.pnl.SetSizer(sizer)


    def info_dialog(self, e): # Displays Config File Dialog
        info_dial = InfoDialog(self)
        info_dial.Show()
    def onEnter(self, e): # Displays Further Info About Widget
        e.GetEventObject().SetToolTip("Only Applicable to InputOne: Two")

    def onText(self, e): # Enables/Disables certain widgets.

        s = e.GetEventObject()


        if s.GetValue() == 'Two':

            SettingsWindow.fiveval.Enable()
            SettingsWindow.sixvalue.Enable()
            SettingsWindow.four1_value.SetValue(-.0002) # defaults values for threshold to better ones for FSK
            SettingsWindow.four2_value.SetValue(.0003)
            SettingsWindow.fiveval.SetValue(25.000)
            SettingsWindow.sixvalue.SetValue(-40.000)
        else:
            SettingsWindow.fiveval.Disable()
            SettingsWindow.sixvalue.Disable()
            SettingsWindow.four1_value.SetValue(.1000)
            SettingsWindow.four2_value.SetValue(.1500)
            SettingsWindow.fiveval.SetValue(0)
            SettingsWindow.sixvalue.SetValue(0)

    def onLoad(self, e): # Calls grid dialog
        dialog = GRDatabase(self)
        dialog.Show()
    def onAdd(self, e): # Checks for user input in order to be able to implement search feature
        if SettingsWindow.choiceone.IsTextEmpty() == True:
            self.SetStatusText("Select Modulation")
            return
        else:
            self.SetStatusText("")
            try:
                dialog = wx.TextEntryDialog(self.pnl, "Input Name:", value="", caption="Assign Name To Configuration",
                                            style=wx.TextEntryDialogStyle ^ wx.CENTER)

                if dialog.ShowModal() == wx.ID_OK:
                    if dialog.GetValue() == "":
                        wx.MessageBox("Configuration must have name")
                        return
                    else:
                        self.SetStatusText("Configuration for %s has been added to database" %dialog.GetValue())
                        pass
                else:
                    return

            finally:
                # explicitly cause the dialog to destroy itself
                dialog.Destroy()
            config_name = dialog.GetValue()


            # else:
            #     pass

        cnn = connect()
        cur = cnn.cursor()
        cur.execute("SELECT * FROM Configuration ORDER BY id DESC LIMIT 1")
        rows = cur.fetchone()
        cnn.close()
        try:
            prev_id_val = rows[0]
        except TypeError:
            prev_id_val = 0 # In case adding first val in db
        input = GRConfig(prev_id_val + 1, config_name, SettingsWindow.choiceone.GetStringSelection(), SettingsWindow.twovalue.GetValue(),
                             SettingsWindow.threevalue.GetValue(), SettingsWindow.four1_value.GetValue(),
                             SettingsWindow.four2_value.GetValue(), SettingsWindow.fiveval.GetValue(),
                             SettingsWindow.sixvalue.GetValue())
        session.add(input)
        session.commit()


    def shutdown(self, e):
        sys.exit(0) # exits out of entire program
    def OnDone(self, event):
        if SettingsWindow.choiceone.IsTextEmpty()== True:
            self.SetStatusText("Input One required")
            return
        else:
            self.SetStatusText("")
            print "dialog closed."
            self.Close()

if __name__ == '__main__':
    app = wx.App()
    settings_for_val = SettingsWindow(None)
    settings_for_val.Show()
    app.MainLoop()


