-- @testpoint: 插入空值
-- @modified at: 2020-11-16

drop table if exists test_nchar_07;
create table test_nchar_07 (id int,name nchar(8));
insert into test_nchar_07 values (1,'');
insert into test_nchar_07 values (1,null);
select * from test_nchar_07;
drop table test_nchar_07;