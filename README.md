# number-recognition-app
An interactable tkinter written number recognizer, using [Hukyl/mlgo](https://github.com/Hukyl/mlgo/) as shared library.

For training the neural network, refer to `Hukyl/mlgo`.


## Preparation

1. Install [Go 1.21+](https://go.dev/dl/) and [Python 3.10+](https://www.python.org/downloads/).

2. Install Go and Python dependencies.

3. Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html).

4. Train a neural network using [mlgo](https://github.com/Hukyl/mlgo/), or use a pretrained model dump (see `pretrained_models/`).

5. From Linux, build the .so file for desired platform (if building from Windows, see section Building).

```
$ ./compile.sh <build-option>
```

6. Create `.env` file in `gui/` folder.

```
SO_PATH="/path/to/built/from/go"
NN_DUMP_PATH="/path/to/model/dump.json"
GS_PATH="/path/to/ghostscript/executable"
```


## Running

To run, just enter the following command:
```
> python start.py
```

## Building

In case building for Windows from Linux, install `mingw`:

```
$ sudo apt-get update
$ sudo apt-get install gcc-mingw-w64  // for 64-bit architecture
```

When building from Windows for Windows, you can just run the following command:
```
> go build -o predict.so -buildmode=c-shared predict.go
```
