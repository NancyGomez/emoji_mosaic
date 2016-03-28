# Names: Nancy Gomez, Sean Carpenter, Robert Lafont
# Project: Emoji Mosaic

from Tkinter import *
from PIL import Image, ImageTk
import random
import os

#********************* EMOJI FUNCTIONS *********************************
def findAverageRGB(image):
	redSum = 0; greenSum = 0; blueSum = 0;
	redCount = 0; greenCount = 0; blueCount = 0;
	
	for h in range(32):
		for w in range(32):
			red, green, blue, alpha = image.getpixel((w,h));
			if (alpha != 0):
				redSum += red; greenSum += green; blueSum += blue;
				redCount += 1; greenCount += 1; blueCount += 1;

	redAvg = redSum/redCount;
	greenAvg = greenSum/greenCount;
	blueAvg = blueSum/blueCount;
	
	return (int(redAvg), int(greenAvg), int(blueAvg));
# **************************************************************************
def transparentToWhite(image, height, width):
	for y in range(height):
		for x in range(width):
			r, g, b, alpha = image.getpixel((x,y));
			if (alpha == 0):
				image.putpixel((x,y), (255, 255, 255, 255));
#****************************************************************************
def findClosestEmoji(red, green, blue, totalEmojis, usedEmoji):
	closestRed = 255; closestGreen = 255; closestBlue = 255;
	for i in range(totalEmojis):
		# conditional statements
		foundRed = abs(red - emojiRGB[i][0]) <= closestRed;
		foundGreen = abs(green - emojiRGB[i][1]) <= closestGreen;
		foundBlue = abs(blue - emojiRGB[i][2]) <= closestBlue;
		
		if (foundRed and foundGreen and foundBlue and usedEmoji[i] / 2 == 0):
			closestRed = abs(red - emojiRGB[i][0]);
			closestGreen = abs(green - emojiRGB[i][1]);
			closestBlue = abs(blue - emojiRGB[i][2]);
			closestEmoji = i;
			
	return (closestEmoji);
#**************************************************************************
def getRandomFile(path):
	files = os.listdir(path);
	index = random.randrange(0, len(files));
	return files[index];
#**************************************************************************

def generateMosaic(mosaicName):
	# open the image that the user's mood matches and resize it
	fileName = getRandomFile("../mediaProject2/allFaces/");
	face = Image.open("../mediaProject2/allFaces/" + fileName);

	img = face.resize((1024,1024)).convert('RGBA');
	# make outter corners white
	transparentToWhite(img,1024,1024);
	
	# stores all the emojis contained in the folder in a list and then finds the average RGB
	# value of each of them and stores that in the RGB matrix for emojis
	count = 0;
	for file in os.listdir("../mediaProject2/64x64"):
		if file.endswith(".png"):<
			imagePath = os.path.abspath("../mediaProject2/64x64/" + file);
			emoji = Image.open(imagePath).convert('RGBA');
			emoji = emoji.resize((32,32));
			transparentToWhite(emoji, 32, 32);
			emojiList.append(emoji);
		
			# column 0 = red, 1 = green, and 2 = blue		
			redEmoji, greenEmoji, blueEmoji = findAverageRGB(emojiList[count]);
			emojiRGB[count][0] = redEmoji;
			emojiRGB[count][1] = greenEmoji;
			emojiRGB[count][2] = blueEmoji;

			count+=1;	
	emojiNum = count-1;

	# a list that stores the emojis number of times an emoji has been used (corresponding index) 
	usedEmojis = [0] * emojiNum;

	# Going through the image and collecting 32x32 mini images (total is 1024)
	for y in range(0, 1024, 32):
		for x in range(0, 1024, 32):
			# get 32x32 pixel images (x and y represent the upper left corner
			# of the box, and the x+32 and y+32 represent the lower right corner
			boundingBox = (x, y, x+32, y+32);
			cropped_img = img.crop(boundingBox).convert('RGBA');
			subSections[x][y] = cropped_img;

			# Compare to the average RGB values of each possible emoji and
			# choose the one that most closely mirrors those values
			red, green, blue = findAverageRGB(subSections[x][y]);
		
			#find the closest emoji (with some randomization)
			closestEmoji = findClosestEmoji(red, green, blue, emojiNum, usedEmojis);
			#add the occurence of the emoji to the array and increment the occurence	
			usedEmojis.insert(closestEmoji, usedEmojis[closestEmoji]);
			usedEmojis[closestEmoji]+=1;
		
			# adding a filter to the image so that it looks nicer :)		
			filtered = Image.new('RGBA', (32, 32), (red, green, blue, 75));
			filteredEmoji = Image.alpha_composite(emojiList[closestEmoji], filtered);
			emojis[x][y] = filteredEmoji;

	# creating an empty image to store the emojis that represent each mini image
	put_together_emojis = Image.new('RGBA', (1024,1024), "white");

	for y in range(0, 1024, 32):
		for x in range(0, 1024, 32):
			put_together_emojis.paste(emojis[x][y], (x,y));

	put_together_emojis.save(mosaicName, 'PNG');
	
#**********************BUTTON FUNCTIONS*********************************
def closeWin(): 
    window.destroy();
# ******************************* MAIN ****************************************

# Making a matrix to hold the subSections and another to hold an emoji which
# represents each subSection
subSections = [[0 for col in range(1024)] for row in range(1024)];
emojis = [[0 for col in range(1024)] for row in range(1024)];

# a list of all the face emojis we have saved and resized
emojiList = [];

# a matrix that stores the rgb values (0 = red, 1 = green, 2 = blue) 
emojiRGB = [[0 for col in range(3)] for row in os.listdir("../mediaProject2/64x64")];

# Generate both mosaics
generateMosaic('Mosaic1.png');
generateMosaic('Mosaic2.png');

# TKINTER STUFF
window = Tk()

# Display text to the screen
label = Label(text="Choose your\nfavorite Mosaic:");
label.config(font=("Times New Roman", 36));
label.pack();

# Opens first mosaic and making it a button
image1 = Image.open('Mosaic1.png');
photo1 = ImageTk.PhotoImage(image1);
B1 = Button(window, command=closeWin);
B1.config(image=photo1);
B1.pack(side=LEFT);

# Opens second mosaic and making it a button
image2 = Image.open('Mosaic2.png');
photo2 = ImageTk.PhotoImage(image2);
B2 = Button(window, command=closeWin);
B2.config(image=photo2);
B2.pack(side=RIGHT);

window.mainloop();
