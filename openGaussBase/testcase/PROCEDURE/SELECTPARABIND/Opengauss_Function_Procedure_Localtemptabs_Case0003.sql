-- @testpoint: 存储过程中本地临时表更新数据，游标返回多结果集，删除临时表，调用合理报错

--创建测试表
drop table if exists proc_localtemptab_t_003;
create table  proc_localtemptab_t_003(id  int,num numeric ,ctime date);
insert into proc_localtemptab_t_003 values (1,12.3,'2020-11-24 16:10:28');

--创建临时表
create temporary table lsb_proc_localtemptab_t_003 as select * from proc_localtemptab_t_003;
select * from lsb_proc_localtemptab_t_003;

--创建存储过程
create or replace procedure proc_localtemptab_003(str boolean) is
cursor1 sys_refcursor;
begin
for i in 1..5
loop
insert into lsb_proc_localtemptab_t_003 values(i,12.5+i,add_months(to_date('2020-11-24 14:59:59'), i));
end loop;
for i in 1..5
loop
update lsb_proc_localtemptab_t_003 set num = num*10 + mod(num,i) where id = i;
end loop;
open cursor1 for select * from lsb_proc_localtemptab_t_003 order by id ,num;
end;
/
--调用存储过程
call proc_localtemptab_003(true);

--查看临时表数据
select * from lsb_proc_localtemptab_t_003 order by id ,num;

--删除临时表，调用报错
drop table lsb_proc_localtemptab_t_003;
call proc_localtemptab_003(true);

--再次创建，调用成功；
create temporary table lsb_proc_localtemptab_t_003 as select * from proc_localtemptab_t_003;
call proc_localtemptab_003(true);

--清理环境
drop procedure proc_localtemptab_003;
drop table proc_localtemptab_t_003;