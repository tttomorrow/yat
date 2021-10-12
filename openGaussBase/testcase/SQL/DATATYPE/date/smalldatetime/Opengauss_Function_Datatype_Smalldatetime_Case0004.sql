-- @testpoint: samlldatetime日期类型相减，合理报错

DROP TABLE IF EXISTS test_smalldatetime4;
CREATE TABLE test_smalldatetime4 (name smalldatetime);
insert into  test_smalldatetime4 values (smalldatetime '2018-09-17' -  smalldatetime '2018-09-16');
DROP TABLE test_smalldatetime4;
