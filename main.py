import dearpygui.dearpygui as dpg 
import serial
from stageControl import *
import numpy as np 
import matplotlib.pyplot as plt

dpg.create_context()
dpg.create_viewport(title='Main Context',width=900,height=600)
with dpg.font_registry():
    default_font = dpg.add_font('Montserrat-Regular.otf',20)
dpg.bind_font(default_font)
#set up units and stages:
unitlist =['fs','ps','um','mm','ct']
sunitlist=['fs/s','ps/s','um/s','mm/s','ct/s']
stages   =['t3ref','t13','t12','z']
devices = populatePorts()
z = np.zeros(1)
#set up a storage location for figures
#display a simple icon
dpg.set_viewport_small_icon("Icon.ico")
dpg.set_viewport_large_icon("Icon.ico")
dev = serial.Serial(baudrate=9600,timeout=1)
initialize_stageControl(dev)
#set up stage initialization window all callbacks in stageControl.py
with dpg.window(label='Stage Control Window',width=440,height=310,on_close=closeConnect):
    #setup control for stage initialization
    dpg.add_text('Stage Control')
    sstatus = dpg.add_text('Stage status:inactive')
    with dpg.group(horizontal=True):
        port = dpg.add_combo(devices,width=100,label='Select Device')
        dpg.add_button(label='connect device',callback=connectDevice,
                       user_data=port)
    #stage monitor
    with dpg.group(horizontal=True):
        stage=dpg.add_combo(stages,label='Stage',width=70,
                            default_value='t3ref')
        position = dpg.add_text('Current Position: Unknown')
    
        
    #translation control for stage positioning 
    with dpg.group(horizontal=True):    
        destination = dpg.add_input_double(label='',width=150)
        units = dpg.add_combo(unitlist,label='Destination',
                              width=70,default_value='fs')

       
    #unit setting 
    with dpg.group(horizontal=True): 
        speed = dpg.add_input_double(label='',default_value=1.5,
                               width=150)
        sunits = dpg.add_combo(sunitlist,label='Speed',
                               width=70,default_value='mm/s')
    
    #stage zero/position
    with dpg.group(horizontal=True):
        dpg.add_button(label='Zero Stage',callback=zeroStage,
                       user_data=[position,sstatus,stage])
        dpg.add_button(label='Get Position',callback=getPosition,
                       user_data=[position,sstatus,stage,units])
        
    #execute motion
    with dpg.group(horizontal=True):
        dpg.add_button(label='Move Stage',callback=moveStage,
                       user_data=[destination,position,stage,units,speed,sunits,sstatus])
        
with dpg.window(label='PicoHarpControl',width=440,height=310,on_close=closeConnect):
    #setup control for stage initialization
    dpg.add_text('Picoharp')
    pstatus = dpg.add_text('Picoharp status:inactive')
    with dpg.group(horizontal=True):
        port = dpg.add_combo(devices,width=100,label='Select Device')
        dpg.add_button(label='connect device',callback=connectDevice,
                       user_data=port)
    with dpg.group(horizontal=True):    
        binning = dpg.add_input_int(label='binning',width=150,default_value=0)#set bin subdivisions  
        offset  = dpg.add_input_int(label='measurement offset (ps)',width=150,default_value=0)#set bin subdivisions  
    
    with dpg.group(horizontal=True):    
        tacq         = dpg.add_input_int(label='measurement time (ms)',width=150,default_value=1000)#set bin subdivisions  
        syncDivider  = dpg.add_input_int(label='Sync division',width=150,default_value=1)#set bin subdivisions
    with dpg.group(horizontal=True):
        CFDZeroCross0    = dpg.add_input_int(label='measurement time (ms)',width=150,default_value=1)#set bin subdivisions  
        CFDLevel0  = dpg.add_input_int(label='measurement offset (ps)',width=150,default_value=0)#set bin subdivisions
        CFDZeroCross1 = 
        CFDLevel1  = 

      
#set up window for displaying plot 
with dpg.window(label="HFWM Data Monitor",pos=(0,310),width=680,height=700):
    x= np.linspace(-10,10)
    y= np.linspace(-10,10)
    X,Y = np.meshgrid(x,y)
    Z = X+Y
    fig,ax = plt.subplots(layout='compressed')
    neg = ax.imshow(Z,extent=[-10,10,-10,10])
    fig.colorbar(neg, ax=ax)
    ax.set_xlabel('stage b delay')
    ax.set_ylabel('stage a delay')
    fig.set_dpi(100)
    fig.set_figwidth(5.8)
    fig.set_figheight(5.8)
    fig.canvas.draw()
    data= np.frombuffer(fig.canvas.buffer_rgba(),dtype=np.uint8)
    width =580
    height=580

    print(np.shape(data))
    with dpg.texture_registry():
        texture_id = dpg.add_dynamic_texture(width, height, data/255)
    dpg.add_image(texture_id)
    pb =dpg.add_progress_bar(width=580)
    timemonitor =dpg.add_text(default_value="--.-- minutes complete, --.-- minutes remaining")
    
#HFWM set up window all info in hfwmSetup.py
with dpg.window(label="HFWM Setup",pos=(440,0),width=560,height=310):
    #select stages
    with dpg.group(horizontal=True):
        stagea = dpg.add_combo(stages,label='Select Stage a',
                               default_value='t3ref',width=100)
        spectrum = dpg.add_combo(['no','yes'],label='Collectspectrum',
                               default_value='no',width=100)
    #set stage speeds 
    with dpg.group(horizontal=True):
        speeda = dpg.add_input_double(label='',
                                      default_value=1.5, 
                                      width=150)
        sunita = dpg.add_combo(sunitlist,label='stage a speed',
                                width=70,default_value='mm/s')
        
    #set stage units 
    with dpg.group(horizontal= True): 
        speedb = dpg.add_input_double(label='',
                                      default_value=5.0,
                                      width=150)
        sunitb = dpg.add_combo(sunitlist,label='stage b speed', 
                               width=70,default_value='mm/s')
    #set stage start point 
    with dpg.group(horizontal= True): 
        starta = dpg.add_input_double(label='Start a',default_value=-1.2,
                                       width=150)

        enda = dpg.add_input_double(label='End a',
                                    default_value=1.2,
                                    width=150)
    #set stage end point
    with dpg.group(horizontal= True): 
        startb = dpg.add_input_double(label='Start b',default_value=-1.2,
                                       width=150)        
        endb = dpg.add_input_double(label='End b',
                                    default_value=1.2,
                                    width=150)
    #set stage units
    with dpg.group(horizontal= True): 
        unita = dpg.add_combo(unitlist,label='stage a units',
                               width=70,default_value='ps')
        unitb = dpg.add_combo(unitlist,label='stage b units', 
                               width=70,default_value='ps')

    #set stage increment
    with dpg.group(horizontal= True): 
        stepsa = dpg.add_input_int(label='steps stage a',
                                      default_value=25,
                                       width=150)
        stepsb = dpg.add_input_int(label='steps stage b',
                                      default_value=25,
                                       width=150)
    with dpg.group(horizontal=True):
        inttime = dpg.add_input_double(label='Integration time [s]',
                                default_value=.05,
                                width=150)
        logopt = dpg.add_radio_button(["line space","log space"], horizontal=True,default_value="line space")
    
    
    #run 
    zvalues=np.zeros(1)
    runpackage = [ stagea,spectrum, #[0,1]
                   speeda,speedb ,#[2,3]
                   sunita,sunitb ,#[4,5]
                   starta,startb ,#[6,7]
                   enda, endb,    #[8,9]
                   stepsa,stepsb, #[10,11]
                   unita,unitb,   #[12,13]
                   pb,texture_id, #[14,15]
                   zvalues,inttime,#[16,17]
                   timemonitor,logopt] #[18,19]
    dpg.add_file_dialog(
        directory_selector=True, show=False, callback=savefile, tag="file_dialog_id",
        cancel_callback=savecanceled, width=700 ,height=400)
    with dpg.group(horizontal=True):               
        dpg.add_button(label='Run',callback=runHFWM,
                       user_data=runpackage,width=100)
                    #,userdata=runpackage,callback=runHFWM)
        dpg.add_button(label='Savecollection',
                       callback=lambda:dpg.show_item('file_dialog_id'))

    

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
#dpg.set_primary_window(window=0,value=True)
dpg.start_dearpygui()
dpg.destroy_context()