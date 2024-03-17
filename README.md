# darshak
Yet another pdf viewer 

### Usage: 
darshak.py <filename\>

### Screenshot 

![demonstration pic](https://github.com/srbhp/solid-potato/raw/master/screenshot.png)

### Build

    ```bash
        pyinstaller pyinstaller_build.py -w --noconfirm  \
        --additional-hooks-dir=hooks --hidden-import PyQt5.QtXml\
        --name="darshak"  --onefile\
    ```

### TODO:

- [ ] add support to annotate
- 
- [ ] Table of contents
    - Highlight
    - Text notes
 
- [ ] Search Text 
- 
- [ ] Read aloud
- 
- [ ] Inking 
- 
- [ ] View and print local, online. 
- 
- [ ] Select Image from the viewer

