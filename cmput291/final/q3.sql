SELECT locations.latitude, locations.longitude, locations.placeName, locations.placeType
FROM locations, visits
WHERE locations.latitude = visits.latitude
      AND locations.longitude = visits.longitude
GROUP BY visits.day
HAVING COUNT(visits.pid) > 5;