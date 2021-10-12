-- @testpoint: 存储过程中本地临时表插入数据，游标返回多结果集，删除临时表，调用合理报错

--创建测试表
drop table if exists proc_localtemptab_t_002;
create table  proc_localtemptab_t_002(id  int,num numeric ,ctime date);
insert into proc_localtemptab_t_002 values (1,12.3,'2020-11-24 16:10:28');

--创建临时表
create temporary table lsb_proc_localtemptab_t_002 as select * from proc_localtemptab_t_002;
select * from lsb_proc_localtemptab_t_002;

--创建存储过程
create or replace procedure proc_localtemptab_002(str boolean) is
cursor1 sys_refcursor;
begin
for i in 1..5
loop
insert into lsb_proc_localtemptab_t_002 values(i,12.5+i,add_months(to_date('2020-11-24 14:59:59'), i));
end loop;
open cursor1 for select * from lsb_proc_localtemptab_t_002 order by id ,num;
end;
/
--调用存储过程
call proc_localtemptab_002(true);

--查看临时表数据
select * from lsb_proc_localtemptab_t_002;

--删除临时表，调用报错
drop table lsb_proc_localtemptab_t_002;
call proc_localtemptab_002(true);

--再次创建，调用成功；
create temporary table lsb_proc_localtemptab_t_002 as select * from proc_localtemptab_t_002;
call proc_localtemptab_002(true);

--清理环境
drop procedure proc_localtemptab_002;
drop table proc_localtemptab_t_002;