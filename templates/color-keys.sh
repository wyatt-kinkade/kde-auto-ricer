#!/bin/bash

# Generate random hex RGB value. No # character.

# Random Colors
colorKeys={color1.strip}
colorFKeys={color2.strip}
colorNumeric={color3.strip}
colorFunctions={color4.strip}
colorModifiers={color5.strip}

# Keys
g810-led -dv 046d -dp c33c -tuk 1 -g fkeys $colorFKeys
g810-led -dv 046d -dp c33c -tuk 1 -g functions $colorFunctions
g810-led -dv 046d -dp c33c -tuk 1 -g numeric $colorNumeric
g810-led -dv 046d -dp c33c -tuk 1 -g arrows $colorFKeys
g810-led -dv 046d -dp c33c -tuk 1 -g keys $colorKeys
g810-led -dv 046d -dp c33c -tuk 1 -g modifiers $colorModifiers
