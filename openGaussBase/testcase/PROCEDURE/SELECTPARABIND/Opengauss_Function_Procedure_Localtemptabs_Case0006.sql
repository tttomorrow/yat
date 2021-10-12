-- @testpoint: 存储过程中动态语句创建本地临时表，插入数据,修改表增加interv类型列，调用，查询 合理报错

--建表插入数据
drop table if exists proc_localtemptab_t_006;
create table  proc_localtemptab_t_006(id  int,num numeric ,ctime date,name varchar(100));
insert into proc_localtemptab_t_006 values (1,12.3,'2020-11-24 16:10:28','jim');

--创建序列
drop sequence if exists proc_localtemptab_seq_006;
create sequence proc_localtemptab_seq_006 start with 100 increment by 10 maxvalue 200 cycle;

--创建存储过程
create or replace procedure proc_localtemptab_006(k int ,j decimal)
is
begin
create temporary table lsb_proc_localtemptab_t_009 as select * from proc_localtemptab_t_006;
insert into lsb_proc_localtemptab_t_009 values(proc_localtemptab_seq_006.nextval,999.99,'2018-09-21','work'||k);
alter table lsb_proc_localtemptab_t_009 add column inter interval year to month;
insert into lsb_proc_localtemptab_t_009 values(proc_localtemptab_seq_006.nextval,999.999,'2018-09-21','工作'||k+1,numtoyminterval(9999.9, 'year'));
end;
/
--调用存储过程
call proc_localtemptab_006(5,2);

--查看临时表数据
select * from lsb_proc_localtemptab_t_009;

--清理环境
drop procedure proc_localtemptab_006;
drop table proc_localtemptab_t_006;
drop sequence proc_localtemptab_seq_006;