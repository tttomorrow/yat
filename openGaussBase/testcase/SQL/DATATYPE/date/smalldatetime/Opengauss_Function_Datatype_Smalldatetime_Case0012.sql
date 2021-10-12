-- @testpoint: 输入smalldatetime日期类型，不指定时间

DROP TABLE IF EXISTS test_smalldatetime12;
CREATE TABLE test_smalldatetime12 (name smalldatetime);
INSERT INTO test_smalldatetime12 VALUES (smalldatetime '2018-09-16');
select * from test_smalldatetime12;
drop table test_smalldatetime12;