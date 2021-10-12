-- @testpoint: 输入时间相加，合理报错

DROP TABLE IF EXISTS test_time03;
CREATE TABLE test_time03 (name time);
insert into  test_time03 values (time '11:21:17' + time '09:21:17');
DROP TABLE test_time03;