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
	
print( "<hr><h1>Get Forecast</h1>" )

forecast_url = url,new_field_id,"/forecasts/",forecast_weather_start,",",forecast_weather_end,"?blockSize=24"

try:
	statusCode, headers, response = makeAPICall('GET', forecast_url, access_token )
	
except Exception as responseException:
	traceback.print_exc(file=sys.stdout)
	print( responseException )
	sys.exit(0)  
	
if statusCode == 200 :

	print( "<p>You requested ",len(response.forecasts)," days of forecast."
			,"The forecasted weather on "
			,strptime(response.forecasts[0].date, "%d %B, %Y")
			," is a high temperature of "
			,response.forecasts[0].forecast[0].temperatures.max,"&deg;" 
			,response.forecasts[0].forecast[0].temperatures.units
			," and a low of "
			,response.forecasts[0].forecast[0].temperatures.min,"&deg;"
			,response.forecasts[0].forecast[0].temperatures.units
			,"</p>" ) 
	print( "<p>Request:</p><pre>GET ",forecast_url,"</pre>" ) 
	print( "<p>Content-Range Header:</p>" )
	
	print( "<pre>",parseHTTPHeaders(headers,{"Content-Range"}),"</pre>" ) 
	print( "<p>Response Body:</p>" )
	print( "<pre>" ) 
	print( json.dumps(tenyr_response,sort_keys=True, indent=2) ) 
	print( "</pre>" ) 
	
else: 
	print( "<p>ERROR: ",statusCode," - ",response.simpleMessage,"<br>" )
	print( response.detailedMessage,"</p>" )
