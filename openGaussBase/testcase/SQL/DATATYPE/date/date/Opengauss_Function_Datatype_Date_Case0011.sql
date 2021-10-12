-- @testpoint: 日期类型相减,合理报错

DROP TABLE IF EXISTS test_date11;
CREATE TABLE test_date11 (name date);
insert into  test_date11 values (date'2018-09-17' - date'2018-09-16');
select * from test_date11;
DROP TABLE test_date11;