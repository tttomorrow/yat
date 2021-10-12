-- @testpoint: 使用循环插入100条数据
drop table if exists loop_t1;
create table loop_t1  (COL_2 int);
truncate table loop_t1;
begin
for i in 1..100 loop
insert into  loop_t1 values(10);
end loop;
end;
/

select * from loop_t1;
--清理环境
drop table if exists loop_t1 cascade;