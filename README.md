             _____
           /  ____  \      [ SYSTEM: SECURE ]
         /  /      \  \     [ NODE:   SANROKU-36  ]
        |  | (0)(0) |  |   
         \  \  __  /  /   
          \__\____/__/    
      ^       /    \       
     (  3   /      \    mm


Walla Walla?



                                          ***PREFACE***

This script is designed to create GPG format files that use AES256 encription standards.

It's a personal project I used to teach myself how to code in python. I wanted to start with something simple but then got a crazy idea. I know winrar, winzip, and 7z already exist 
and offer far better protection. This is not for profit. I only designed this program as an exercise in teaching myself.


That being said...



                                          ***WHAT DOES IT DO, SANROKU? GIMME THE INSTRUCTIONS!!***

WHen you run the script, you will see a very poor Ascii version of my hansdome mug. Below it, you will see a disclaimer. This does not keep the files that it encryoted after you decrypt those
same files. And below that, you will see the option to use "Lockup" or "Breaker"

If you choose Lockup, it will create a folder called "notes" if it doesn't already exist. Then it will ask you whch folder relative to the home directory(Just type the name of the folder inside the home folder and it will clone an encrypted copy inside 'notes') you want to encrypt. Then it will ask you for a password. *REMEMBER THIS PASSWORD!!* (Note: It will not delete the original folder. It will only copy the contents into a tar.gz.gpg file inside of the notes directory)

1) Select Option 1
2) Type the name relative to the home folder of your username /home/$user/<"name of the directory you want to encrypt a copy of">. You are not encrypting specific files using this. You are creating a copy of an entire folder recursively(**Everything** inside of it)
3) Give it a password
4) A tar.gz.gpg file of that folder will be inside. Encrypted.

If you choose Breaker, it will look inside the notes folder if it exists. If it doesn't, there will be "No vaults detected." The first option already created the vault. This allows you to unlock the file you locked using the Locker feature

1) Select Option 2
2) Select the number corresponding to the archive within the notes folder
3) Type the password
4) Type your sudo password
5) Use the GUI (or another CLI terminal if you like) to navigate over to the ~/temp_rest folder(/home/$user/temp_rest) and open temp_restore.tar.gz
6) Extract the contents into any folder of your choosing(within reason). Remember, you are extracting an entire folder. 
7) Press enter on the window you used to load the script once you're done. That will destroy the temp_rest folder and all of its contents, shredding it and everything inside of it.

Considerations
- I wanted to organize the encryption method and limit it to a specific folder to make my life easier. Thus allowing me to decrypt the copies exactly where I created them
- The volatility of the 'temp_rest' folder and its entire contents is a design choice. It saves on ram. I plan to automate this in later revisions so that you don't require digging into the actual temp_rest folder to get the file.
- Additionally, it uses RAM to create the contents. I picked the volatility as a feature to really enforce the ephemeral nature of the decryption part of the file. The temp_rest folder isn't an actual folder. It's a symlink to a temporary folder. That's why I *do not* recommend using files larger than 5GB for this project to copy and encrypt. 


                                      **INSTALLATION**



You will need Python to even run it. It will do absolutely nothing without it. Since I work in a Linux environment, I can only recommend you go to the official Python Website
if you choose to use this on Windows. I will not write a version for Windows merely because I don't particularly enjoy using Windows 11.

For Linux, it will depend on your distro, but most of them are deviations of Arch Linux, Debian/Ubuntu, and Fedora anyway.


For most distributions of Linux(Distros), this command should work:

In your distro, open your terminal(Pressing the ctrl + alt + T should do the trick).

Debian/Ubuntu:

sudo apt update && sudo apt upgrade -y

- All that really does is update your system without asking you to input Y/n as an answer.

sudo apt install python3

- Of course, you will need python to run it. Without it, the script will do nothing.

sudo apt install python3-pip

- And pip. You can't get any support packages without it. It allows the installation of modules that allow for most to get python to work its magic and do some cool things. But for the
standard user, you simply just type "pip install (module or program)" to add features. Pip doesn't automatically run. You have to type that in every time.

sudo apt install python3-dev python3-venv build-essential

- This is the meat and potatoes. This comes with some of the stuff you need to run Python. Test environments are important if you plan to code or test anything.



Fedora(And its derrivatives):

sudo dnf update && sudo dnf upgrade -y

sudo dnf install python3

sudo dnf install python3-pip

sudo dnf install python3-dev && sudo dnf install python3-venv && sudo dnf install build-essential


For ArchLinux:

sudo pacman -Syu

- Updates the system. Pretty standard

sudo pacman -S python

sudo pacman -S python-pip


Other Distros have other package managers. Read the manual for those ones.

Next:

pip install shutil

pip install tarfile

pip install getpass


These three commands will allow the script to do as it was intended to do. Create the tar.gz.gpg files.
