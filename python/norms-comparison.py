import testvars
import header
import string
import json
import time

api_key = ''
api_secret = ''
url = 'https://api.awhere.com/v2/weather/fields/'

print( "<h1>Get Access Token</h1>" )

try:
	access_token = GetOAuthToken(api_key, api_secret)
	
except Exception as accessException:
	print( accessException )
	sys.exit(0)  		
	
print( "<p>Access Token = $access_token</p>" )	   
	
print( "<hr><h1>Compare Recent Weather Observations to Long-Term Normals</h1>" )


month_day_start = observed_weather_start.strftime('%m-%d') 
month_day_end   = observed_weather_end.strftime('%m-%d') 

three_year_start_year   = (observed_weather_start+timedelta(years=-4)).strftime('%Y') 
ten_year_start_year     = (observed_weather_start+timedelta(years=-11)).strftime('%Y') 
end_year                = (observed_weather_start+timedelta(years=-1)).strftime('%Y') 

observed_weather_url = url,new_field_id,"/observations/",observed_weather_start,",",observed_weather_end,"?sort=-date","&units=usa"
						
three_year_norms_url = url,new_field_id,"/norms/",month_day_start,",",month_day_end,"/years/",three_year_start_year,",",end_year,"?sort=-day","&units=usa" 		

ten_year_norms_url = url,new_field_id,"/norms/",month_day_start,",",month_day_end,"/years/",ten_year_start_year,",",end_year,"?sort=-day","&units=usa"
	
	
try:
	obs_statusCode, obs_headers, obs_response = makeAPICall('GET', observed_weather_url, access_token )
	
	threeyr_statusCode, threeyr_headers, threeyr_response = makeAPICall('GET', three_year_norms_url, access_token )
	
	tenyr_statusCode, tenyr_headers, tenyr_response = makeAPICall('GET', ten_year_norms_url, access_token )

except Exception as responseException:
	traceback.print_exc(file=sys.stdout)
	print( responseException )
	sys.exit(0)  
	

if obs_statusCode == 200 and threeyr_statusCode == 200 and tenyr_statusCode == 200 :

	print( "<table>" )
	print( "<tr><th>Weather Attribute</th><th>Current Actual</th><th>3-Year Norm<br><small>",three_year_start_year,"&ndash;",end_year,"</small></th>" )
	print( "<th>10-Year Norm<br><small>",ten_year_start_year,"&ndash;",end_year,"</small></th></tr>" )

	for index in range(0,len(obs_response.observations)-1) :
	
		obsdata = obs_response[index]
		
		print( "<tr class=\"date-row\"><td colspan=\"4\">Comparing <b>"
			,strptime(obsdata.date, "%d %B, %Y")
			,"</b> to the averages of <b>"
			,threeyr_response.norms[index].day,"-",three_year_start_year," through "
			,threeyr_response.norms[index].day,"-",end_year,"</b> and <b>"
			,tenyr_response.norms[index].day,"-",ten_year_start_year," through "
			,tenyr_response.norms[index].day,"-",end_year,"</b>"
			,"</td></tr>" )
		
		print( "<tr>" ) 
		print( "<td>Max Temperature</td>" )
		print( "<td>",round(obsdata.temperatures.max,1),"&deg;",obsdata.temperatures.units,"</td>" ) 
		print( "<td>",round(threeyr_response.norms[index].maxTemp.average,1),"&deg;",threeyr_response.norms[index].maxTemp.units,"</td>" ) 
		print( "<td>",round(tenyr_response.norms[index].maxTemp.average,1),"&deg;",tenyr_response.norms[index].maxTemp.units,"</td>" ) 
		print( "</tr><tr>" )
		print( "<td>Min Temperature</td>" )
		print( "<td>",round(obsdata.temperatures.min,1),"&deg;",obsdata.temperatures.units,"</td>" ) 
		print( "<td>",round(threeyr_response.norms[index].minTemp.average,1),"&deg;",threeyr_response.norms[index].minTemp.units,"</td>" ) 
		print( "<td>",round(tenyr_response.norms[index].minTemp.average,1),"&deg;",tenyr_response.norms[index].minTemp.units,"</td>" ) 
		print( "</tr><tr>" )
		print( "<td>Precipitation</td>" )
		print( "<td>",round(obsdata.precipitation.amount,1),obsdata.precipitation.units,"</td>" ) 
		print( "<td>",round(threeyr_response.norms[index].precipitation.average,1),threeyr_response.norms[index].precipitation.units,"</td>" ) 
		print( "<td>",round(tenyr_response.norms[index].precipitation.average,1),tenyr_response.norms[index].precipitation.units,"</td>" ) 
		print( "</tr><tr>" )
		print( "<td>Max Humidity</td>" )
		print( "<td>",round(obsdata.relativeHumidity.max),"%</td>" ) 
		print( "<td>",round(threeyr_response.norms[index].maxHumidity.average),"%</td>" ) 
		print( "<td>",round(tenyr_response.norms[index].maxHumidity.average),"%</td>" ) 
		print( "</tr><tr>" )
		print( "<td>Min Humidity</td>" )
		print( "<td>",round(obsdata.relativeHumidity.min),"%</td>" ) 
		print( "<td>",round(threeyr_response.norms[index].minHumidity.average),"%</td>" ) 
		print( "<td>",round(tenyr_response.norms[index].minHumidity.average),"%</td>" ) 
		print( "</tr>" )
		
	print( "</table>" ) 
	
	print( "<p>Response Body for Observations:</p>" )
	print( "<pre>" ) 
	print( json.dumps(obs_response,sort_keys=True, indent=2) ) 
	print( "</pre>" ) 																
	
	print( "<p>Response Body for Three-Year-Norms:</p>" )
	print( "<pre>" ) 
	print( json.dumps(threeyr_response,sort_keys=True, indent=2) ) 
	print( "</pre>" ) 																
	
	print( "<p>Response Body for Ten-Year-Norms:</p>" )
	print( "<pre>" ) 
	print( json.dumps(tenyr_response,sort_keys=True, indent=2) ) 
	print( "</pre>" ) 	
	
	
else:

	if obs_statusCode != 200 :
			print( "<p>ERROR: ",obs_statusCode," - ",obs_response.simpleMessage,"<br>" )
			print( obs_response.detailedMessage,"</p>" )
			
	if threeyr_statusCode != 200 :
			print( "<p>ERROR: ",threeyr_statusCode," - ",threeyr_response.simpleMessage,"<br>" )
			print( threeyr_response.detailedMessage,"</p>" )
	
	if tenyr_statusCode != 200 :
			print( "<p>ERROR: ",tenyr_statusCode," - ",tenyr_response.simpleMessage,"<br>" )
			print( tenyr_response.detailedMessage,"</p>" )
	
	
