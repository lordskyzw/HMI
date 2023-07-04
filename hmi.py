import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from tensorflow.keras.models import load_model 
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import cv2
from PIL import Image, ImageTk


# Load the saved model
neuralnet = load_model('neuralnet.h5')

data = pd.read_excel('lab/pretreatment.xlsx', sheet_name='Sheet2')

# Split the data into predictors (X) and target variable (y)
X = data[['Turbidity', 'Flow', 'Ferric']]
y = data['DP']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features to a specific range (e.g., between 0 and 1)
scaler = MinMaxScaler(feature_range=(0, 4), copy=True)
# Fit the scaler to the training data
scaler.fit(X_train)

# Transform the training and testing data using the fitted scaler
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# scaler.feature_names = ['Turbidity', 'Flow', 'Ferric']  # Specify your actual feature names


# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)


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

        # create stop button
        self.stop_button = customtkinter.CTkButton(self.sidebar_frame, text="Stop", command=self.stop_button_event)
        self.stop_button.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.is_paused = False
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        

        # Create the graph figure and axes
        self.graph_figure = plt.figure(figsize=(8, 6))
        self.graph_axes = self.graph_figure.add_subplot(111)

        # Generate sample data for the graph (replace with your own data)
        self.dp = [0]
        self.time = list(range(1))
        

        # Plot the self.DP against self.time
        self.graph_axes.plot(self.time, self.dp)

        # Set the labels and title for the graph
        self.line, = self.graph_axes.plot(self.time, self.dp)
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
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical", from_=10, to=50, number_of_steps=80)
        self.slider_1.grid(row=1, column=0, rowspan=5, padx=(0,10), pady=(10, 10), sticky="ns")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_1.grid(row=1, column=0, rowspan=5, padx=(100, 0), pady=(10, 10), sticky="ns")
        self.controls1_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Ferric Chloride", anchor="s", font=("Arial", 14, "bold"), bg_color='transparent')
        self.controls1_label.grid(row=6, column=0, padx=(30,0), pady=(10, 10))

        #Slider 2 is for Flow
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical", from_=100, to=400, number_of_steps=300)
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

        # Load the video
        self.video = cv2.VideoCapture("assets/loop.mp4")
        self.is_playing = True
        _, self.frame = self.video.read()

        # Create a label to display the video frames
        self.video_label = customtkinter.CTkLabel(self.clarifier_frame)
        self.video_label.grid(row=0, column=0)

        # Start the video playback
        self.play_video()

    # def play_video(self):
    #     _, self.frame = self.video.read()
    #     if self.frame is not None:
    #         # Convert the video frame to RGB format
    #         frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    #         # Resize the frame to fit the clarifier frame
    #         frame_resized = cv2.resize(frame_rgb, (self.clarifier_frame.winfo_width(), self.clarifier_frame.winfo_height()))

    #         # Convert the resized frame to a PIL Image
    #         image = Image.fromarray(frame_resized)

    #         # Convert the PIL Image to a Tkinter PhotoImage
    #         photo_image = ImageTk.PhotoImage(image)
    #         # Create a CTkImage from the PhotoImage
    #         ctk_image = CTkImage.from_photo_image(photo_image)

    #         # Update the video label with the new frame
    #         self.video_label.configure(image=ctk_image)
    #         self.video_label.image = ctk_image

    #     else:
    #         # Reset the video capture to the beginning
    #         self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    #     # Schedule the next frame update
    #     self.after(30, self.play_video)

    def play_video(self):
        ret, frame = self.video.read()
        if ret:
            # Convert the frame to PIL Image format
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Resize the image to fit the label
            image = image.resize((400, 300))

            # Create a CTkImage from the PIL Image
            ctk_image = customtkinter.CTkImage(image)

            # Update the video label with the new frame
            self.video_label.configure(image=ctk_image)
            self.video_label.image = ctk_image

        # if self.is_playing:
        #     self.after(30, self.play_video)


        self.update_graph()

    #def start_time_simulation(self):
         
    def stop_button_event(self):
        # Toggle the value of the is_paused flag variable
        self.is_paused = not self.is_paused

        # Update the text of the stop button based on the current state
        if self.is_paused:
            self.stop_button.configure(text="Continue")
        else:
            self.stop_button.configure(text="Stop")
            if not self.is_paused:
                self.update_graph()
                self.play_video()

            
    def update_graph(self, _=None):
        
        '''This should always increase the time and then update the graph per second'''
        if self.is_paused:
            return

        self.scrollable_frame.clear_frame()

        # Get the values from the sliders
        slider1_value = self.slider_1.get()
        slider2_value = self.slider_2.get()

        # Create an array with the slider values
        input_values = np.array([[slider1_value, slider2_value, 0]])  # Assuming the third input feature is 0

        # Scale the input values using the same scaler used during training
        input_values_scaled = scaler.transform(input_values)

        # Perform prediction using the loaded neural network model
        prediction = neuralnet.predict(input_values_scaled)

        # Update the graph data with the new prediction
        self.dp.append(prediction[0][0])
        self.time.append(self.time[-1] + 1)  # Increment the time value

        # Update the log entries
        self.log_entries.append((slider1_value, slider2_value, self.dp[-1]))
        for i, log_entry in enumerate(self.log_entries):
            for j, value in enumerate(log_entry):
                log_label = customtkinter.CTkLabel(self.scrollable_frame, text=str(value))
                log_label.grid(row=i, column=j, padx=10, pady=(0, 10))

        # Clear the previous graph and plot the updated data
        self.graph_axes.clear()
        self.graph_axes.plot(self.time, self.dp)
        self.graph_axes.set_xlabel('Time')
        self.graph_axes.set_ylabel('DP')
        self.line.set_data(self.time, self.dp)  # Update the line data with the updated dp and time
        self.graph_axes.set_xlim(0, len(self.dp))
        self.graph_axes.set_ylim(0, max(self.dp) + 1)
        self.graph_axes.set_title(label='The effect of Ferric Chloride & Flow on DP', loc='center', fontdict={'fontsize': 10, 'fontweight': 'bold'})

        # Redraw the graph canvas
        self.graph_canvas.draw()
        self.after(2000, self.update_graph)



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def sidebar_button_event(self):
        print("sidebar_button click")

    

        


if __name__ == "__main__":
    app = App()
    app.mainloop()
