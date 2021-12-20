SELECT distinct pid, name, phone
FROM (SELECT locations.latitude, locations.longitude, visits.day as day1
	  FROM locations, visits, persons
	  WHERE locations.latitude = visits.latitude
	        AND locations.longitude = visits.longitude
	        AND visits.pid = persons.pid
	        AND persons.name = 'John Smith'
	        AND visits.day >= '2020-03-22')
     left outer join
     (SELECT persons.pid, persons.name, persons.phone, locations.latitude, locations.longitude, visits.day as day2
	  FROM locations, visits, persons
	  WHERE locations.latitude = visits.latitude
	        AND locations.longitude = visits.longitude
	        AND visits.pid = persons.pid) using (latitude, longitude)
WHERE day2 = day1;