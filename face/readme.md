## Python script to identify whether person in picture is awake or asleep.

## Work in progress:

Unable to detect faces if both eyes closed

## Current results:

<img src="https://raw.githubusercontent.com/captmomo/practice/master/face/ministers_rated.JPG" width=50%>

<img src="https://raw.githubusercontent.com/captmomo/practice/master/face/wink_1_rated.JPG" width=50%>

![wink_2](https://raw.githubusercontent.com/captmomo/practice/master/face/wink_2_rated.JPG |width=200))

![baby_1](https://raw.githubusercontent.com/captmomo/practice/master/face/baby_1_rated.JPG | width=200))

## Notes:

Need to play around with scaleFactor, minSize and maxSize
eg. for ministers picture this setting works:  
    
    faces = face_cascade.detectMultiScale(gray, 
                scaleFactor=3, 
                minNeighbors=2, 
                minSize=(30,30), 
                flags = cv2.CASCADE_SCALE_IMAGE)
