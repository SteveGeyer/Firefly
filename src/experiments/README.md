# Experimental Directory

This directory holds code for various experiments on analysis.

```
.
├── README.md
├── analyzeimage.py              -- Analyze the images in 'images'
├── images                       -- Images to process
│   ├── angle_20d_back_17cm.png
│   ├ ...
│   └── up_10cm_back_34cm.png
└── makearuco.py                 -- Creates a Aruco test page
```

## Images

The 'images' directory has a series of images to test algorithms
against. A series of images were taken at different distances from the
target and different orientations. All distances and angles shown
below are approximate.

The target has two Aruco 6X6_250 images with an ID of 1. When printed
each marker was 3.4cm by 3.4cm. These marker's centers are 12.3cm
apart.

Images with the filename pattern back\_**dist**\_cm.png are positioned
with the camera centered veritcally on the markers and half way
between the markers horizontally. **dist** is how far back from the
target.

Images with the filename pattern
left\_offset\_10\_cm\_back\_**dist**\_cm.png are positioned with the
camera centered veritcally on the markers and the drone 10 cm from the
half way point between the markers horizontally. **dist** is how far
back from the target.

Images with the filename pattern up\_10\_cm\_back\_**dist**\_cm.png
are positioned with the camera centered 10 cm higher that the
veritcally center on the markers and half way between the markers
horizontally. **dist** is how far back from the target.

Images with the filename pattern down\_10\_cm\_back\_**dist**\_cm.png
are positioned with the camera centered 10 cm lower that the
veritcally center on the markers and half way between the markers
horizontally. **dist** is how far back from the target.

Images with the filename pattern
angle\_**deg**\_deg\_back\_**dist**\_cm.png are positioned with the
camera centered veritcally on the markers and half way between the
markers horizontally. However it is pivoted by **deg** degrees
sideways. **dist** is how far back from the target.
