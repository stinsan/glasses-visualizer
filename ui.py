import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from monodepth2.test_simple import test_simple
import os


def monodepthify(filename):
    """
    Runs the test_simple script from Monodepth using the
    mono+stereo_640x192 model.
    :param filename: The name of the image file.
    """
    test_simple(filename)


class UI:
    def __init__(self):
        """
        Initializes the user interface.
        """
        # Constants for application window size;
        self.WIDTH = 1024
        self. HEIGHT = 576

        self.root = tk.Tk()
        self.root.title('Glasses Visualizer')           # Application title.
        self.root.resizable(width=False, height=False)  # Not resizable.

        # Frame for the image output.
        self.image_frame = tk.Frame(self.root)
        self.image_frame.grid(column=0, row=0)

        # Frame for the options below the image output frame.
        self.options_frame = tk.Frame(self.root)
        self.options_frame.grid(column=0, row=1)

        # Create a green canvas in the image output frame with 5 padding.
        self.image_canvas = tk.Canvas(self.image_frame, bg='green', width=self.WIDTH, height=self.HEIGHT)
        self.image_canvas.pack(padx='5', pady='5')

        # Create an upload button that prompts the user to upload an image.
        self.upload_button = tk.Button(self.options_frame, text="Upload", fg="red", command=self._upload_image)
        self.upload_button.pack(padx='5', pady='5')

        self.root.mainloop()  # Draw the UI.

    def _upload_image(self):
        """
        Uploads an image, runs it through Monodepth, and outputs it onto the application.
        TODO: Make it output the blurred image, not just the depth map.
        :return:
        """
        global_filename = filedialog.askopenfilename()  # Ask the user to choose a picture,
        monodepthify(global_filename)                   # then run Monodepth on that picture.

        # Monodepth outputs the depth map image into the same directory of the original image.
        # The depth map image will be output with the file name "<original-image-name>_disp.jpeg".
        # We want to get this image and show it onto the image canvas.
        orig_image_filename = os.path.splitext(os.path.basename(global_filename))[0]
        depth_map_filename = '{}_disp.jpeg'.format(orig_image_filename)
        monodepth_output_directory = os.path.dirname(global_filename)

        # Get the image and resize it to fit application window.
        self.image = ImageTk.PhotoImage(Image.open(os.path.join(monodepth_output_directory,
                                                                depth_map_filename)).resize((self.WIDTH, self.HEIGHT)))

        # Show the image onto the image canvas.
        self.image_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)


if __name__ == '__main__':
    ui = UI()
