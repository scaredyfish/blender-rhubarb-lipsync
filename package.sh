cp *.py dist/linux/blender-rhubarb-lipsync
cp *.py dist/windows/blender-rhubarb-lipsync
cp *.py dist/osx/blender-rhubarb-lipsync

VERSION="$(grep -Po "__version__ = '\K[0-9\.]*"  __init__.py)"

cd dist

cd linux
zip -r "../blender-rhubarb-lipsync-linux-$VERSION.zip" blender-rhubarb-lipsync

cd ../windows
zip -r "../blender-rhubarb-lipsync-windows-$VERSION.zip" blender-rhubarb-lipsync

cd ../osx
zip -r "../blender-rhubarb-lipsync-osx-$VERSION.zip" blender-rhubarb-lipsync

cd ..
