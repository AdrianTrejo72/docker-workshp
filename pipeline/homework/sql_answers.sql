--3
select count(1)
FROM public."green_tripdata_2025-11"  
WHERE trip_distance <= 1 limit 10;

--4 

select index, lpep_pickup_datetime, trip_distance, tip_amount, total_amount
FROM public."green_tripdata_2025-11" 
WHERE trip_distance < 100 order by 3 desc Limit 1;

--5

select 
    zone."Zone",
    sum(trip.total_amount) as suma --trip.total_amount, 
FROM public."green_tripdata_2025-11" as trip
    INNER JOIN public."taxi_zone_lookup" as "zone" ON trip."PULocationID" = zone."LocationID"
WHERE trip.lpep_pickup_datetime > '2025-11-18 00:00:00' 
group by zone."Zone" order by suma desc
Limit 1

--6
select  
    doz."Zone", trip."tip_amount"
FROM public."green_tripdata_2025-11" as "trip"
    INNER JOIN public."taxi_zone_lookup" as puz ON trip."PULocationID" = puz."LocationID"
    INNER JOIN public."taxi_zone_lookup" as doz ON trip."DOLocationID" = doz."LocationID"
WHERE puz."Zone" = 'East Harlem North'
ORDER BY trip."tip_amount" desc
Limit 1








