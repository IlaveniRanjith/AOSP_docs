# Pixel 6A

* ***Building And Flashing AOSP for Pixel 6A (Bluejay)***

## Preparing The Environment

* We need to keep our packages up to date to avoid errors due to older ones.

```cmd
sudo apt update
```

```cmd
sudo apt upgrade
```

## Installing Necessary Tools

* To build and flash our device we need some tools to convert source code into binary file for that we need to execute the below command.

```cmd
sudo apt install openssh-server screen python git openjdk-8-jdk android-tools-adb bc bison build-essential \
curl flex g++-multilib gcc-multilib gnupg gperf imagemagick lib32ncurses-dev lib32readline-dev lib32z1-dev \
liblz4-tool libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool \
squashfs-tools xsltproc yasm zip zlib1g-dev libtinfo5 libncurses5
```

## Downloading and setting the Repo Tool

* When we download Android source code from google, it has hundreds of git repositories. We need to handle those files for that we need a tool called repo tool, to download and set the path execute the following code.

```cmd
sudo wget 'https://storage.googleapis.com/git-repo-downloads/repo' -P /usr/local/sbin/
```

```cmd
sudo chmod a+x /usr/local/sbin/repo
```

* We can test the repo tool by typing ***repo***. If we get the following, it should work.
!!! new ""
    error: repo is not installed.  Use "repo init" to install it here. 

## Configure the git tools

* Now we need to Configure the git tools by executing following commands

```cmd
git config --global user.email "you@example.com"

git config --global user.name "Your Name"
```

## Downloading the AOSP source code.

* Create a folder in our system and download the aosp source code in it.
* Make a note of the branch and build the id of the device which we want to build and flash.
  * Build Information for Pixel 6A (Bluejay)
  * Branch : ***SD2A.220601.001.A1***
  * Build TAG: ***android-12.1.0_r12***

    For Code Names and branches see here [CodeNames](https://source.android.com/setup/start/build-numbers).

    For device specific vendor binaries see here [DriverBinaries](https://developers.google.com/android/drivers#bluejaysd2a.220601.001.a1 ).

* To create folder enter the following commands in terminal

```cmd
mkdir ~/AOSP_Root
```

* To change the directory from current directory

```cmd
cd ~/AOSP_Root
```

* This command will initialize the sources that are required for the branch mentioned after the b tag.

```cmd
repo init -u https://android.googlesource.com/platform/manifest -b android-12.1.0_r12
```

* If you are concern about space then use the following command with additional parameter ***"--depth=1"***

```cmd
repo init -u https://android.googlesource.com/platform/manifest -b android-12.1.0_r12 --depth=1
```

* By executing the following command you can download the source code

```cmd
repo sync -j30
```

!!! info "<span style="color:Red">*NOTE*</span>"
    ***The above command will take significant time depends upon the Internet speed and system configuration.***
<!-- <span style="color:Red">NOTE:</span> ***The above command will take significant time depends upon the Internet speed and system configuration.*** -->

* After downloading the source code you need to download the Device specific vendor binaries From here [DriverBinaries](https://dl.google.com/dl/android/aosp/google_devices-bluejay-sd2a.220601.001.a1-0145bbe6.tgz) and download the correct binary file using build id and branch.

* After downloading Binaries Place them in the ***AOSP_Root/*** directory and extract the tar zip file using the following command.

```cmd
tar -xzf google_devices-bluejay-sd2a.220601.001.a1-0145bbe6.tgz
```

* After extracting the above file you will get on shell script file named ***extract-google_devices-bluejay.sh***. execute the script file using following command.

```cmd
./extract-google_devices-bluejay.sh
```

* While executing these file, you need to type **I ACCEPT** when prompted in order to execute these successfully.

Now successfully downloaded the full source code now we need to Build the source code.

## Building the AOSP Source Code

!!! info "<span style="color:Red">*NOTE*</span>"
    Before executing below commands make sure you are in ***AOSP_Root/*** Directory.
<!-- <span style="color:Red">NOTE:</span> ***Before executing below commands make sure you are in*** **AOSP_Root/** ***Directory.*** -->

* By executing following command all essential definitions provided by envsetup.sh are loaded into the current shell.

```cmd
source build/envsetup.sh
```

* now you need to execute the following command to select the device specific build target.

```cmd
lunch
```

* the above command will show the list of avialable devices build targets you need to select your device specific target by typing corresponding number or name of the target ( in my case it is ***aosp_bluejay-userdebug*** )

```cmd
aosp_bluejay-userdebug
```

!!! info "<span style="color:Red">*NOTE*</span>"
    <span style="color:green"> ***do the below changes Specific to my branch and device***</span>
<!-- <span style="color:Red">**NOTE:**</span>  <span style="color:green"> ***do the below changes particular to my branch and device***</span> -->

* After lunch command execute the following command to build **otatools** which are required to build and package the flashable zip file.

```cmd
make otatools -j20
```

* After above command you need to modify the following file to build the **vendor-bootconfig.img** image file which is required in android 12 builds, but the target line is missing in my branch and device source code.

* File Path:  **AOSP_Root/build/make/core/Makefile**
* to open that file use the below commands in **AOSP_Root/** Terminal.

```cmd
cd build/make/core

gedit Makefile
```

* Once you opened the above file identify the following line
!!! new "" 
    ***$(BUILT_TARGET_FILES_PACKAGE): $(INTERNAL_VENDOR_RAMDISK_FRAGMENT_TARGETS)***

Add below line after above line. (<span style="color:Red">NOTE:</span> ***use "ctrl+f" to search the string.***)

```cmd
$(BUILT_TARGET_FILES_PACKAGE): $(INTERNAL_VENDOR_BOOTCONFIG_TARGET)
```

* Now goto the Root directory by typing the following command.

```cmd
croot
```

* Now execute the following command to build the source code

```cmd
make updatepackage -j20
```

!!! info "<span style="color:Red">*NOTE*</span>"
    ***The above command will take significant time depends upon the Internet speed and system configuration.***
<!-- <span style="color:Red">NOTE:</span> ***The above command will take significant time depends upon the Internet speed and system configuration.*** -->

* After successfull completion of building source code you will get flashable zip file in the following path ***out/target/product/bluejay/*** file named ***aosp_bluejay-img-eng.cdac.zip***.

* The above file you can flash on to the device using **adb and fastboot** tools.

## Flashing The AOSP source code.

* To flash you need unlock the bootloader of the device 

### Unlocking the Bootloader (Optional)

To unlock the bootloader of the device you have to follow below steps if not done before.

1. Enable the developer options by tapping 7 times on Build Number.
2. Then goto developer options and enable **OEM unlocking** toggle and **USB debugging** toggle also.
3. Then execute the following commands on the terminal by connecting device to system.
       *  After connecting device allow the prompt if any shows on the device by ticking the mark of **Always allow from this computer**
        ```cmd
        adb reboot bootloader
        ```
        
        ```cmd
        fastboot flashing unlock
        ```

4. by executing above commands on the device it will show prompt and press the *Volume keys* untill it shows **"Unlock the bootloader"** option and then press *Power* button to confirm.

5. then you can see in the device options <span style="color:Red">**Device state:Unlocked**</span>.
6. then execute the following command to go back to Homepage.
        ```cmd
        fastboot reboot
        ```

    *  now you succesfully unlocked the bootloader of the device.

### Flashing the Image file.

* To Flash image file executing the below commands in **AOSP_Root/** directory.

```cmd
adb reboot bootloader

fastboot -w update out/target/product/bluejay/aosp_bluejay-img-eng.cdac.zip
```

!!! danger "<span style="color:Red">*NOTE*</span>"
    ***Don't Remove your device until the above command executed sucessfully.***
<!-- <span style="color:Red">NOTE:</span> ***Don't Remove your device until the above command executed sucessfully.*** -->

* After successfull completion of above command you will redirect to Homepage of your device of custom ROM.
