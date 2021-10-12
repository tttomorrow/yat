-- @testpoint: smalldatetime日期类型相加，合理报错

DROP TABLE IF EXISTS test_smalldatetime3;
CREATE TABLE test_smalldatetime3 (name smalldatetime);
insert into  test_smalldatetime3 values (smalldatetime '2018-09-17' +  smalldatetime '2018-09-16');
DROP TABLE test_smalldatetime3;