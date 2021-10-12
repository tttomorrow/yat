-- @testpoint: 插入含时区time类型边界值

DROP TABLE IF EXISTS test_time11;
CREATE TABLE test_time11 (name time);
insert into  test_time11 values (time '00:00:00 PST');
insert into  test_time11 values (time '23:59:59 PST');
select * from test_time11;
DROP TABLE IF EXISTS test_time11;