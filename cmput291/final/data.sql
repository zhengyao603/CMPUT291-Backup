-- Let's drop the tables in case they exist
drop table if exists visits;
drop table if exists persons;
drop table if exists locations;

create table locations (
  latitude	float,
  longitude	float,
  placeName	text,
  placeType	text,
  primary key (latitude, longitude)
);

create table persons (
  pid           int,
  name          text,
  phone         text,
  homeLat       float,
  homeLong      float,
  primary key (pid),
  foreign key (homeLat, homeLong) references locations
);

create table visits (
  pid		int,
  latitude	float,
  longitude	float,
  day		date,
  primary key (pid, latitude, longitude, day),
  foreign key (pid) references persons,
  foreign key (latitude, longitude) references locations
);
  
PRAGMA foreign_keys = ON;

insert into locations values (53.5227, -113.5117, 'Remedy Coffee', 'restaurant');
insert into locations values (53.5207, -113.5251, 'UofA Hospital', 'hospital');
insert into locations values (53.3076, -113.5837, 'Edmonton Airport', 'transit');
insert into locations values (53.4873, -113.4936, 'Superstore at Calgary Trail', 'grocery');
insert into locations values (53.5240, -113.5232, 'UofA LRT station', 'transit');
insert into locations values (53.4561, -113.5165, 'Century LRT station', 'transit');
insert into locations values (53.5284, -113.5155, 'Kinsmen Park', 'park');
insert into locations values (53.5337, -113.5371, 'Emily Murphy Park', 'park');
insert into locations values (53.5199, -113.5113, NULL, 'residential');
insert into locations values (53.4599, -113.5626, NULL, 'residential');
insert into locations values (53.4579, -113.5188, NULL, 'residential');
insert into locations values (53.5101, -113.5091, NULL, 'residential');
insert into locations values (53.5218, -113.4489, NULL, 'residential');
insert into locations values (53.5121, -113.5290, NULL, 'residential');

insert into persons values (100, 'John Smith', '780-111-1111', 53.5199, -113.5113);
insert into persons values (200, 'Davood Rafiei', '780-222-2222', 53.4599, -113.5626);
insert into persons values (300, 'Andrew Fox', '780-222-3333', 53.4579, -113.5188);
insert into persons values (400, 'Brian Lin', '780-333-3333', 53.5101, -113.5091);
insert into persons values (500, 'Amir Salimi', '780-444-444', 53.5218, -113.4489);
insert into persons values (600, 'John Doe', '780-444-5555', 53.5121, -113.5290);

insert into visits values (100, 53.5227, -113.5117, '2020-03-20');	-- remedy
insert into visits values (100, 53.5240, -113.5232, '2020-03-25');	-- uofa transit
insert into visits values (100, 53.5240, -113.5232, '2020-03-27');	-- uofa transit
insert into visits values (100, 53.5337, -113.5371, '2020-03-26');	-- emily murphy

insert into visits values (200, 53.5337, -113.5371, '2020-03-26');	-- emily murphy
insert into visits values (300, 53.4873, -113.4936, '2020-03-25');	-- uofa transit
insert into visits values (400, 53.5227, -113.5117, '2020-03-20');	-- remedy

insert into visits values (100, 53.4561, -113.5165, '2020-03-18');	-- century lrt
insert into visits values (200, 53.4561, -113.5165, '2020-03-18');	-- century lrt
insert into visits values (300, 53.4561, -113.5165, '2020-03-18');	-- century lrt
insert into visits values (400, 53.4561, -113.5165, '2020-03-18');	-- century lrt
insert into visits values (500, 53.4561, -113.5165, '2020-03-18');	-- century lrt
insert into visits values (600, 53.4561, -113.5165, '2020-03-18');	-- century lrt
insert into visits values (200, 53.4873, -113.4936, '2020-03-16');	-- uofa transit
insert into visits values (400, 53.4873, -113.4936, '2020-03-16');	-- uofa transit
insert into visits values (500, 53.4873, -113.4936, '2020-03-16');	-- uofa transit
insert into visits values (600, 53.4873, -113.4936, '2020-03-16');	-- uofa transit

insert into visits values (200, 53.3076, -113.5837, '2020-02-25');	-- edmonton airort
insert into visits values (500, 53.3076, -113.5837, '2020-03-20');	-- edmonton airport
insert into visits values (500, 53.5218, -113.4489, '2020-03-21');	-- home
insert into visits values (600, 53.3076, -113.5837, '2020-03-20');	-- edmonton airport
insert into visits values (600, 53.4561, -113.5165, '2020-03-24');	-- century lrt
