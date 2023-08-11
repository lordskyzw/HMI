import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation
import customtkinter
from newton import *
import numpy as np


customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


def hide_label(label):
    label.destroy()


# Create a Tkinter window
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("Prediction Chart")

        # Create a matplotlib figure and axis
        self.figure, self.ax = plt.subplots()

        # Set axis labels and title
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value")
        self.ax.set_title("DP Accumulation Prediction")

        # Create a canvas to embed the matplotlib figure in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Start dynamic growth animation
        self.dynamic_growth_animation()

    def dynamic_growth_animation(self):
        control_growth_rate = np.log(8) / 250
        dynamic_growth_rate = np.log(8) / 350
        frames = 350  # Number of frames for the animation
        update_x_values = np.linspace(
            0, 350, frames
        )  # Start animation from 0 seconds, up to 350 seconds

        def update(frame):
            control_y_values = np.exp(control_growth_rate * update_x_values[:frame])
            dynamic_y_values = np.exp(dynamic_growth_rate * update_x_values[:frame])

            # Clear previous data
            self.ax.clear()

            # Plot control growth curve
            self.ax.plot(
                update_x_values[:frame], control_y_values, label="Control Growth"
            )

            # Plot dynamic growth curve
            self.ax.plot(
                update_x_values[:frame], dynamic_y_values, label="Optimized Growth"
            )

            # Set axis limits and labels
            self.ax.set_xlim(0, 500)
            self.ax.set_ylim(0, 10)
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Accumulated DP")
            self.ax.set_title("DP accumulation Prediction")
            self.ax.legend()

        ani = animation.FuncAnimation(
            self.figure, update, frames=frames, interval=100, blit=False
        )
        self.canvas.draw()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Human Machine Interface")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Human Machine Interface",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.button_1 = customtkinter.CTkButton(
            self, text="open Chart", command=self.open_toplevel
        )
        self.button_1.grid(padx=20, pady=20)

        self.toplevel_window = None
        # apperance mode and the widgets
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.copilot_flag = customtkinter.StringVar(value="off")

        self.copilot_switch = customtkinter.CTkSwitch(
            self.sidebar_frame,
            text="Predictive Control",
            command=self.copilot,
            variable=self.copilot_flag,
            progress_color="green",
            onvalue="on",
            offvalue="off",
        )
        self.copilot_switch.grid(row=1, column=0, padx=20, pady=(10, 0))

        # create stop button
        self.stop_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Stop", command=self.stop_button_event
        )
        self.stop_button.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.is_paused = False

        ############################################################ INITIAL GRAPH ####################################################
        self.graph_figure = plt.figure(figsize=(8, 7))
        self.graph_axes = self.graph_figure.add_subplot(111)
        # Generate sample data for the graph
        self.dp = [0]
        self.time = list(range(1))
        self.last_input = {"flow": None, "ferric_chloride": None}

        # Plot the self.DP against self.time
        self.graph_axes.plot(self.time, self.dp)
        # Set the labels and title for the graph
        (self.line,) = self.graph_axes.plot(self.time, self.dp)
        self.graph_axes.set_xlabel("Time")
        self.graph_axes.set_ylabel("DP")
        self.graph_axes.set_title(
            label="The effect of Ferric Chloride & Flow on DP",
            loc="center",
            fontdict={"fontsize": 10, "fontweight": "bold"},
        )
        # Display the graph within the app's grid layout
        self.graph_canvas = FigureCanvasTkAgg(self.graph_figure, master=self)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().grid(
            row=0, column=1, rowspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )
        ############################################################ END OF INITIAL GRAPH ###############################################################

        ################################################## SLIDERS CONFIGURATION #######################################################
        ################################### Slider 1 is for Ferric Chloride ###############################################
        # create slider_progressbar_frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(
            self,
            bg_color="gray10",
            border_width=2,
            border_color="gray10",
            corner_radius=0,
        )
        self.slider_progressbar_frame.grid(
            row=3, rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        self.slider_progressbar_frame.grid_columnconfigure((0, 1), weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(5, weight=1)

        self.slider_label = customtkinter.CTkLabel(
            master=self.slider_progressbar_frame,
            text="Manual Control",
        )
        self.slider_label.grid(row=0, padx=(80, 0), pady=(10, 0), sticky="n")

        self.slider_1 = customtkinter.CTkSlider(
            self.slider_progressbar_frame,
            orientation="vertical",
            from_=10,
            to=50,
            number_of_steps=80,
        )
        self.slider_1.grid(
            row=1, column=0, rowspan=5, padx=(0, 10), pady=(10, 10), sticky="ns"
        )
        self.controls1_label = customtkinter.CTkLabel(
            self.slider_progressbar_frame,
            text="Ferric Chloride",
            anchor="s",
            font=("Arial", 14, "bold"),
            bg_color="transparent",
        )
        self.controls1_label.grid(row=6, column=0, padx=(10, 10), pady=(0, 10))
        ########################################### Slider 2 is for Flow     ########################################################
        self.slider_2 = customtkinter.CTkSlider(
            self.slider_progressbar_frame,
            orientation="vertical",
            from_=100,
            to=400,
            number_of_steps=300,
        )
        self.slider_2.grid(
            row=1, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns"
        )
        self.controls2_label = customtkinter.CTkLabel(
            self.slider_progressbar_frame,
            text="Flow",
            anchor="s",
            font=("Arial", 14, "bold"),
            bg_color="transparent",
        )
        self.controls2_label.grid(row=6, column=1, padx=(10, 10), pady=(0, 10))
        self.slider_1.configure(command=self.slider_command)
        self.slider_2.configure(command=self.slider_command)

        self.system_response_frame = customtkinter.CTkFrame(
            self,
            bg_color="gray10",
            border_width=2,
            border_color="gray10",
            corner_radius=0,
        )
        self.system_response_frame.grid(
            row=3, rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        self.system_response_frame.grid_columnconfigure((0, 1), weight=1)
        self.system_response_frame.grid_rowconfigure(5, weight=1)

        self.system_response_slider_label = customtkinter.CTkLabel(
            master=self.system_response_frame,
            text="System Response",
        )
        self.system_response_slider_label.grid(
            row=0, padx=(90, 10), pady=(10, 0), sticky="n"
        )
        self.system_response_slider_1 = customtkinter.CTkSlider(
            self.system_response_frame,
            orientation="vertical",
            from_=10,
            to=50,
            number_of_steps=80,
        )
        self.system_response_slider_2 = customtkinter.CTkSlider(
            self.system_response_frame,
            orientation="vertical",
            from_=100,
            to=400,
            number_of_steps=300,
        )

        self.system_response_frame.grid(row=3, column=2, padx=(0, 0))
        self.system_response_slider_1_label = customtkinter.CTkLabel(
            self.system_response_frame,
            text="Ferric Chloride",
            anchor="s",
            font=("Arial", 14, "bold"),
            bg_color="transparent",
        )
        self.system_response_slider_1_label.grid(
            row=6, column=0, padx=(10, 0), pady=(0, 10)
        )
        self.system_response_slider_2_label = customtkinter.CTkLabel(
            self.system_response_frame,
            text="Flow",
            anchor="s",
            font=("Arial", 14, "bold"),
            bg_color="transparent",
        )
        self.system_response_slider_2_label.grid(
            row=6, column=1, padx=(0, 40), pady=(0, 10)
        )
        self.system_response_slider_1.grid(row=1, column=0, padx=0)
        self.system_response_slider_2.grid(row=1, column=1, padx=(0, 40))
        ###################################################### END OF SLIDER CONFIGURATION ############################################

        self.run()

    def open_toplevel(self):
        if self.copilot_flag.get() == "on":
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(
                    self
                )  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it
        else:
            print("Predictive Control mode is not enabled.")

    # CREATE THE MAINLOOP FUNCTION WHICH CHECKS IF PAUSED AND THEN CHECKS IF COPILOT IS ON OR OFF BEFORE CHOOSING WHICH METHOD TO CALL
    def run(self):
        if self.is_paused:
            return
        else:
            if self.copilot_flag.get() == "on":
                self.predictive_control()
            elif self.copilot_flag.get() == "off":
                self.update_graph()

        self.after(2000, self.run)

    def copilot(self):
        if self.copilot_flag.get() == "on":
            optimizing_label = customtkinter.CTkLabel(
                self, text="AUTO OPTIMIZING", text_color="green"
            )
            optimizing_label.grid(row=0, column=2)
            self.after(2000, optimizing_label.destroy)
            print("switch toggled, current value: {}".format(self.copilot_flag.get()))
            print(
                "the last value for FERRIC CHLORIDE is:{}"
                + "the last value for FLOW is:{}".format(
                    self.last_input["ferric_chloride"], self.last_input["flow"]
                )
            )
            self.predictive_control()
        elif self.copilot_flag.get() == "off":
            white_label = customtkinter.CTkLabel(
                self, text="AUTO OPTIMIZING OFF", text_color="white"
            )
            white_label.grid(row=0, column=2)
            self.after(2000, white_label.destroy)
            print("switch toggled, current value: off")
            self.run()

    def stop_button_event(self):
        # Toggle the value of the is_paused flag variable
        self.is_paused = not self.is_paused

        # Update the text of the stop button based on the current state
        if self.is_paused:
            self.stop_button.configure(text="Continue")
        else:
            self.stop_button.configure(text="Stop")
            self.run()

    def slider_command(self, _=None):
        self.run()

    def slider1systemresponsecalc(self, slider2_value, normalized_turbidity):
        return

    def slider2systemresponsecalc(self, slider1_value, normalized_turbidity):
        return

    def predictive_control(self, _=None):
        """this enables the autopilot feature. When it is called, it:
        1)implement the system response sliders
        2) checks for the changed slider
        3) compansate for that change by regulating the unchanged slider on the respective system response bar
        """
        if self.is_paused:
            return
        else:
            slider1_value = self.slider_1.get()
            slider2_value = self.slider_2.get()
            # find the changed slider
            if slider1_value != self.last_input["ferric_chloride"]:
                print("ferric chloride has changed")
                self.system_response_slider_1.set(output_value=slider1_value)
                # slider 1 has changed therefore compansate with slider 2
                slider2_system_response_value = flow_optimizer(
                    ferric_chloride=slider1_value
                )
                self.system_response_slider_2.set(slider2_system_response_value)
                self.last_input["ferric_chloride"] = slider1_value
                self.dp.append(1.5)
                self.time.append(self.time[-1] + 1)  # Increment the time value

                ####################################################### GRAPHING OPERATIONS ##################################################

                # Clear the previous graph and plot the updated data
                self.graph_axes.clear()
                self.graph_axes.plot(self.time, self.dp)
                self.graph_axes.set_xlabel("Time")
                self.graph_axes.set_ylabel("DP")
                self.line.set_data(
                    self.time, self.dp
                )  # Update the line data with the updated dp and time
                self.graph_axes.set_xlim(0, len(self.dp))
                self.graph_axes.set_ylim(0, max(self.dp) + 0.2)
                self.graph_axes.set_title(
                    label="The effect of Ferric Chloride & Flow on DP",
                    loc="center",
                    fontdict={"fontsize": 10, "fontweight": "bold"},
                )

                # Redraw the graph canvas
                self.graph_canvas.draw()
                self.run()

            elif slider2_value != self.last_input["flow"]:
                self.system_response_slider_2.set(output_value=slider2_value)
                print("flow has changed")
                # Flow - slider 2 has changed therefore compansate with Ferric - slider 1
                slider1_system_response_value = ferric_optimizer(flow=slider2_value)
                # slider1_system_response is a slider
                self.system_response_slider_1.set(slider1_system_response_value)
                self.last_input["flow"] = slider2_value
                self.dp.append(1.5)
                self.time.append(self.time[-1] + 1)

                ####################################################### GRAPHING OPERATIONS ######################################################################################################### GRAPHING OPERATIONS ##################################################

                # Clear the previous graph and plot the updated data
                self.graph_axes.clear()
                self.graph_axes.plot(self.time, self.dp)
                self.graph_axes.set_xlabel("Time")
                self.graph_axes.set_ylabel("DP")
                self.line.set_data(
                    self.time, self.dp
                )  # Update the line data with the updated dp and time
                self.graph_axes.set_xlim(0, len(self.dp))
                self.graph_axes.set_ylim(0, max(self.dp) + 0.2)
                self.graph_axes.set_title(
                    label="The effect of Ferric Chloride & Flow on DP",
                    loc="center",
                    fontdict={"fontsize": 10, "fontweight": "bold"},
                )

                # Redraw the graph canvas
                self.graph_canvas.draw()
                self.run()

            else:
                print("no change, therefore using optimum figures")
                slider1_value = self.slider_1.get()
                slider2_value = self.slider_2.get()
                self.last_input["flow"] = slider2_value
                self.last_input["ferric_chloride"] = slider1_value

                ################################# Updating the screens ###################################################################################################
                self.dp.append(1.5)
                self.time.append(self.time[-1] + 1)  # Increment the time value

                ####################################################### GRAPHING OPERATIONS ##################################################

                # Clear the previous graph and plot the updated data
                self.graph_axes.clear()
                self.graph_axes.plot(self.time, self.dp)
                self.graph_axes.set_xlabel("Time")
                self.graph_axes.set_ylabel("DP")
                self.line.set_data(
                    self.time, self.dp
                )  # Update the line data with the updated dp and time
                self.graph_axes.set_xlim(0, len(self.dp))
                self.graph_axes.set_ylim(0, max(self.dp) + 0.2)
                self.graph_axes.set_title(
                    label="The effect of Ferric Chloride & Flow on DP",
                    loc="center",
                    fontdict={"fontsize": 10, "fontweight": "bold"},
                )

                # Redraw the graph canvas
                self.graph_canvas.draw()

    def update_graph(self, _=None):
        """This should always increase the time and then update the graph per second"""
        if self.is_paused:
            return

        slider1_value = self.slider_1.get()
        slider2_value = self.slider_2.get()
        self.last_input["flow"] = slider2_value
        self.last_input["ferric_chloride"] = slider1_value

        ################# CALCULATING DIFFERENTIAL PRESSURE #################################################################################################
        prediction = round(
            main_equation(
                flow=slider2_value,
                ferric_chloride=slider1_value,
                turbidity=random_turbidity(0.6),
            ),
            3,
        )
        ################## END OF CALCULATING DIFFERENTIAL PRESSURE ############################################################################################

        ############################################################################################################################################
        ################################# Updating the screens ###################################################################################################
        self.dp.append(prediction)
        self.time.append(self.time[-1] + 1)  # Increment the time value

        ####################################################### GRAPHING OPERATIONS ##################################################

        # Clear the previous graph and plot the updated data
        self.graph_axes.clear()
        self.graph_axes.plot(self.time, self.dp)
        self.graph_axes.set_xlabel("Time")
        self.graph_axes.set_ylabel("DP")
        self.line.set_data(
            self.time, self.dp
        )  # Update the line data with the updated dp and time
        self.graph_axes.set_xlim(0, len(self.dp))
        self.graph_axes.set_ylim(0, max(self.dp) + 0.2)
        self.graph_axes.set_title(
            label="The effect of Ferric Chloride & Flow on DP",
            loc="center",
            fontdict={"fontsize": 10, "fontweight": "bold"},
        )

        # Redraw the graph canvas
        self.graph_canvas.draw()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
