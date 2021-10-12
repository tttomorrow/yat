-- @testpoint: 插入特殊字符

drop table if exists test_clob_055;
create table test_clob_055(c_clob clob);
insert into test_clob_055 values('$@#%……&*（)');
select * from test_clob_055;
drop table test_clob_055;
