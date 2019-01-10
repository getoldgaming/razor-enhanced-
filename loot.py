#===================================================#
#               Chest Content Viewer                #
#===================================================#
#                                                   #
#   Author: CookieLover                             #
#   Release Date: 10/05/2017                        #
#                                                   #
#===================================================#
#                                                   #
#   What you need:                                  #
#   - a container to ransack                        #
#                                                   #
#   Info:                                           #
#   - you can move the selected item into your      #
#     backpack by pressing Get                      #
#   - upon creating the list a file will be saved   #
#     in your Razor Enhanced main folder named      #
#     chest_*.txt with * being the current date     #
#     and time to avoid overwriting                 #
#                                                   #
#===================================================#

import clr, time, thread

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Data')

import System
from System.Collections.Generic import List
from System.Drawing import Point, Color, Size
from System.Windows.Forms import (Application, Button, Form, BorderStyle, 
    Label, FlatStyle, DataGridView, DataGridViewAutoSizeColumnsMode,
    DataGridViewSelectionMode, DataGridViewEditMode, CheckBox)
from System.Data import DataTable

class Content(System.IComparable, System.IConvertible):
    ID = 0
    name = ''
    props = ''
    
    def __init__(self, i, n, p):
        self.ID = i
        self.name = n
        self.props = p
        
class ChestForm(Form):
    CurVer = '1.0.1'
    ScriptName = 'Chest Content Viewer'
    Contents = []
    
    def __init__(self, contents):
        self.Contents = contents
        
        self.BackColor = Color.FromArgb(25,25,25)
        self.ForeColor = Color.FromArgb(231,231,231)
        self.Size = Size(500, 400)
        self.Text = '{0} - v{1}'.format(self.ScriptName, self.CurVer)
                
        self.DataGridSetup()
        
        self.cbHide = CheckBox()
        self.cbHide.Text = 'Hide'
        self.cbHide.Checked = True
        self.cbHide.BackColor = Color.FromArgb(25,25,25)
        self.cbHide.Location = Point(342, 326)
        self.cbHide.Size = Size(50, 30)
        
        self.btnGet = Button()
        self.btnGet.Text = 'Get'
        self.btnGet.BackColor = Color.FromArgb(50,50,50)
        self.btnGet.Location = Point(422, 324)
        self.btnGet.Size = Size(50, 30)
        self.btnGet.FlatStyle = FlatStyle.Flat
        self.btnGet.FlatAppearance.BorderSize = 1
        self.btnGet.Click += self.btnGetPressed
        
        self.Controls.Add(self.DataGrid)
        self.Controls.Add(self.cbHide)
        self.Controls.Add(self.btnGet)
        
        #self.DataGrid.Columns(0).Visible = False
           
    def DataGridSetup(self):
        self.DataGrid = DataGridView()
        self.DataGrid.RowHeadersVisible = False
        self.DataGrid.MultiSelect = False
        self.DataGrid.SelectionMode = DataGridViewSelectionMode.FullRowSelect
        self.DataGrid.BackgroundColor = Color.FromArgb(25,25,25)
        self.DataGrid.RowsDefaultCellStyle.BackColor = Color.Silver
        self.DataGrid.AlternatingRowsDefaultCellStyle.BackColor = Color.Gainsboro
        self.DataGrid.ForeColor = Color.FromArgb(25,25,25)
        self.DataGrid.Location = Point(12, 12)
        self.DataGrid.Size = Size(460, 306)
        self.DataGrid.DataSource = self.Data()
        self.DataGrid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells
        self.DataGrid.EditMode = DataGridViewEditMode.EditProgrammatically
        self.DataGrid.BorderStyle = BorderStyle.None
        
    def btnGetPressed(self, sender, args):
        row = self.DataGrid.SelectedCells[0].RowIndex
        
        if row == -1:
            Misc.SendMessage('{0}: No row selected.'.format(self.ScriptName), 33)
            return
            
        col = self.DataGrid.SelectedCells[0].ColumnIndex
        serial = self.DataGrid.Rows[row].Cells[col].Value
        self.DeleteRow(serial)
        Items.Move(int(serial, 0), Player.Backpack, 0)
        if self.cbHide.Checked:
            Misc.Pause(300)
            Player.UseSkill('Hiding')
            t = thread.start_new_thread(self.HidingTimer, (1,))
            

    def DeleteRow(self, serial):
        for r in xrange(self.DataGrid.DataSource.Rows.Count):
            row = self.DataGrid.DataSource.Rows[r]
            if row['ID'] == serial:
                self.DataGrid.DataSource.Rows.Remove(row)
                return        
    
    def HidingTimer(self, num):
        for s in xrange(11):
            Player.HeadMessage(55,'Hiding Timer: {0}s'.format(11-s))
            Misc.Pause(1000)
            
    def Data(self):
        data = DataTable()
        data.Columns.Add('ID', clr.GetClrType(str))
        data.Columns.Add('Name', clr.GetClrType(str))
        data.Columns.Add('Props', clr.GetClrType(str))
        
        for content in self.Contents:
            data.Rows.Add(hex(content.ID), content.name, content.props)
           
        return data

contents = []
filetext = []

filename = 'chest_{0}.txt'.format(time.strftime('%y%m%d%H%M%S'))

Misc.SendMessage('Target a container to see its contents.', 76)       
contid = Target.PromptTarget()
if contid > -1:
    cont = Items.FindBySerial(contid)
    Items.WaitForContents(cont, 8000)
    Misc.Pause(500)

    for i in cont.Contains:
        Items.WaitForProps(i, 8000)
        plist = list(Items.GetPropStringList(i))
        props = '; '.join(p.replace('<b>','').replace('</b>','') for p in plist[1:])
        contents.append(Content(i.Serial, plist[0], props))
        filetext.append('{0} ({1})\n\n{2}\n'.format(plist[0], hex(i.Serial), props.replace('; ','\n')))

    if contents == []:
        Misc.SendMessage('It is either empty or not a container at all.', 33)
    else:
        with open(filename, 'w') as f:
            f.write('\n'.join(t for t in filetext))
        form = ChestForm(contents)
        Application.Run(form)
    
else:
    Misc.SendMessage('No container was targeted.', 33)
    

