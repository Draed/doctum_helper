# doctum_helper

## temp features 

- prevent writing existing json file course
- add a completion custom for task description :
    - read article
    - watch video
    - ...

## Description

A simple linux terminal application that help writing [doctum content (courses)](https://github.com/Draed/doctum_content) with correct json format.

### Components 

- Bash (5.2.15(1)-release)
- Python (v3.12.7)
- [Python package](./src/requirements.txt)

### Images

<img src="./images/json_file_completion.png" alt="json_file_completion" width="1000"/>
<br>
<img src="./images/validator.png" alt="validator" width="500"/>
<img src="./images/full_app.png" alt="full_app" width="500"/>

## Prerequisites 

- [virtualvenv](https://virtualenv.pypa.io/en/latest/installation.html) must already be installed

## Usage

### First installation 

- Launch install script :
```shell
git clone https://github.com/Draed/doctum_helper.git
cd doctum_helper
bash install.sh
```

- Now the doctum_helper alias `dh` might be available, see [below doctum_helper usage](#doctum_helper-usage)

### doctum_helper (dh) usage

#### Launch doctum_helper 
- To start the program, just launch `dh` in the terminal and follow the instructions

#### First start
- At first start the doctum_helper will ask for default parameters :
    - the path to the doctum_content directory (where doctum_content should be stored)

#### Completion
- Completion is available for 3 questions (use tab to trigger completion) :
    - Enter the path for the new new doctum course : listing existing path in doctum_content folder 
    - Enter the tag : showing doctum_content dir name as tag category
    - Enter the task description : with default task description