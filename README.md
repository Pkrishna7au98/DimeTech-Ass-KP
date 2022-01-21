# DimeTech-Assignment-KP
The small task to deal with backend and generate reports using flask, sqlalchemy and frontend tools.


The app.py file includes the complete backend code which is easy to understand. From the beginning importing the necessary modules, and then connecting the app with SQLAlchemy. 
Then a object class is defined in order to input the csv file data to our database. it includes the datatype and length of input data form given csv file.

Then, There are two routes are defined. 
1. This route is for homepage, where we simply render the index.html and give a file attachement option, so that the file can be attached and uploaded. All the files that will be uploaded, will be saved to our local storage and feed into the database. 

2. The second route is for the task-2, which gives us the result of objects detected in the given date range. It also shows the images of the scanned bags which includes items that are stored in "Objects_detected" column. 

At the end of the code, two functions are defined to parse the csv file and converting the datatype to string. 

-----------------------------------------------------------------------------------------------------------------------------------------------------------


In order to run the code:

1. Simply download the project file/repository and then extract it.
2. then just run the app.py in python environment. 
3. it might give some errors if flask, pandas and numpy are not installed. 
4. So, install these modules, and run the code.
5. Now, the database part : It is created on MySQL with XAMPP.
6. so, if needed install the XAMPP and simply start Apache and MySQL.
