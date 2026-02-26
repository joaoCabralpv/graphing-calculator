import dearpygui.dearpygui as dpg
from ParseExprssion import *
from Plot import *
from math import floor,ceil

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
    

# plot data
x_list = []
y_list = []


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
                dpg.add_plot_axis(dpg.mvXAxis, label="x",tag="x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

                # series belong to a y axis
                dpg.add_line_series(x_list, y_list, parent="y_axis",tag="plot1")

    dpg.add_input_text(parent="functions",tag="function_expression")

    #expression=dpg.add_input_text()
    #dpg.add_text("plot")

dpg.hide_item(plot)

current_window=scientific
dpg.create_viewport(title='Calculator', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Scientific", True)
dpg.show_style_editor()


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
        
    elif current_window == plot:
        input=dpg.get_value("function_expression")
        f,var = create_rpn_stack_for_function(input,"x")
        x_list=[]
        y_list=[]
        x_min,x_max=dpg.get_axis_limits("x_axis")
        #print(dpg.get_axis_limits("x_axis"))
        try:
            for x in range(floor(x_min*100),ceil(x_max*100)):
                #print(1)
                x/=100
                try:
                    var["x"].represented.set_value(x)
                except:
                    pass
                x_list.append(x)
                y_list.append(f())
            #print(x_list)
            #print(y_list)
            dpg.set_value("plot1",[x_list, y_list])
        except:
            print(input)

            


        #dpg.add_text(solve(dpg.get_value(expression)),parent=main,before="input")


    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()