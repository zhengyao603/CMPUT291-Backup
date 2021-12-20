SELECT distinct locations.placeName, locations.placeType
FROM locations, visits, persons
WHERE locations.latitude = visits.latitude
      AND locations.longitude = visits.longitude
      AND visits.pid = persons.pid
      AND persons.name = 'John Smith';