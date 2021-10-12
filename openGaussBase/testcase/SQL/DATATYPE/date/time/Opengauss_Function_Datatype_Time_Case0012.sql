-- @testpoint: time没有输入时区

DROP TABLE IF EXISTS test_time12;
CREATE TABLE test_time12 (name time without time zone);
insert into  test_time12 values (time '00:00:00');
insert into  test_time12 values (time '12:59:59');
select * from test_time12;
DROP TABLE IF EXISTS test_time12;