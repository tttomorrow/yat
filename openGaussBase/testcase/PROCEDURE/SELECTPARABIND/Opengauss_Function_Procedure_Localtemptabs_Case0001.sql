-- @testpoint: 存储过程使用本地临时表插入数据

--创建测试表
drop table if exists proc_localtemptab_t_001;
create table  proc_localtemptab_t_001(id  int,name varchar(100),ctime date);
insert into proc_localtemptab_t_001 values (1,'proc_localtemptab_t_001','2020-11-24 16:10:28');

--创建临时表
create temporary table lsb_proc_localtemptab_t_001 as select * from proc_localtemptab_t_001;

--创建存储过程
create or replace procedure proc_localtemptab_001(str boolean) is
begin
insert into lsb_proc_localtemptab_t_001 values(1,'proc_localtemptab_t_001','2020-09-17 16:10:28');
end;
/
--调用存储过程
call proc_localtemptab_001(true);

--查看临时表数据
select * from lsb_proc_localtemptab_t_001;

--清理环境
drop procedure proc_localtemptab_001;
drop table proc_localtemptab_t_001;