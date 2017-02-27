# gdal2mbtiles: Python-based tools for creating OGC MBTiles.
MBTiles Specification [[RU]](http://gis-lab.info/qa/mbtiles-spec.html), [[EN]](https://github.com/mapbox/mbtiles-spec)

# Introduction

* Combination of multiprocess [gdal2tiles](https://github.com/bolshoydi/gdal2tilesp) and [mbutil](https://github.com/mapbox/mbutil) 
in order to write tiles directly into Mbtiles database.
* Writing tiles without transitional (temporary) storage on disk
* Works in both ways: as CLI script and from interface. Just launch `window.py` from gui

# Requirements

* [GDAL 2.X.X](https://pypi.python.org/pypi/GDAL/)
* [PIL\Pillow] (https://pypi.python.org/pypi/Pillow/4.0.0)
* [PyQt4](https://pypi.python.org/pypi/PyQt4/4.11.4)

# Basic Usage

`python gdal2mbtiles.py input_file [options] -z min_zoom - maxzoom output.mbtiles`

  `gdal2mbtiles --help` to see list of available options:
  
  `--version` (Doesn't work)            show program's version number and exit
  
 `-h, --help  `          show this help message and exit
  
  `-p PROFILE, --profile=PROFILE`
                        Tile cutting profile (mercator,geodetic,raster) -
                        default 'mercator' (Google Maps compatible)
                        
  `-r RESAMPLING, --resampling=RESAMPLING`
                        Resampling method (average,near,bilinear,cubic,cubicsp
                        line,lanczos,antialias) - default 'average'
                        
  `-s SRS, --s_srs=SRS`   The spatial reference system used for the source input
                        data
                        
  `-z ZOOM, --zoom=ZOOM`  Zoom levels to render (format:'2-5' or '10').
  
  `-e, --resume`          Resume mode. Generate only missing files.
  
  `-a NODATA, --srcnodata=NODATA`
                        NODATA transparency value to assign to the input data
  `--processes=PROCESSES`
                        Number of concurrent processes (defaults to the number
                        of cores in the system)
                        
  `-v, --verbose`         Print status messages to stdout

 
## Web viewer options:
  
    Options for generated HTML viewers a la Google Maps

    `-w WEBVIEWER, --webviewer=WEBVIEWER`
                        Web viewer to generate
                        (all,google,openlayers,leaflet,index,metadata,none) -
                        default 'all'
    `-t TITLE, --title=TITLE`
                        Title of the map
    `-c COPYRIGHT, --copyright=COPYRIGHT`
                        Copyright for the map
    `-g GOOGLEKEY, --googlekey=GOOGLEKEY`
                        Google Maps API key from
                        http://code.google.com/apis/maps/signup.html
    `-y YAHOOKEY, --yahookey=YAHOOKEY`
                        Yahoo Application ID from
                        http://developer.yahoo.com/wsregapp/
## Config options:
  
    Options for config parameters

    `-x, --auxfiles`      Generate aux.xml files.
    
    `-f OUTPUT_FORMAT, --format=OUTPUT_FORMAT`
                        Image format for output tiles. Just PNG and JPEG
                        allowed. PNG is selected by default
                        
    `-o OUTPUT_CACHE, --output=OUTPUT_CACHE`
                        Format for output cache. Values allowed are tms and
                        xyz, being xyz the default value                       
                        

# Example
  `gdal2mbtiles.py input.tif -z 12-14 -a 0 output.mbtiles`
  
