-- @testpoint: 插入中文
-- @modify at: 2020-11-17

drop table if exists test_varchar2_09;
create table test_varchar2_09 (name varchar2(20));
insert into test_varchar2_09 values ('gkb中国');
insert into test_varchar2_09 values ('中国gkb');
insert into test_varchar2_09 values ('开源数据库');
select * from test_varchar2_09;
drop table test_varchar2_09;