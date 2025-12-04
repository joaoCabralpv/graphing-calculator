import dearpygui.dearpygui as dpg
from ParseExprssion import solve


dpg.create_context()

def scientific_mode():
    #current_window=current_window
    dpg.hide_item(plot)
    dpg.show_item(scientific)
    dpg.set_primary_window(scientific, True)
    current_window=scientific

def plot_mode():
    dpg.hide_item(scientific)
    dpg.show_item(plot)
    dpg.set_primary_window(plot, True)
    current_window=plot



with dpg.window(tag="Scientific") as scientific:
    with dpg.menu_bar(label="Menu"):
        dpg.add_button(label="Scientific",callback=scientific_mode)
        dpg.add_button(label="Plot",callback=plot_mode)

    expression = dpg.add_input_text(tag="input", default_value="")

with dpg.window(tag="Plot") as plot:

    with dpg.menu_bar(label="Menu"):
        dpg.add_button(label="Scientific",callback=scientific_mode)
        dpg.add_button(label="Plot",callback=plot_mode)
    
    with dpg.child_window(resizable_x=True):
        expression=dpg.add_input_text()

    expression=dpg.add_input_text()
    dpg.add_text("plot")

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
    if dpg.is_item_focused(expression) and dpg.is_key_pressed(dpg.mvKey_Return):
        result=(solve(dpg.get_value(expression)))
        with dpg.group(horizontal=True,parent=scientific,before="input"):
            dpg.add_text(str(dpg.get_value(expression))+str(result))
            dpg.set_value(expression,"")

        #dpg.add_text(solve(dpg.get_value(expression)),parent=main,before="input")


    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()