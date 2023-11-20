from customtkinter import *
from PIL import Image
import matplotlib.pyplot as plt

from bin import utils, original_and_copy, one_file

def main():
    app = App()
    app.mainloop()

class App(CTk):
    def __init__(self):
        super().__init__()

        self.init_root()
        self.init_variables()
        self.init_placeholders()
        self.init_nav()

        self.init_about_frame()
        self.init_original_and_copy_frame()
        self.init_one_file_frame()

        self.select_frame_by_name('about')

    def init_root(self):
        """Inits main window of app."""
        self.title('Steganalysis tools')
        self.iconbitmap('static/icons/icon.ico')
        self.resizable(False, False)
        self.geometry('800x500')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def init_variables(self):
        self.original_path = None
        self.copy_path = None

        self.one_file_path = None
        self.one_file_channel = 'RED'
        self.one_file_offset = '0'

    def init_placeholders(self):
        """Inits placeholder images from static folder"""
        self.original_image = CTkImage(light_image=Image.open('static/placeholders/image_light.png'), 
                                       dark_image=Image.open('static/placeholders/image_dark.png'), 
                                       size=(230, 180))
        
        self.copy_image = CTkImage(light_image=Image.open('static/placeholders/image_light.png'), 
                                   dark_image=Image.open('static/placeholders/image_dark.png'), 
                                   size=(230, 180))
        
        self.one_file_image = CTkImage(light_image=Image.open('static/placeholders/image_light.png'), 
                                   dark_image=Image.open('static/placeholders/image_dark.png'), 
                                   size=(230, 180))

    def init_nav(self):
        """Inits left nav bar"""
        self.nav_frame = CTkFrame(self, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky=NSEW)
        self.nav_frame.grid_rowconfigure(4, weight=1)

        self.name_label = CTkLabel(self.nav_frame, text='Steganalysis tools', compound='left', font=CTkFont(size=15, weight='bold'))
        self.name_label.grid(row=0, column=0, padx=15, pady=15)

        # Buttons
        self.about_button = self.create_nav_button('About', self.about_button_event)
        self.about_button.grid(row=1, column=0, sticky=EW)

        self.original_and_copy_button = self.create_nav_button('Original and copy', self.original_and_copy_button_event)
        self.original_and_copy_button.grid(row=2, column=0, sticky=EW)

        self.one_file_button = self.create_nav_button('One file', self.one_file_button_event)
        self.one_file_button.grid(row=3, column=0, sticky=EW)


    def create_nav_button(self, label, command):
        return CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10, text=label,
                         fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'),
                         anchor=W, command=command)
    
    def init_about_frame(self):
        """Inits home about frame"""
        self.about_frame = CTkFrame(self, corner_radius=0, fg_color='transparent')
        about_text = CTkLabel(self.about_frame, text='About steganalysis tools app')
        about_text.place_configure(relx=0.5, rely=0.5, anchor=CENTER)

    def init_original_and_copy_frame(self):
        """Inits original and copy frame"""
        self.original_and_copy_frame = CTkFrame(self, corner_radius=0, fg_color='transparent')

        # Original frame
        self.original_frame = CTkFrame(self.original_and_copy_frame, fg_color=('gray85', 'gray10'))
        self.original_frame.place_configure(relx=0.02, rely=0.02, relheight=0.85, relwidth=0.47)
        self.original_frame.place()

        self.original_img_label = CTkLabel(self.original_frame, text="", image=self.original_image)
        self.original_img_label.place_configure(relx=0.5, rely=0.25, anchor=CENTER)
        self.original_img_label.place()

        self.select_original_button = CTkButton(self.original_frame, text='Select original image', 
                                                fg_color=('gray75', 'gray25'), text_color=('gray10', 'gray90'),
                                                command=self.select_original_button_event)
        self.select_original_button.place_configure(relx=0.5, rely=0.52, relwidth=0.9, anchor=CENTER)
        self.select_original_button.place()

        self.original_info_label = CTkLabel(self.original_frame, text="", font=CTkFont(size=15, weight='normal'))
        self.original_info_label.place_configure(relx=0.05, rely=0.6)
        self.original_info_label.place()

        # Copy_frame
        self.copy_frame = CTkFrame(self.original_and_copy_frame, fg_color=('gray85', 'gray10'))
        self.copy_frame.place_configure(relx=0.51, rely=0.02, relheight=0.85, relwidth=0.47)
        self.copy_frame.place()

        self.copy_img_label = CTkLabel(self.copy_frame, text="", image=self.copy_image)
        self.copy_img_label.place_configure(relx=0.5, rely=0.25, anchor=CENTER)
        self.copy_img_label.place()

        self.select_copy_button = CTkButton(self.copy_frame, text='Select copy image', 
                                                fg_color=('gray75', 'gray25'), text_color=('gray10', 'gray90'),
                                                command=self.select_copy_button_event)
        self.select_copy_button.place_configure(relx=0.5, rely=0.52, relwidth=0.9, anchor=CENTER)
        self.select_copy_button.place()

        self.copy_info_label = CTkLabel(self.copy_frame, text="", font=CTkFont(size=15, weight='normal'))
        self.copy_info_label.place_configure(relx=0.05, rely=0.6)
        self.copy_info_label.place()

        # Action buttons
        self.hash_comparison_button = CTkButton(self.original_and_copy_frame, text='Compare images by hash', 
                                                command=self.hash_comparison_button_event, font=CTkFont(size=15, weight='bold'))
        self.hash_comparison_button.place_configure(relx=0.02, rely=0.90, relwidth=0.47, relheight=0.07)

        self.find_diff_pixels_button = CTkButton(self.original_and_copy_frame, text='Find different pixels in images', 
                                                command=self.find_diff_pixels_button_event, font=CTkFont(size=15, weight='bold'))
        self.find_diff_pixels_button.place_configure(relx=0.51, rely=0.90, relwidth=0.47, relheight=0.07)

    def init_one_file_frame(self):
        """Inits one_file_frame frame"""
        self.one_file_frame = CTkFrame(self, corner_radius=0, fg_color='transparent')

        self.one_file_inner_frame = CTkFrame(self.one_file_frame, fg_color=('gray85', 'gray10'))
        self.one_file_inner_frame.place_configure(relx=0.02, rely=0.02, relheight=0.85, relwidth=0.47)
        self.one_file_inner_frame.place()

        self.one_file_label = CTkLabel(self.one_file_inner_frame, text="", image=self.one_file_image)
        self.one_file_label.place_configure(relx=0.5, rely=0.25, anchor=CENTER)
        self.one_file_label.place()

        self.select_one_file_button = CTkButton(self.one_file_inner_frame, text='Select an image', 
                                                fg_color=('gray75', 'gray25'), text_color=('gray10', 'gray90'),
                                                command=self.select_one_file_button_event)
        self.select_one_file_button.place_configure(relx=0.5, rely=0.52, relwidth=0.9, anchor=CENTER)
        self.select_one_file_button.place()

        self.one_file_info_label = CTkLabel(self.one_file_inner_frame, text="", font=CTkFont(size=15, weight='normal'))
        self.one_file_info_label.place_configure(relx=0.05, rely=0.6)
        self.one_file_info_label.place()

        # Action Buttons
        self.show_histogram_button = CTkButton(self.one_file_frame, text='Show image histograms', 
                                                command=self.show_histogram_button_event, font=CTkFont(size=15, weight='bold'))
        self.show_histogram_button.place_configure(relx=0.02, rely=0.90, relwidth=0.47, relheight=0.07)

        self.channel_label = CTkLabel(self.one_file_frame, text='Channel:')
        self.channel_label.place_configure(relx=0.51, rely=0.02)
        self.channel_option_menu = CTkOptionMenu(self.one_file_frame, values=['RED', 'GREEN', 'BLUE'],
                                             command=self.channel_combobox_callback)
        self.channel_option_menu.place_configure(relx=0.51, rely=0.07)

        self.offset_label = CTkLabel(self.one_file_frame, text='Offset:')
        self.offset_label.place_configure(relx=0.51, rely=0.17)
        self.offset_option_menu = CTkOptionMenu(self.one_file_frame, values=['0', '1', '2', '3', '4', '5', '6', '7'],
                                             command=self.offset_combobox_callback)
        self.offset_option_menu.place_configure(relx=0.51, rely=0.22)

        self.detect_strings_button = CTkButton(self.one_file_frame, text='Detect ASCII strings in image', 
                                                command=self.detect_strings_button_event, font=CTkFont(size=15, weight='bold'))
        self.detect_strings_button.place_configure(relx=0.51, rely=0.42, relwidth=0.47, relheight=0.07)

        self.offset_label = CTkLabel(self.one_file_frame, text='This could take a few minutes')
        self.offset_label.place_configure(relx=0.51, rely=0.85)
        self.detect_odd_pixels_button = CTkButton(self.one_file_frame, text='Detect odd pixels in image', 
                                                command=self.detect_odd_pixels_button_event, font=CTkFont(size=15, weight='bold'))
        self.detect_odd_pixels_button.place_configure(relx=0.51, rely=0.90, relwidth=0.47, relheight=0.07)

    def select_original_button_event(self):
        img_path = filedialog.askopenfilename(filetypes= [('Image file', ('.png', '.jpg', '.jpeg', '.bmp'))])
        if img_path:
            img_info = original_and_copy.get_file_info(img_path)
            if img_info:
                img_size = utils.calculate_img_size(img_info.get('width'), img_info.get('height'))
                self.original_image = CTkImage(Image.open(img_path), size=img_size)
                self.original_img_label.destroy()
                self.original_img_label = CTkLabel(self.original_frame, text="", image=self.original_image)
                self.original_img_label.place_configure(relx=0.5, rely=0.25, anchor=CENTER)
                self.original_img_label.place()

                self.original_info_label.destroy()
                self.original_info_label = CTkLabel(self.original_frame, anchor=W, justify=LEFT,
                                                    text=utils.dict_to_info(img_info), 
                                                    font=CTkFont(size=15, weight='normal'))
                self.original_info_label.place_configure(relx=0.05, rely=0.6)
                self.original_info_label.place()

                self.original_path = img_path

    def select_copy_button_event(self):
        img_path = filedialog.askopenfilename(filetypes= [('Image file', ('.png', '.jpg', '.jpeg', '.bmp'))])
        if img_path:
            img_info = original_and_copy.get_file_info(img_path)
            if img_info:
                img_size = utils.calculate_img_size(img_info.get('width'), img_info.get('height'))
                self.copy_image = CTkImage(Image.open(img_path), size=img_size)
                self.copy_img_label.destroy()
                self.copy_img_label = CTkLabel(self.copy_frame, text="", image=self.copy_image)
                self.copy_img_label.place_configure(relx=0.5, rely=0.25, anchor=CENTER)
                self.copy_img_label.place()

                self.copy_info_label.destroy()
                self.copy_info_label = CTkLabel(self.copy_frame, anchor=W, justify=LEFT,
                                                    text=utils.dict_to_info(img_info), 
                                                    font=CTkFont(size=15, weight='normal'))
                self.copy_info_label.place_configure(relx=0.05, rely=0.6)
                self.copy_info_label.place()

                self.copy_path = img_path

    def hash_comparison_button_event(self):
        if self.original_path and self.copy_path:
            result = original_and_copy.compare_by_hash(self.original_path, self.copy_path)

            window = CTkToplevel(self)
            window.title('Images are IDENTICAL' if result[0] else 'Images are DIFFERENT')
            window.resizable(False, False)
            window.geometry('750x100')

            result_label = CTkLabel(window, anchor=W, justify=LEFT, font=CTkFont(family="Courier", size=15),
                                    text='Original HASH: ' + result[1] + '\n'+ 4*' ' + 'Copy HASH: ' + result[2])
            result_label.place_configure(relx=0.5, rely=0.5, anchor=CENTER)
            result_label.place()

            window.attributes('-topmost', 'true')

    def find_diff_pixels_button_event(self):
        if self.original_path and self.copy_path:
            result = original_and_copy.compare_by_pixels(self.original_path, self.copy_path)

            window = CTkToplevel(self)
            window.title('Different pixels in images')
            window.resizable(False, False)
            window.geometry('600x400')

            if isinstance(result, str):
                error_label = CTkLabel(window, text=result, font=CTkFont(size=15, weight='normal'))
                error_label.place_configure(relx=0.5, rely=0.5, anchor=CENTER)
                error_label.place()
            else:
                label_text = 'No different pixels in images.'
                if result != []:
                    label_text = 'Position'.ljust(22) + 'Original image'.ljust(22) + 'Copy image'
                    for pixel in result:
                        position = pixel.get('position')
                        label_text += ('\nx: ' + str(position[0]) + '; y: ' + str(position[1])).ljust(22)
                        label_text += str(pixel.get('original_pixel')).ljust(22) + str(pixel.get('copy_pixel'))

                scroll_frame = CTkScrollableFrame(window, width=566, height=378)
                scroll_frame.grid(row=0, column=0, padx=5, pady=5)

                result_label = CTkLabel(scroll_frame, text=label_text, anchor=W, justify=LEFT, font=CTkFont(family="Courier", size=15))
                result_label.grid(row=0, column=0)
                
            window.attributes('-topmost', 'true')

    def select_one_file_button_event(self):
        img_path = filedialog.askopenfilename(filetypes= [('Image file', ('.png', '.jpg', '.jpeg', '.bmp'))])
        if img_path:
            img_info = original_and_copy.get_file_info(img_path)
            if img_info:
                img_size = utils.calculate_img_size(img_info.get('width'), img_info.get('height'))
                self.one_file_image = CTkImage(Image.open(img_path), size=img_size)
                self.one_file_label.destroy()
                self.one_file_label = CTkLabel(self.one_file_inner_frame, text="", image=self.one_file_image)
                self.one_file_label.place_configure(relx=0.5, rely=0.25, anchor=CENTER)
                self.one_file_label.place()

                self.one_file_info_label.destroy()
                self.one_file_info_label = CTkLabel(self.one_file_inner_frame, anchor=W, justify=LEFT,
                                                    text=utils.dict_to_info(img_info), 
                                                    font=CTkFont(size=15, weight='normal'))
                self.one_file_info_label.place_configure(relx=0.05, rely=0.6)
                self.one_file_info_label.place()

                self.one_file_path = img_path

    def show_histogram_button_event(self):
        if self.one_file_path:
            histogram = one_file.get_img_histogram(self.one_file_path)

            plt.figure(figsize=(16,4))

            plt.subplot(131)
            plt.hist(histogram[0], bins=256, color='red', alpha=0.7, rwidth=1.8)
            plt.title('Red pixels')

            plt.subplot(132)
            plt.hist(histogram[1], bins=256, color='green', alpha=0.7, rwidth=0.8)
            plt.title('Green pixels')

            plt.subplot(133)
            plt.hist(histogram[2], bins=256, color='blue', alpha=0.7, rwidth=0.8)
            plt.title('Blue pixels')

            plt.tight_layout()
            plt.show()

    def channel_combobox_callback(self, value):
        self.one_file_channel = value

    def offset_combobox_callback(self, value):
        self.one_file_offset = value

    def detect_strings_button_event(self):
        if self.one_file_path:
            channel_str = self.one_file_channel
            channel = 0 if channel_str == 'RED' else 1 if channel_str == 'GREEN' else 2
            offset = int(self.one_file_offset)
            detected_strings = one_file.detect_strings(self.one_file_path, channel, offset)
            
            window = CTkToplevel(self)
            window.title('Detected strings in image (channel: ' + channel_str + ', offset: ' + str(offset) + ')')
            window.resizable(False, False)
            window.geometry('800x500')

            scroll_frame = CTkScrollableFrame(window, width=766, height=478)
            scroll_frame.grid(row=0, column=0, padx=5, pady=5)

            result_label = CTkLabel(scroll_frame, text=detected_strings, anchor=W, justify=LEFT, font=CTkFont(family="Courier", size=15))
            result_label.grid(row=0, column=0)
                
            window.attributes('-topmost', 'true')

    def detect_odd_pixels_button_event(self):
        if self.one_file_path:
            result = one_file.detect_odd_pixels(self.one_file_path)

            window = CTkToplevel(self)
            window.title('Odd pixels in images')
            window.resizable(False, False)
            window.geometry('600x400')

            if isinstance(result, str):
                error_label = CTkLabel(window, text=result, font=CTkFont(size=15, weight='normal'))
                error_label.place_configure(relx=0.5, rely=0.5, anchor=CENTER)
                error_label.place()
            else:
                label_text = 'No odd pixels detected in images.'
                if result != []:
                    label_text = 'Position'.ljust(22) + 'Pixel value'.ljust(22) + 'Expected pixel value'
                    for pixel in result:
                        position = pixel.get('position')
                        label_text += ('\nx: ' + str(position[0]) + '; y: ' + str(position[1])).ljust(22)
                        label_text += str(pixel.get('pixel')).ljust(22) + str(pixel.get('expected'))

                scroll_frame = CTkScrollableFrame(window, width=566, height=378)
                scroll_frame.grid(row=0, column=0, padx=5, pady=5)

                result_label = CTkLabel(scroll_frame, text=label_text, anchor=W, justify=LEFT, font=CTkFont(family="Courier", size=15))
                result_label.grid(row=0, column=0)
                
            window.attributes('-topmost', 'true')


    def select_frame_by_name(self, name):
        """Switches between frames"""
        self.about_button.configure(fg_color=('gray75', 'gray25') if name == 'about' else 'transparent')
        self.original_and_copy_button.configure(fg_color=('gray75', 'gray25') if name == 'original_and_copy' else 'transparent')
        self.one_file_button.configure(fg_color=('gray75', 'gray25') if name == 'one_file' else 'transparent')

        if name == 'about':
            self.about_frame.grid(row=0, column=1, sticky=NSEW)
        else:
            self.about_frame.grid_forget()
        if name == 'original_and_copy':
            self.original_and_copy_frame.grid(row=0, column=1, sticky=NSEW)
        else:
            self.original_and_copy_frame.grid_forget()
        if name == 'one_file':
            self.one_file_frame.grid(row=0, column=1, sticky=NSEW)
        else:
            self.one_file_frame.grid_forget()

    def about_button_event(self):
        self.select_frame_by_name('about')

    def original_and_copy_button_event(self):
        self.select_frame_by_name('original_and_copy')

    def one_file_button_event(self):
        self.select_frame_by_name('one_file')

if __name__ == '__main__':
    main()