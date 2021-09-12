# HandyInteraction

The Handy Interaction software is presented as a desktop application that is based on the detection and tracking of the 
user's hands, using a conventional camera, to allow the extraction of motion-based features in real time and facilitate 
human-computer interaction in different technological contexts. The application uses machine learning and deep learning 
models, and arises from the study of the state of the art in the use of computer vision algorithms for interaction 
design.

## Installation
The software installation is based on cloning the project repository, or downloading the containing folder with all the 
necessary files. Once said folder is unzipped, the following file structure is obtained. In this case we are going to 
call the containing folder **${HANDY_ROOT}**.
```
${HANDY_ROOT}
|--ICONS
|--MODELS
|--about.py
|--HandPoseDraw.py
|--HandPoseEmbedder.py
|--handy.py
|--KNN_classifier.py
|--ui_function.py
|--ui_main.py
|--requirements.txt
```

To install the dependencies it is assumed that Python 3.7 or higher is installed and the most recent version of conda 
available on the internet. Also, it is suggested to create a virtual environment using conda to install the dependencies 
for this software without affecting other python packages that may be installed on the system. The steps are shown below 
and must be executed from a terminal/command prompt window.

    conda create -n HandyApp
    conda activate HandyApp
    cd ${HANDY_ROOT}
    pip install -r requirements.txt

Once the virtual environment is activated and the required packages installed, the software runs by running the 
**handy.py** script, as shown in the following command.
```
(HandyApp) c:\${HANDY_ROOT}>python handy.py
``` 
 
 
## About this Software
Handy Interaction was developed by **Antonio Escamilla Pinilla** working for the Universidad Pontificia Bolivariana, in 
the context of a research project entitled **MOTION-BASED FEATURE ANALYSIS FOR THE DESIGN OF FULL-BODY INTERACTIONS IN 
THE CONTEXT OF COMPUTER VISION AND LARGE VOLUME SPACES**. Project funded by the Research Center for Development and 
Innovation CIDI-UPB with number 584C-05/20-23.
