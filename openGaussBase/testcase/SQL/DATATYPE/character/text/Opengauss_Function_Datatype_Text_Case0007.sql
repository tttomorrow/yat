-- @testpoint: 插入特殊字符

drop table if exists test_text_07;
create table test_text_07(c_text text);
insert into test_text_07 values('$@#%……&*（)');
select * from test_text_07;
drop table test_text_07;