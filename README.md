## Songs, Playlists and Users' database management

Our application acquires some of a music streaming platform's basic features that provide services to the users using data from a
database. It was created using Python and its standard GUI library named Tkinter for the functionalities and SQLite3 for data management from
the database. The program is similar to a music streaming application where the users are either music listeners or artists. What the users can
do with the application is very simple. First, they can log in using their unique ID and passwords, which they have registered and stored in the
database. Then, depending on whether the user is a listener, an artist, or even both, they can perform several actions on the platform, such as
starting and ending a music session or creating a song playlist (for listeners) or adding a song to the application’s database (for artists).
The most dominant part of the program’s design lies in using Tkinter, a Python graphical user interface. The application’s features are
displayed or acted on by the users through buttons, labels, and search entries on the interface, contributing to the user experience. The GUI is
also useful during the creation process by helping the programmers navigate easily and thus be less likely to make mistakes due to its simplicity
and visibility. Python was chosen to write the program because of its compatibility with SQLite - the go-to language for managing data using a
relational model. Below is a small user guide on how to use the program.






## Library
```
numpy>=1.18.2
scipy>=1.4.1
wget>=3.2
seaborn>=0.10.0
tensorflow==2.3.0
tensorflow-gpu==2.3.0
opencv-python==4.1.2.30
tqdm==4.43.0
pandas
awscli
urllib3
```

## Structure and Components
- `create_datasets/create_datasets.py`: Create datasets with captured image 
- `model_data/coco`: Testing data for yolov3
- `tools/XML_to_YOLOv3.py`: prepare data (position in image) for the model
- `YOLOv3_colab_training.py`: train data in google colab 
- `train.py`: train data without google colab
- `other files`: yolov3 supplement files

