#code for parsing the mk files:-
from pymake import Makefile

# Load and parse a Makefile
makefile = Makefile("/home/cdac/disk1/Pixel_7A/AOSP_ROOT_android-13.0.0_r52/device/google/lynx/device-lynx.mk")

# Access targets, dependencies, and commands
for target in makefile.targets:
    print("Target:", target.name)
    print("Dependencies:", target.dependencies)
    print("Commands:", target.commands)


#code for iteration on target 

for target in makefile.targets:
    print("Target:", target.name)
    for rule in target.rules:
        print("Dependencies:", rule.dependencies)
        print("Commands:", rule.commands)