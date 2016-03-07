from PIL import Image
import os

#********************* FUNCTIONS **************************************
def findAverageRGB(image):
	redSum = 0
	greenSum = 0
	blueSum = 0
	
	redCount = 0
	greenCount = 0
	blueCount = 0
	
	for h in range(32):
		for w in range(32):
			red, green, blue, alpha = image.getpixel((w,h))
			redSum += red
			greenSum += green
			blueSum += blue
			
			redCount += 1
			greenCount += 1
			blueCount += 1

	redAvg = redSum/redCount
	greenAvg = greenSum/greenCount
	blueAvg = blueSum/blueCount
	
	return (int(redAvg), int(greenAvg), int(blueAvg))
# **************************************************************************
def transparentToWhite(image, height, width):
	for y in range(height):
		for x in range(width):
			if (image.getpixel((x,y)) == (0, 0, 0, 0)):
				image.putpixel((x,y), (255, 255, 255, 255))
#************************** MAIN *****************************************
# user declares their  mood
'''THAT CODE GOES HERE'''

# open the image that the user's mood matches and resize it
moodImg = Image.open("1.png")
img = moodImg.resize((1024,1024)).convert('RGBA')
# make outter corners white
transparentToWhite(img,1024,1024)

# ERROR CHECK: checking to make sure we have the right number of images
numImages = 0
expectedImages = 1024

# Making a matrix to hold the subSections and another to hold an emoji which
# represents each subSection
subSections = [[0 for col in range(expectedImages)] for row in range(expectedImages)]
emojis = [[0 for col in range(expectedImages)] for row in range(expectedImages)]

# a list of all the face emojis we have saved and resized
emojiList = []

# a matrix that stores the rgb values 
emojiRGB = [[0 for col in range(3)] for row in range(40)]

# stores all 40 emojis contained in the folder in a list and then finds the average RGB
# value of each of them and stores that in the RGB matrix for emojis 
for i in range(40):
	imagePath = os.path.abspath("../mediaProject2/allFaces/" + str(i+1) + ".png")
	emoji = Image.open(imagePath).convert('RGBA')
	emoji = emoji.resize((32,32))
	# make outter corners white
	transparentToWhite(emoji, 32, 32)
	emojiList.append(emoji)
	redEmoji, greenEmoji, blueEmoji = findAverageRGB(emojiList[i])
	emojiRGB[i][0] = redEmoji
	emojiRGB[i][1] = greenEmoji
	emojiRGB[i][2] = blueEmoji 
	
# Going through the image and collecting 32x32 mini images (total is 1024)
for y in range(0, 1024, 32):
	for x in range(0, 1024, 32):
		# get 32x32 pixel images (x and y represent the upper left corner
		# of the box, and the x+32 and y+32 represent the lower right corner
		boundingBox = (x, y, x+32, y+32)
		cropped_img = img.crop(boundingBox).convert('RGBA')
		subSections[x][y] = cropped_img
				
		# ERROR CHECK: checking to make sure every sub image is the same size
		width, height = subSections[x][y].size
		if (width != height):
			print("Error, an image is not sized correctly.")
		
		# Compare to the average RGB values of each possible emoji and
		# choose the one that most closely mirrors those values
		red, green, blue = findAverageRGB(subSections[x][y])
		
		filtered = Image.new('RGBA', (32, 32), (red, green, blue, 150))
		filteredEmoji = Image.alpha_composite(emojiList[1], filtered)
		emojis[x][y] = filteredEmoji
		numImages+=1
				
	
# ERROR CHECK: checking to make sure we have the right number of images		
if (numImages != expectedImages):
	print("Error, incorrect number of images.")

# creating an empty image to store the mini images and another to store the
# emojis that represent each mini image (default color set to white)
put_together = Image.new('RGBA', (1024,1024), "white")
put_together_emojis = Image.new('RGBA', (1024,1024), "white")

for y in range(0, 1024, 32):
	for x in range(0, 1024, 32):
		put_together.paste(subSections[x][y], (x,y))
		put_together_emojis.paste(emojis[x][y], (x,y))
		
put_together.show()
put_together_emojis.show()		
