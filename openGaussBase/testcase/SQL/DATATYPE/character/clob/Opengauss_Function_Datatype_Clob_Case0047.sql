-- @testpoint: 插入正常字符、中文、混合字符
-- @modified at: 2020-11-13


drop table if exists test_clob_047;
create table test_clob_047(id int,c_clob clob);
insert into test_clob_047 values(2,'abc');
insert into test_clob_047 values(3,'中国');
insert into test_clob_047 values(4,'123Gauss测试');
select * from test_clob_047;
drop table test_clob_047;

