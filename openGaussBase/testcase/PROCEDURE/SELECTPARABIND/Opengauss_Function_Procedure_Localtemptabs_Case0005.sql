-- @testpoint: 调用自定义函数本地临时表中插入数据，存储过程中游标fetch打印结果 删除临时表，调用合理报错
--创建测试表
drop table if exists proc_localtemptab_t_005;
create table  proc_localtemptab_t_005(id  int,num numeric ,ctime date,name varchar(100));
insert into proc_localtemptab_t_005 values (1,12.3,'2020-11-24 16:10:28','jim');

--创建序列
drop sequence if exists proc_localtemptab_seq_005;
create sequence proc_localtemptab_seq_005 start with 100 increment by 10 ;

create temporary table lsb_proc_localtemptab_t_005 as select * from proc_localtemptab_t_005;
select * from lsb_proc_localtemptab_t_005;

--创建函数
create or replace function proc_localtemptab_f_005(k int ,j decimal) return int
is
begin
for i in 1..k
loop
insert into lsb_proc_localtemptab_t_005 values(proc_localtemptab_seq_005.nextval,mod(j,i),add_months(to_date('2020-11-24 14:59:59'), i),'work'||i);
end loop;
return k;
end;
/
--调用函数
select proc_localtemptab_f_005(9,898);

--创建存储过程
create or replace procedure proc_localtemptab_005(str boolean) is
cursor1 sys_refcursor;
var_num numeric(10,2);
var_name varchar2(100);
begin
open cursor1 for select num,name from lsb_proc_localtemptab_t_005 order by id ,num,name;
loop
fetch cursor1 into var_num,var_name;
if cursor1%found then
   raise info 'num is=%',var_num;
   raise info 'name is=%',var_name;
else
  exit;
end if;
end loop;
end;
/
--调用存储过程
call proc_localtemptab_005(true);

--查看临时表数据
select * from lsb_proc_localtemptab_t_005 order by id ,num,name;

--删除临时表，调用报错
drop table lsb_proc_localtemptab_t_005;
select proc_localtemptab_f_005(9,898);
call proc_localtemptab_005(true);

--再次创建，调用成功；
create temporary table lsb_proc_localtemptab_t_005 as select * from proc_localtemptab_t_005;
select proc_localtemptab_f_005(9,898);
call proc_localtemptab_005(true);

--清理环境
drop procedure proc_localtemptab_005;
drop table proc_localtemptab_t_005;
drop sequence proc_localtemptab_seq_005;
drop function proc_localtemptab_f_005;