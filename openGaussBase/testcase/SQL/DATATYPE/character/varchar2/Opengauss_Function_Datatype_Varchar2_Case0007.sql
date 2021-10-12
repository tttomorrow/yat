-- @testpoint: 插入空值
-- @modify at: 2020-11-17

drop table if exists test_varchar2_07;
create table test_varchar2_07 (id int,name varchar2(8));
insert into test_varchar2_07 values (1,'');
insert into test_varchar2_07 values (2,null);
select * from test_varchar2_07;
drop table test_varchar2_07;