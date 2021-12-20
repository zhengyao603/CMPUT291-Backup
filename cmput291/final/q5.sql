SELECT placeType, MAX(visit_count) as visits
FROM (SELECT locations.placeType, COUNT(visits.pid) as visit_count
      FROM locations, visits
      WHERE locations.latitude = visits.latitude
            AND locations.longitude = visits.longitude
      GROUP BY locations.placeType);