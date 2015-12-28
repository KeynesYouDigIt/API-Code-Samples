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
	
print( "<hr><h1>Get Recent Weather Observations</h1>" )	

observed_weather_url = url,new_field_id,'/observations/',observed_weather_start,',',observed_weather_end

try:
	statusCode, headers, response = makeAPICall('GET', observed_weather_url, access_token )
	
except Exception as responseException:
	traceback.print_exc(file=sys.stdout)
	print( responseException )
	sys.exit(0)  
	
if statusCode == 200 : 
	
	print( "<p>You requested ",len(response.observations)," days of historical "
		,"observed weather. The weather on "
		,strptime(response.observations[0].date, "%d %B, %Y")
		," was a high temperature of "
		,response.observations[0].temperatures.max,"&deg;"
		,response.observations[0].temperatures.units
		," and a low of "
		,response.observations[0].temperatures.min,"&deg;"
		,response.observations[0].temperatures.units
		,"</p>" )
			
	print( "<p>Request:</p><pre>GET ",observed_weather_url,"</pre>" ) 
	print( "<p>Content-Range Header:</p>" )
	
	print( "<pre>",parseHTTPHeaders(headers,{"Content-Range"}),"</pre>" ) 
	print( "<p>Response Body:</p>" )
	print( "<pre>" ) 
	print( json.dumps(response,sort_keys=True, indent=2) ) 
	print( "</pre>" ) 															
	
else: 
	print( "<p>ERROR: ",statusCode," - ",response.simpleMessage,"<br>" )
	print( response.detailedMessage,"</p>" )
