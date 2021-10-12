-- @testpoint: 存储过程中调用自定义函数本地临时表中插入数据，删除数据，游标返回多结果集，删除临时表，调用合理报错
--创建测试表
drop table if exists proc_localtemptab_t_004;
create table  proc_localtemptab_t_004(id  int,num numeric ,ctime date,name varchar(100));
insert into proc_localtemptab_t_004 values (1,12.3,'2020-11-24 16:10:28','jim');

--创建序列
drop sequence if exists proc_localtemptab_seq_004;
create sequence proc_localtemptab_seq_004 start with 100 increment by 10 ;

--创建临时表
create temporary table lsb_proc_localtemptab_t_004 as select * from proc_localtemptab_t_004;
select * from lsb_proc_localtemptab_t_004;

--创建函数
create or replace function proc_localtemptab_f_004(k int ,j decimal) return int
is
begin
for i in 1..k
loop
insert into lsb_proc_localtemptab_t_004 values(proc_localtemptab_seq_004.nextval,mod(j,i),add_months(to_date('2020-11-24 14:59:59'), i),'work'||i);
end loop;
return k;
end;
/
--调用函数
select proc_localtemptab_f_004(9,1.23);

--创建存储过程
create or replace procedure proc_localtemptab_004(str boolean) is
cursor1 sys_refcursor;
begin
open cursor1 for select * from lsb_proc_localtemptab_t_004 order by id ,num,name;
end;
/
--调用存储过程
call proc_localtemptab_004(true);

--查看临时表数据
select * from lsb_proc_localtemptab_t_004 order by id ,num,name;

--删除临时表，调用报错
drop table lsb_proc_localtemptab_t_004;
call proc_localtemptab_004(true);

--再次创建，调用成功；
create temporary table lsb_proc_localtemptab_t_004 as select * from proc_localtemptab_t_004;
call proc_localtemptab_004(true);

--清理环境
drop procedure proc_localtemptab_004;
drop table proc_localtemptab_t_004;
drop sequence proc_localtemptab_seq_004;
drop function proc_localtemptab_f_004;