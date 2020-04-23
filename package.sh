cp *.py dist/linux
cp *.py dist/windows
cp *.py dist/osx

cd dist/linux
zip -r ../blender-rhubarb-lipsync-linux-3.0.0.zip *

cd ../windows
zip -r ../blender-rhubarb-lipsync-windows-3.0.0.zip *

cd ../osx
zip -r ../blender-rhubarb-lipsync-osx-3.0.0.zip *

cd ../..
