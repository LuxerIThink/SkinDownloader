<br/><br/><h1 align="center">SkinDownloader</h1>
<h3 align="center">Tool for download, manage and convert (from old to new type) multiple minecraft skins<h3/>
<h5 align="center">Only for windows<h5/><br/><br/>

## Who is it for?
This tool was designed for graphics designer to faster management with rendering multiple skins for many people frequently changing their skins, or with old type skins (64x32) in mineimator/blender or other rendering software.

## UI and its lack
This program is the console only, after the first run code generate options text type file with default configuration. In options file user can change path where skins will be saved 'PathForSkins:' (perhaps tool need administrator rights for this operation), path to file where you can write nicknames of the premium minecraft accounts which skins you want to download and options where the tool can add to saved skin file names a letter that means a type of skin, where "A" means "Alex" and "S" means "Steve"

## Skin converting from old type to new type and how it works
This software assumes 4 types of skins: Steve, OldSteve, Alex, OldAlex. Steve's and Alex's texture have dimensions 64x64. Old texture has only 32x32. OldSteve/OldSteve has 4 wide pixel arms, but Alex's/OldAlex's arms has only 3 pixel wide. Whether the skin is Alex/OldAlex or Steve/OldSteve type, we can check with MojangApi function. To check texture size we need use other method, becose MojangApi doeen't have funtion for that.
Skin converting part after download skin check the height of the texture. If skin texture height is 32px, texture will be converted. As MojangApi does not support skin converting from old to new type, I used the possibility of cutting out pices of the texture and pasting them in the right places with PIL part of Image Library . This operation is performed by the OldToNew function and changeTxt function. Old and New skins coordinates are saved in getOldTxtCoord and getNewTxtCoord functions, where there are 4 coordinates ( horizontal coordinate of upper left corner of image, vertical coordinate of upper left corner of image, horizontal coordinate of lower right corner of image, vertical coordinate of lower right corner of image) for every part of old skin (top texture, bottom texture, right texture/left texture, front texture, left texture/right texture, backTexture). After that converted skin is saved to file.

## Multitheading
To speed up your work I added basic multheading. Every thead of your processor deals with one skin asynchronous. When thead finish operation on actual skins, get another one. This solution can decrease time of code working few times. A library theading was used for it. Multitheading is used in mainFunction with Queue for it.

## Project tree:
Used libraries: mojang from MojangAPI, requests, os, PIL from Image, io from BytesIO, numpy, sys, time, queue from Queue, theading, itertools from islice

### Functions:
- optionsLoc - options file location
- defSkinsLoc - default location for skins download folder
- defNicknamesLoc - default location for nicknames texy dile
- defPrefix - default option for adding skin type prefix for skin filename
- genOptions - generate options file with default configuration
- genExampleNickNameFile - generation example skin nicknames file
- str2bool - converting string type boolean text to boolean
- LoadOptions - generating default options file, loading options from file, generating folders, check problems with folders, files and options
- getOldTxtCoord - old texture coordinates of skin body parts
- getNewTxtCoord - new texture coordinates of skin body parts
- changeTxt - function to rotating, croping and pasting texture from old skinf ile to new one
- OldToNew - creating new empty file, create temp texture from old texture, callling changeTxt function for each part of skin
- addPrefix - fucntion for adding skin type prefix for skin filename if this is option is turned on
- downloadSkin - skin download, check skin height (can call OldtoNew function)
- mainFunction - main Function for every operation (loading options, and menages the theading queue)
