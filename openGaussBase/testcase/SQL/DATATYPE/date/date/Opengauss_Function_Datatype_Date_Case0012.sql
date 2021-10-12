-- @testpoint: 结合update，更新日期
-- @modified at: 2020-11-18

DROP TABLE IF EXISTS test_date12;
CREATE TABLE test_date12 (A INT,B DATE);
INSERT INTO test_date12 VALUES (1,DATE '2018-09-16');
update test_date12 set B = DATE '2088-09-01' where B = DATE '2018-09-16';
select A,B from test_date12 order by A;
drop table test_date12;