import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


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
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Human Machine Interface", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        

        # Create the graph figure and axes
        self.graph_figure = plt.figure(figsize=(8, 6))
        self.graph_axes = self.graph_figure.add_subplot(111)

        # Generate sample data for the graph (replace with your own data)
        time = [1, 2, 3, 4, 5]
        dp = [10, 20, 15, 25, 18]

        # Plot the DP against time
        self.graph_axes.plot(time, dp)

        # Set the labels and title for the graph
        self.graph_axes.set_xlabel('Time')
        self.graph_axes.set_ylabel('DP')
        self.graph_axes.set_title(label='The effect of Ferric Chloride & Flow on DP', loc='center', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        
        # Display the graph within the app's grid layout
        self.graph_canvas = FigureCanvasTkAgg(self.graph_figure, master=self)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")


        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, bg_color="gray10", border_width=2, border_color="gray10", corner_radius=10)
        self.slider_progressbar_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        #self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(5, weight=1)

        self.controls_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="CONTROLS", anchor="n", font=("Arial", 14, "bold"), bg_color='transparent')
        self.controls_label.grid(row=0, column=1, padx=50, pady=(10, 0))
        

        #Slider 1 is for Ferric Chloride
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_1.grid(row=1, column=0, rowspan=5, padx=(0,10), pady=(10, 10), sticky="ns")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_1.grid(row=1, column=0, rowspan=5, padx=(100, 0), pady=(10, 10), sticky="ns")
        self.controls1_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Ferric Chloride", anchor="s", font=("Arial", 14, "bold"), bg_color='transparent')
        self.controls1_label.grid(row=6, column=0, padx=(30,0), pady=(10, 10))

        #Slider 2 is for Flow
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=1, column=2, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_2.grid(row=1, column=3, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")
        self.controls2_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Flow", anchor="s", font=("Arial", 14, "bold"), bg_color='transparent')
        self.controls2_label.grid(row=6, column=2, padx=(50,0), pady=(10, 10))

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Input Logs")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.log_entries = [
        ("Flow", "Ferric Chloride", "DP"),
        (10, 5, 50),
        (15, 7, 55),
        (12, 6, 52)
        ]
        for i, log_entry in enumerate(self.log_entries):
            for j, value in enumerate(log_entry):
                log_label = customtkinter.CTkLabel(self.scrollable_frame, text=str(value))
                log_label.grid(row=i, column=j, padx=10, pady=(0, 10))
        
        self.appearance_mode_optionemenu.set("System")
        
        self.slider_1.configure(command=self.update_graph)
        self.slider_2.configure(command=self.update_graph)
        # Create the clarifier widget
        self.clarifier_frame = customtkinter.CTkFrame(self, bg_color="white", border_width=2, border_color="gray40")
        self.clarifier_frame.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.clarifier_label = customtkinter.CTkLabel(
            self.clarifier_frame,
            text="Clarifier",
            anchor="n",
            font=("Arial", 14, "bold"),
            bg_color='transparent',
        )
        self.clarifier_label.grid(row=0, column=0, padx=50, pady=(10, 0))

        # Add the clarifier content (e.g., text, images, etc.) as needed
        

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def update_graph(self, value):

        self.scrollable_frame.clear_frame()

        # Get the values from the sliders
        slider1_value = self.slider_1.get()
        slider2_value = self.slider_2.get()

        # Update the graph data with the new values THIS IS WHERE THE INPUT FROM THE NEURAL NETWORK WILL GO
        time = [1, 2, 3, 4, 5]
        dp = [10 * slider1_value, 20 * slider2_value, 15 * slider1_value, 25 * slider2_value, 18 * slider1_value]

        # Update the log entries
        self.log_entries.append((slider1_value, slider2_value, dp[-1]))


        


        for i, log_entry in enumerate(self.log_entries):
            for j, value in enumerate(log_entry):
                log_label = customtkinter.CTkLabel(self.scrollable_frame, text=str(value))
                log_label.grid(row=i, column=j, padx=10, pady=(0, 10))
        

        # Clear the previous graph and plot the updated data
        self.graph_axes.clear()
        self.graph_axes.plot(time, dp)

        # Set the labels and title for the graph
        self.graph_axes.set_xlabel('Time')
        self.graph_axes.set_ylabel('DP')
        self.graph_axes.set_title(label='The effect of Ferric Chloride & Flow on DP', loc='center', fontdict={'fontsize': 10, 'fontweight': 'bold'})

        # Redraw the graph canvas
        self.graph_canvas.draw()


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
