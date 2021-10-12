-- @testpoint: drop sequence if exists serial;
drop sequence if exists serial;
CREATE SEQUENCE serial START 101 CACHE 20;
drop sequence serial;