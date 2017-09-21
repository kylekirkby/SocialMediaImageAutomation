from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import ImageOps 
from urllib import request
import io
import textwrap
import csv
import os

class SocialMediaImageAutomation:
    
    """
    This class is used to generate social media images based on a CSV data source
    and output type which is one of a few preset options.
    """
    
    def __init__(self, data_src_file_name, media_templates, local_file_folder="resources/",output_path="output/"):

        # Get the data source csv file
        self._data_src_file_name = data_src_file_name
        # Local resources directory path
        self.local_resources_path = local_file_folder
        # Local Output path for images
        self.output_path = os.getcwd() + "/" + output_path
        # Circle Thumbnail Size
        self.circle_thumb_size = (300, 300)
        
        self.types = ["SFO17 Video Placeholder.jpg", "SFO17 Social Media-placeholder.jpg"]
        
        # Youtube Thumbnail Image URl
        self.youtube_thumbnail_image = "https://img.youtube.com/vi/{0}/sddefault.jpg"
        
        # Background image template
        self.template_images = media_templates
        
        self.photo_offset = (620,20)
        self.event_hash_tag = "#SFO17"
        
        self.fonts = {"regular":"Lato-Regular.ttf",
                      "bold":"Lato-Bold.ttf"}
        
        self.colours = {"black":(0,0,0),
                        "white":(255,255,255),
                        "grey":(153,153,153),
                        "linaro-blue":(70,145,218)}
        
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            
        self.csv_data = self.grab_data_from_csv()
        
        
        for template in self.template_images:
            # print(self.csv_data)
            self.create_social_media_images(template)
            
        
    def grab_data_from_csv(self):
        
        my_file = self._data_src_file_name
        with open(my_file, 'rt',encoding="utf8") as f:
            reader = csv.reader(f)
            csv_data = list(reader)
            data = []
            for each in csv_data:
                title = each[1]
                session_id = each[0]
                position = each[5]
                speaker_names = each[-5]
                track = each[4]
                if "://" in each[6]:
                    photo = each[6]
                else:
                    photo = ""
            
                new_list = [title,speaker_names,track,photo,position,session_id]
                data.append(new_list)
            # for each in data:
            #     print(each)
            
        return data
    
    
    def write_text(self, background_image_draw, text, coords, font_size, font, colour, centered=False, multiline=False, wrap_width=28):
        
        image_font = ImageFont.truetype(font, font_size)
            
        text_width, text_height = image_font.getsize(text)
    
        text_y = coords[1]
        
        if centered:
            x = coords[0][0]
            x2 = coords[0][1]
            text_x = x + ((x2 - x) - (text_width) / 2)
        else:
            text_x = coords[0]
            
        text_coords = (text_x,text_y)
        
        if not multiline:
            background_image_draw.text(text_coords, text, colour, font=image_font)
        else:
            # Convert the text into multiple lines
            lines = textwrap.wrap(text, width=wrap_width)
            line_y = text_coords[1]
            for line in lines:
                width, height = image_font.getsize(line)
                background_image_draw.text((text_coords[0],line_y), line, colour, font=image_font)
                line_y += height
    
        return background_image_draw
        
        
    def create_social_media_images(self, media_template):
        
        
        for speaker in self.csv_data:
            
            title = speaker[0]
            name = speaker[1]
            track = speaker[2]
            image_name = speaker[3]
            position = speaker[4]
            session_id = speaker[5]
            
            if title == "" or session_id == "":
                pass
            else:
                if name == "":
                    name = session_id
                if "://" in image_name:
                    image_file_name = self.grab_photo(image_name)                        
                elif image_name == "":
                    image_file_name = False
                else:
                    image_file_name = self.local_resources_path + image_name
                
                if image_file_name != False:
                    circle_thumb = self.create_circle_thumbnail(image_file_name)

                background_image = Image.open(media_template)

                if image_file_name:
                    # Paste the generated circular thumbnail.
                    background_image.paste(circle_thumb, self.photo_offset, circle_thumb)

                # Get the draw object from ImageDraw.Draw() method
                background_image_draw = ImageDraw.Draw(background_image)
                
                if media_template in self.types:
                    if media_template == self.types[0]:
                        # Video Generation
                        
                        # Generate blue overlay
                        
                        if len(name) < 20:
                            background_image_draw = self.write_text(background_image_draw, name,[[500,750],330],44, self.fonts["bold"], self.colours["black"], centered=True)
                        else:
                            background_image_draw = self.write_text(background_image_draw, name,[[500,750],330],20, self.fonts["bold"], self.colours["black"], centered=True)
                        
                        if len(position) < 40:
                            background_image_draw = self.write_text(background_image_draw, position,[[500,750],390],18, self.fonts["regular"], self.colours["grey"], centered=True)

                        background_image_draw = self.write_text(background_image_draw, track,[20,175],26, self.fonts["bold"], self.colours["white"])
                        
                        background_image_draw = self.write_text(background_image_draw, title,[20,218],32, self.fonts["bold"], self.colours["white"], multiline=True)
                        
                        if not image_file_name:
                            background_image_draw = self.write_text(background_image_draw, self.event_hash_tag,[[500,750],120],44, self.fonts["bold"], self.colours["linaro-blue"], centered=True)
                        

                        output_file = self.output_path + session_id + ".png"
                        print(output_file)
                        # Save the final image.
                        background_image.save(output_file, quality=95)
                        
                    elif media_template == self.types[1]:
                        # Social Media Image Generation
                        if len(name) < 20:
                            background_image_draw = self.write_text(background_image_draw, name,[[500,750],330],44, self.fonts["bold"], self.colours["black"], centered=True)
                        else:
                            background_image_draw = self.write_text(background_image_draw, name,[[500,750],330],20, self.fonts["bold"], self.colours["black"], centered=True)
                        
                        if len(position) < 40:
                            background_image_draw = self.write_text(background_image_draw, position,[[500,750],390],18, self.fonts["regular"], self.colours["grey"], centered=True)

                        background_image_draw = self.write_text(background_image_draw, track,[20,175],26, self.fonts["bold"], self.colours["white"])
                        
                        background_image_draw = self.write_text(background_image_draw, title,[20,218],32, self.fonts["bold"], self.colours["white"], multiline=True)
                        
                        if not image_file_name:
                            background_image_draw = self.write_text(background_image_draw, self.event_hash_tag,[[500,750],120],44, self.fonts["bold"], self.colours["linaro-blue"], centered=True)
                        

                        output_file = self.output_path + session_id + ".png"
                        print(output_file)
                        # Save the final image.
                        background_image.save(output_file, quality=95)
                
                
                
            
    def grab_photo(self, url):
        
        speaker_image_file_name = url.split("/")[-1]
        
        try:
            speaker_image = request.urlretrieve(url, speaker_image_file_name)
        except Exception as e:
            return False
            
        return speaker_image_file_name
        
    def create_circle_thumbnail(self, file_name):
    

        # Open the speaker image to generate the circular thumb.
        image_obj = Image.open(file_name)
        # Create a circle thumbnail file name
        circle_thumbnail_file_name = '{0}-{1}.png'.format(file_name,"circle")
        # Create a new circle thumb mask
        mask = Image.new('L', self.circle_thumb_size, 0)
        # Instantiate Draw() for mask.
        draw = ImageDraw.Draw(mask)
        # Draw a circle with set size and fill.
        draw.ellipse((0, 0) + self.circle_thumb_size, fill=255)
        # Fit the image to the mask
        circle_thumbnail = ImageOps.fit(image_obj, mask.size, centering=(0.5, 0.5))
        circle_thumbnail.putalpha(mask)
        circle_thumbnail.save(circle_thumbnail_file_name)
        
        circle_thumb = Image.open(circle_thumbnail_file_name)
        
        return circle_thumb


if __name__ == "__main__":
    
    cards = SocialMediaImageAutomation("sessions-latest.csv",["SFO17 Social Media-placeholder.jpg","SFO17 Video Placeholder.jpg"])