from flask_restful import Resource, reqparse, request
import urllib
import storage
import os

import tempfile

try:
    import ogr

    drivers = {
        "shp": ogr.GetDriverByName('ESRI Shapefile'),
        "geojson": ogr.GetDriverByName('GeoJSON'),
        "gdb": ogr.GetDriverByName('openfilegdb'),
    }
except ImportError:
    ogr = None
    drivers = None


class ShpConvert:
    @staticmethod
    def isType(filenames):
        extensions = [os.path.splitext(filename)[1] for filename in filenames]
        return '.shp' in extensions

    @staticmethod
    def getDataSource(filenames, dir):
        return drivers['shp'].Open(dir, 0)

    dirSuffix = None


class GdbConvert:
    @staticmethod
    def isType(filenames):
        return 'gdb' in filenames

    @staticmethod
    def getDataSource(filenames, dir):
        return drivers['gdb'].Open(dir, 0)

    dirSuffix = ".gdb"


class GeoJsonConvert:
    @staticmethod
    def isType(filenames):
        extensions = [os.path.splitext(filename)[1] for filename in filenames]
        return '.json' in extensions or '.geojson' in extensions

    @staticmethod
    def getDataSource(filenames, dir):
        return drivers['geojson'].Open(dir, 0)

    dirSuffix = ".gdb"


readers = [ShpConvert, GdbConvert]


class ConvertUploadController(Resource):
    def post(self):
        if(drivers is None):
            return {
                "error": "GDAL not installed"
            }
        files = request.files.getlist('files')
        filenames = [file.filename for file in files]
        # print()

        reader = None
        for potential_reader in readers:
            if potential_reader.isType(filenames):
                reader = potential_reader
                break

        if reader is None:
            return {
                "error": "Type of files not found"
            }

        print(reader.dirSuffix)
        with tempfile.TemporaryDirectory(suffix=reader.dirSuffix) as tmpdirname:
            for file in files:
                file.save(os.path.join(tmpdirname, file.filename))
            print(len(files))
            print(tmpdirname)
            datasource = reader.getDataSource(filenames, tmpdirname)
            ids = []
            for layer in datasource:
                with tempfile.TemporaryDirectory() as tmpGeojson:
                    geojsonTempFile = os.path.join(tmpGeojson, 'temp.json')
                    ds = drivers['geojson'].CreateDataSource(geojsonTempFile)
                    ds.CopyLayer(layer, 'layer')
                    with open(geojsonTempFile, 'rb') as f:
                        id = storage.add_file(f)
                ids.append({
                    "id": id,
                    "name": layer.GetName()
                })

        return {"ids": ids}
