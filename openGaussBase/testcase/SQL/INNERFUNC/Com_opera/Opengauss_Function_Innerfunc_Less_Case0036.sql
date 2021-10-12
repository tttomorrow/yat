-- @testpoint: opengauss比较操作符<,比较类型:UUID
drop table if exists ts_zhparser;
CREATE TABLE ts_zhparser(col UUID, col1 UUID);
INSERT INTO ts_zhparser VALUES('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11','a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12');
select col < col1 from ts_zhparser;
drop table if exists ts_zhparser;