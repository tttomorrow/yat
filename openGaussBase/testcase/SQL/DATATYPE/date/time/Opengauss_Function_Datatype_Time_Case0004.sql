-- @testpoint: 输入时间相减

DROP TABLE IF EXISTS test_time04;
CREATE TABLE test_time04 (name time);
insert into test_time04 values (time '21:21:17' - time '09:21:17');
select * from test_time04;
DROP TABLE test_time04;
