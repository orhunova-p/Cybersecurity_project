# Cybersecurity_project
Project for CS 7389F.251 in Texas State University

## Overview
This project focuses on generating adversarial patches for stop signs in the context of autonomous driving systems. The goal is to simulate realistic physical-world attacks that may affect object detection models.

The original CARLA-A3 implementation uses trained object detection models and iteratively modifies an image using gradients to create adversarial patches that fool the model.

Since my goal was just to expand the variety of adversarial stop signs variations, I didn't use ML for this projec. I created adversarial patches manually by adding noise, drawing shapes, and simulating lighting effects.

---

## Features
This script generates:

- A base stop sign reconstructed from masks
- Three types of adversarial patches:
  1. **Subtle Texture Attack** – simulates material noise and printing imperfections
  2. **Graffiti Attack** – simulates vandalism using random shapes
  3. **Sun Glare Attack** – simulates lighting effects and reflections

All adversarial changes are put to the stop sign region and preserve the readability of the "STOP" text.

---

## Repository Structure

There is a main.py file - the script to generate adversarial patches, and data folder which contains images, generated from this file. To run the script use `python main.py` command, but please also see the required files below. Also there is a data folder containing the generated images.

## Required External Files

This project depends on mask files from the CARLA-A3 repository:

details/attack/adversarial_yolo_master/masks/base_mask.txt

details/attack/adversarial_yolo_master/masks/text_mask.txt

You can obtain them from: https://github.com/Fraunhofer-AISEC/CARLA-A3. They are not easily accessible from the repo though, you will need to set up the CARLA-A3 environment first and after that locate the corresponding mask files within the project structure.

## How to run with CARLA-A3

Since this project was developed to expend the variety of edversarial patches for CARLA-A3, please refer to their Github page (https://github.com/Fraunhofer-AISEC/CARLA-A3) for detailed instructions on how to download and build the simulation using the adversarial stop signs from this project. The example of how generated patches can be used with the CARLA-A3 simulator: 

`python3 AdvStopsign.py -p data/My_Patch_1.png` 

Please refer to the "Running the Adversarial Attack Scenario" section on their Github for furter details.

## How to run without CARLA-A3

There is a possibility to generate the adversarial attaks on the stop sign without CARLA-A3. First you will need to run `pip install numpy pillow`. Then, you need to gain two files base_mask.txt and text_mask.txt form their repo and whange the path for the `mask_dir` variable in main.py for whatever folder you have those files in. After that run the script using `python main.py` command and it will generate four outputs, which will be saved in the data/ folder.
