import PySimpleGUI as GUI

GUI.theme("DarkAmber")

layout = [[GUI.Text('Persistent window')],      
          [GUI.Input(key='-IN-')],      
          [GUI.Button('Read'), GUI.Exit()]]

def start():
    
    window = GUI.Window('Window that stays open', layout)  
    
    