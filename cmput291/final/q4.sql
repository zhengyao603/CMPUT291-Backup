SELECT pid, latitude, longitude
FROM (SELECT visits.pid, visits.day as airport_date
	  FROM locations, visits
	  WHERE locations.latitude = visits.latitude
	        AND locations.longitude = visits.longitude
	        AND locations.placeName = 'Edmonton Airport')
     left outer join
     (SELECT visits.pid, locations.latitude, locations.longitude, visits.day as others_date
	  FROM locations, visits
	  WHERE locations.latitude = visits.latitude
	        AND locations.longitude = visits.longitude
	        AND locations.placeType <> 'residential'
	        AND locations.placeName <> 'Edmonton Airport') using (pid)
WHERE others_date <= datetime(airport_date, '+14 days')
      AND others_date >= airport_date;