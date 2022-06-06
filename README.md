# MoTiVML

## Description

An open source ROS based library that extends the capabilities of the [SERA](https://www.cse.chalmers.se/~bergert/paper/2018-icsa-sera.pdf) architecture to include variability management, with a high level of flexibility and customizability of robotic product line entities, while improving practices currently present in the robotics applications development domain.

With this library, roboticists can model robotic `FEATURES`, create `MODEL` configurations using binding time and binding mode and plug in source code implementations for modelled `FEATURES`

## Prerequisites

1. Ubuntu 20 LTS or higher

2. [ROS](http://wiki.ros.org/ROS/Installation) installation. This application was developed and tested with ROS Neotic 1.15.9.

3. [Python3](https://www.python.org/) installation

4. C++ 11 or higher

## Installation

Go to your workspace project, type catkin_make and press enter on your keyboard.

## Usage: How To:

### Create and Validate `MODEL`:

1. Create a project in a directory in the parent directory
2. In the project, specify a model.json and config.json file
3. In the model.json file of your project, add your nested features according to your preferences
NB: Each feature specification must have the keys `id`, `name`, `constraints`, `group`, `isMandatory`. Likewise the `constraints`
object must contain `featureIncluded`, `featureExcluded`, `bindingTimeAllowed`, `bindingModeAllowed`
4. In the config.json file of your project, for every feature added in your model.json file, a corresponding configuration object must be added.
NB: Each featue config object must have the keys `id` which references a feature ID in your model.json file, and `props.` The `props` attribute must contain `time` and `mode` attributes.

5. Validate your model schema and constraints with the command `python motivml.py <project_directory_name>`
6. Alternatively, you can also use the in-built command line interface. Launch the MoTiVML commannd line interface with the command `python mmconsole.py <project_directory_name>`
7. In the MoTiVML commandline interface,  use the command `show <project_name>` to view a graphical representation of your project model.
 

### Plug in Source Code Implementations of `FEATURES`

If there are no syntax and symantic errors detected by the MoTiVML engine, source code implementations of features can be implemented and executed. Source code implementation in both `C++` and `Python` can be plugged in

1. Extract, encapsulate and plug in your feature implementations into the `featx` directory
2. For each plugged in source code implementation, name the entrypoint file ccontaining the `main` function with the same name as the corresponding feature in your MoTiVML model.json file
3. In the MoTiVML commandline interface,  use the command `run <feature_name>` to execute the feature source code.

## Publication
To be updated soon
