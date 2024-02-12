buildsystem=$1

go version &> /dev/null

if [ $? == 1 ]
then
    echo "Go not installed or not in \$PATH!"
    exit 1
fi

case $buildsystem in
    win64)
        x86_64-w64-mingw32-g++ --version &> /dev/null
        gppCode=$?
        x86_64-w64-mingw32-gcc --version &> /dev/null
        gccCode=$?
        if [ $gppCode -ne 0 ] && [ $gccCode -ne 0 ]; then
            echo "Install mingw to compile for Windows!"
            exit 1
        fi
        GOOS=windows GOARCH=amd64 CGO_ENABLED=1 CXX=x86_64-w64-mingw32-g++ CC=x86_64-w64-mingw32-gcc go build -o ./predict.so -buildmode=c-shared predict.go
        ;;
    linux)
        go build -o ./predict.so -buildmode=c-shared predict.go
        ;;
    -h)
        echo "This tool builds the predict.go file to a specified platform."
        echo "For Windows, the script requires mingw to be installed in \$PATH."
        exit 0
        ;;
    *)
        echo -e "Specify build option!\nPrint help using -h.\n\nCurrent options: win64, linux"
        exit 1
esac


if [ $? == 0 ]
then
    rm ./predict.h
    echo "Successful build!"
fi