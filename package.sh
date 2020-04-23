cp *.py dist/linux
cp *.py dist/windows
cp *.py dist/osx

VERSION="$(grep -Po "__version__ = '\K[0-9\.]*"  __init__.py)"

cd dist/linux
zip -r "../blender-rhubarb-lipsync-linux-$VERSION.zip" *

cd ../windows
zip -r "../blender-rhubarb-lipsync-windows-$VERSION.zip" *

cd ../osx
zip -r "../blender-rhubarb-lipsync-osx-$VERSION.zip" *

cd ../..
