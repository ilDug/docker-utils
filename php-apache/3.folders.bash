#!bash

# FOLDERS
folders="\
assets
assets/docs
assets/fonts
assets/images
assets/videos
dist
lib
lib/certs
lib/keys
lib/php
pages
pages/templates
pages/views
src
src/styles
src/scripts
src/typescript
src/typescript/classes
src/typescript/controllers
src/typescript/functions
src/typescript/interfaces
src/typescript/services
"
echo "$folders" | xargs mkdir

