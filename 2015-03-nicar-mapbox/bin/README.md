DATA PROCESSING
===========================
Keep in mind that the steps outlined below aren't definitve. If you are familiar with QGIS or a whiz at Excel and would prefer to do some of the steps differently, you should do it! There's no one definitive way in programming. My aim was simply to keep intermediary steps and outside programs to a minimum, while remaining somewhat beginner friendly.

### Cleaning Our Data in Five Steps
After some time spent hunting for a data set that lends itself well to chloropleth mapping, I found unemployment rates for 2013 at the county level [here](http://www.ers.usda.gov/data-products/county-level-data-sets/download-data.aspx). 
<ul>
<li><strong>Step One</strong>: Download and convert excel file to csv using csvkit (https://csvkit.readthedocs.org/en/0.8.0/index.html). <code>in2csv Unemployment.xls > unemployment-headers.csv</code></li>
<li><strong>Step Two</strong>: Remove extraneous header chatter with csvkit so the first row in the csv is column names. <code>cat unemployment-headers.csv | sed "1,6d" >unemployment-no-headers.csv</code></li>
<li><strong>Step Three</strong>: To get only the data points needed for our interactive, run <code>python clean.py</code>.</li>
<li><strong>Step Four</strong>: With our csv data formatted, it's now time to download a shapefile & join our csv data using our FIPS id.</li>
	<ul>
		<li><strong>First</strong>, navigate to https://www.census.gov/geo/maps-data/data/cbf/cbf_counties.html and download from 2013 this shp file: cb_2013_us_county_20m.zip. Save and unzip in our shp directory in bin. This shapefile is county level census data for 2013 at a resolution that will load nicely in the browser.</li>
		<li><strong>But beware!</strong> Puerto Rico is part of this shapefile and we're not showing data from Puerto Rico. So let's first filter it out using the magnificent ogr2ogr commandline tool: http://ben.balter.com/2013/06/26/how-to-convert-shapefiles-to-geojson-for-use-on-github/ (this will walk you through basic usage and installation). To filter out Puerto Rico, run this command in shp/cb_2013_us_county_20m <code>ogr2ogr -f 'ESRI Shapefile' -where "STATEFP NOT LIKE '%72'" filtered.shp cb_2013_us_county_20m.shp</code>. This will generate new filtered.* files.</li>
		<li><strong>Next</strong>, let's join our unemployment.csv to filtered.shp, as joining csv data to geojson cannot be done in a simple command line prompt. First, to avoid long paths, copy unemployment.csv in our bin directory into shp/cb_2013_us_county_20m. Now run this command inside bin/shp/cb_2013_us_county_20m<code>ogr2ogr -sql "select filtered.*, unemployment.* from filtered left join 'unemployment.csv'.unemployment on filtered.GEOID = unemployment.FIPS" joined.shp filtered.shp</code> Be patient. The command takes a few seconds to finish.</li>
		<li><strong>Next</strong>, let's convert our joined shapefile, joined.shp, to geojson so that it can be used by Mapbox Studio, TileMill and javascript. Run this command inside bin/shp/cb_2013_us_county_20m <code>ogr2ogr -f GeoJSON joined.geojson joined.shp</code></li>
	</ul>
<li><strong>Step Five</strong>: We must do one last thing to our data. Convert our unemployment rate, unemploy_3 to a float. If we don't do this Mapbox Studio and TileMill can't recognize our data.To do this, run this python script inside bin/shp/cb_2013_us_county_20m <code>python tonump.py</code> Finally data processing is done! Time to Map!</li>
</ul>
