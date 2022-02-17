# qrgenread

This script is able to generate QR-Codes, read QR-Codes from directory and detect QR-Codes live via Webcam.

The <code>main()</code>-function defines the primary arguments you should pass by console.

```python
if args[1] == "gen":
    generateQR(*args[2:])
elif args[1] == "read":
    readQR(*args[2:])
elif args[1] == "live":
    liveCapturingQR(*args[2:])
```
 
The secondary arguments are depended on the called function.

If you want to generate an QR-Code, you are able to set datas, filename, pixelcolor, backgroundcolor and the style (rounded or not). Just the datas-Argument is required. The other ones have defaults or generated filenames from the current timestamp.

```python
python qr.py gen https://github.com/binkertpat/qrgen respository
python qr.py gen https://github.com/binkertpat/qrgen respository black white rounded 
```

If you want to read QR-Codes there are two ways. The first way is copy & paste the Images in the <code>readQR</code>-directory. All these files are decoded automatic. You are able to call the function with a path, to your own directory. 

```python
python qr.py read                              
python qr.py read ./myQRcodes/awesomeCodes   
```

The last opportunity is decoding QR-Codes live via webcam. Over console, you call:

```python
python qr.py live   
```

After that, a new window is opening. This window shows the webcam image with the marked detected QR-Code. The decoded QR-Code data will print to the console.
