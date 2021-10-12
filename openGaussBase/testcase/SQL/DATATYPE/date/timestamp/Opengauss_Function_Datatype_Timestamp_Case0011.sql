-- @testpoint: 结合截取函数，返回timestamp的日期部分

DROP TABLE IF EXISTS test_timestamp11;
CREATE TABLE test_timestamp11 (name TIMESTAMP);
insert into  test_timestamp11 values (trunc(TIMESTAMP '2018-09-16 11:22:33.456'));
select * from test_timestamp11;
DROP TABLE IF EXISTS test_timestamp11;