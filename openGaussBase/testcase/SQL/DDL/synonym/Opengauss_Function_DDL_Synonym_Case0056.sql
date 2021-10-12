-- @testpoint: 同义词进行DML操作
-- @modify at: 2020-11-25
--建表
drop table if exists test_SYN_056;
create table test_SYN_056 (c_id int not null,c_first varchar2(40),c_since date,c_end timestamp,c_text clob,c_data blob);
--插入数据
--创建同义词
drop synonym if exists test_SYN_056;
create or replace synonym SYN_056_1 for test_SYN_056;
--通过同义词对表进行insert
select * from SYN_056_1 order by C_ID ;
--通过同义词删除表中数据
delete from SYN_056_1 where C_ID='1';
select * from SYN_056_1 order by C_ID ;
--通过同义词修改表中的数据
update SYN_056_1 set c_end='2020-07-08 14:22:59' where C_ID=2;
select * from SYN_056_1 order by C_ID ;
--清理环境
drop table test_SYN_056;
drop synonym SYN_056_1;