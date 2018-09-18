# wps-app-server
Server for serving the wps web app client.

Because of the heavy lifting WPS required to handle the - pure web app is just not enough. 

The requirements of this server are:
  - Serve the WPS web app
  - Handle upload of geographic files in various of types
    - User upload from WPS web app
    - Output of WPS process 
  - Consume these geographic files as GeoJson
    - Web view in WPS web app
    - Input of WPS process

## Install instructions
  - Install python 3
  - Create a virtualenv with command : python -m venv venv
  - Activate virtualenv
    - Windows : venv\Scripts\activate
    - Mac and Ubuntu : . venv/bin/activate
  - Install dependencies : pip install -r requirements.txt

## API
  - Upload file from url
    - `POST`
    - `/api/urlUpload` 
    - Payload - `{"url":"http//...."}`
  - Upload geographic files in POST body
    - `POST`
    - `/api/convertUpload`
    - Payload - Form Data with files attached in `files`
  - Get file
    - `GET`
    - `/layer/{id}`
  - Get static files
    - `GET`
    - `./*`