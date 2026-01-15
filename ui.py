import dearpygui.dearpygui as dpg
from ParseExprssion import solve
from Plot import *
from math import sin

dpg.create_context()

current_window=None
def scientific_mode():
    #current_window=current_window
    print(1)
    dpg.hide_item(plot)
    dpg.show_item(scientific)
    dpg.set_primary_window(scientific, True)
    global current_window
    current_window=scientific

def plot_mode():
    print(2)
    dpg.hide_item(scientific)
    dpg.show_item(plot)
    dpg.set_primary_window(plot, True)
    global current_window
    current_window=plot



with dpg.window(tag="Scientific") as scientific:
    with dpg.menu_bar(label="Menu"):
        dpg.add_button(label="Scientific",callback=scientific_mode)
        dpg.add_button(label="Plot",callback=plot_mode)

    expression = dpg.add_input_text(tag="input", default_value="")
    print(1)
    print(expression)
    

# creating data
sindatax = []
sindatay = []
for i in range(0, 500):
    sindatax.append(i / 1000)
    sindatay.append(0.5 + 0.5 * sin(50 * i / 1000))

with dpg.window(tag="Plot") as plot:

    with dpg.menu_bar(label="Menu"):
        dpg.add_button(label="Scientific",callback=scientific_mode)
        dpg.add_button(label="Plot",callback=plot_mode)

    with dpg.group(horizontal=True):
        
        with dpg.child_window(tag="functions",resizable_x=True):
            pass
            #expression=dpg.add_input_text()

        dpg.add_same_line()
        with dpg.child_window(tag="plotwidow",resizable_x=True):
            with dpg.plot(label="Line Series",width=-1,height=-1):
                
                # optionally create legend
                dpg.add_plot_legend()

                # REQUIRED: create x and y axes
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

                # series belong to a y axis
                dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="y_axis")

    dpg.add_input_text(parent="functions")

    #expression=dpg.add_input_text()
    #dpg.add_text("plot")

dpg.hide_item(plot)

current_window=scientific
dpg.create_viewport(title='Calculator', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Scientific", True)


while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    #print(expression)
    #print(dpg.get_value(expression))
    if current_window == scientific and dpg.is_key_pressed(dpg.mvKey_Return):
        #print("input")
        result=(solve(dpg.get_value("input")))
        with dpg.group(horizontal=True,parent=scientific,before="input"):
            dpg.add_text(str(dpg.get_value("input"))+"="+str(result))
            dpg.set_value("input","")

        #dpg.add_text(solve(dpg.get_value(expression)),parent=main,before="input")


    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()