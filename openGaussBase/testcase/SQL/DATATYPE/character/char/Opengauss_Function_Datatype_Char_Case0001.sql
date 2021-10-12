-- @testpoint: 插入正常值(中、英文字符，数字)
-- @modify at: 2020-11-05


DROP TABLE IF EXISTS test_char_01;
CREATE TABLE test_char_01 (stringv char(20));
insert into test_char_01 values ('oh mygod');
insert into test_char_01 values ('测试');
insert into test_char_01 values (123);
select * from test_char_01;
drop table test_char_01;