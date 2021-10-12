-- @testpoint: 存储过程中动态语句创建本地临时表，插入数据，不调用存储过程查看临时表数据，合理报错

--建表插入数据
drop table if exists proc_localtemptab_t_007;
create table  proc_localtemptab_t_007(id  int,num numeric ,ctime date,name varchar(100));
insert into proc_localtemptab_t_007 values (1,12.3,'2020-11-24 16:10:28','jim');

--创建序列
drop sequence if exists proc_localtemptab_seq_008;
create sequence proc_localtemptab_seq_008 start with 100 increment by 10 maxvalue 200 cycle ;

--创建存储过程
create or replace procedure proc_localtemptab_007(k int ,j decimal)
is
begin
create temporary table lsb_proc_localtemptab_t_007 as select * from proc_localtemptab_t_007;
for i in 1..k
loop
insert into lsb_proc_localtemptab_t_007 values(proc_localtemptab_seq_008.nextval,mod(j,i),sysdate,'work'||i);
end loop;
end;
/
--查看临时表数据 报错
select * from lsb_proc_localtemptab_t_007;

--调用存储过程
call proc_localtemptab_007(5,2);

--再次查看临时表数据 成功
select id,num,name from lsb_proc_localtemptab_t_007;

--清理环境
drop procedure proc_localtemptab_007;
drop table proc_localtemptab_t_007;
drop sequence proc_localtemptab_seq_008;
