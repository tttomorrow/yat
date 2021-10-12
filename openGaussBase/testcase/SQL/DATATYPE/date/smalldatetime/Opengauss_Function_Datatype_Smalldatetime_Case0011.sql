-- @testpoint: 结合截取函数，返回smalldatetime的日期部分

DROP TABLE IF EXISTS test_smalldatetime11;
CREATE TABLE test_smalldatetime11 (name smalldatetime);
insert into  test_smalldatetime11 values (trunc(smalldatetime '2018-09-16 11:22:33.456'));
select * from test_smalldatetime11;
DROP TABLE test_smalldatetime11;