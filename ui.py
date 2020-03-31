import tkinter as tk
import os
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from monodepth2.test_simple import test_simple


def monodepth(filename, model_name):
    """
    Runs Monodepth on an image using the given model.
    It outputs the depth map in the same directory as
    where the original image was.
    :param filename: The global file path of the image.
    :param model_name: The name of the model we want to use.
    """
    test_simple(filename, model_name)


class UI:
    def __init__(self):
        """
        Initializes the user interface.
        """
        # Dimensions of the application window.
        self.WIDTH = 1024
        self.HEIGHT = 676

        # Dimensions of an image, ensure it's a 16:9 ratio.
        self.IMG_WIDTH = 1024
        self.IMG_HEIGHT = 576

        self.root = tk.Tk()
        self.root.title('Glasses Visualizer')  # Application title.

        # Create a canvas to show the image.
        self.image_canvas = tk.Canvas(self.root, width=self.IMG_WIDTH, height=self.IMG_HEIGHT, bg='green')

        # Create a frame to hold all of the options.
        self.options_frame = tk.Frame(self.root)

        # Upload button to upload an image.
        self.upload_button = tk.Button(self.options_frame, text='Upload',
                                       width=10, command=self._upload)

        # Pack it all up.
        self.image_canvas.pack()
        self.options_frame.pack()
        self.upload_button.pack(pady=10)

        self.root.mainloop()  # Show the UI.

    def _upload(self):
        """
        The upload functionality for the upload button.
        It asks the user for the image, runs it through Monodepth,
        then shows it onto the image canvas.
        """

        # Asks the user for an image, runs that through Monodepth
        # using the (hard-coded) model.
        img_global_filename = askopenfilename()
        monodepth_model = 'mono+stereo_1024x320'
        monodepth(img_global_filename, monodepth_model)

        # Monodepth outputs a depth map with the file name
        # '<original-image-name>_disp.jpg' in the directory of the original image.
        # We want to find that path so we can find the depth map.
        output_directory = os.path.dirname(img_global_filename)
        img_local_filename = os.path.splitext(os.path.basename(img_global_filename))[0]
        depth_map_global_filename = os.path.join(output_directory, "{}_disp.jpeg".format(img_local_filename))

        # Get the depth map image.
        self.depth_map = ImageTk.PhotoImage(
            Image.open(depth_map_global_filename).resize((self.IMG_WIDTH, self.IMG_HEIGHT)))

        # Output the depth map image onto the image canvas.
        self.image_canvas.create_image(0, 0, image=self.depth_map, anchor=tk.NW)


if __name__ == '__main__':
    ui = UI()
