-- @testpoint: 自定义函数同义词与窗口函数结合使用
-- @modify at: 2020-11-25
--建自定义函数
drop function if exists SYN_FUN_001(c bigint) cascade;
create or replace function SYN_FUN_001(c int)return number
as
b int := c;
begin
    for i in 1..c loop
        b:= b*1;
    end loop;
    return b;
end;
/
--建自定义函数同义词
drop synonym if exists SYN_FUN_SYN_001;
create or replace synonym SYN_FUN_SYN_001 for SYN_FUN_001;
--创建函数
drop function if exists SYN_FUN_002(c bigint);
create or replace function SYN_FUN_002(c bigint) return int
as
b int := c;
begin
    for i in 1..c loop
        b:= b - 1;
    end loop;
    return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_002;
create or replace synonym SYN_FUN_SYN_002 for SYN_FUN_002;
--创建函数
drop function if exists SYN_FUN_003(c bigint);
create or replace function SYN_FUN_003(c bigint) return int
as
b int := c;
begin
    for i in 1..c loop
        b:= b*1;
    end loop;
    return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_003;
create or replace synonym SYN_FUN_SYN_003 for SYN_FUN_003;
--创建函数
drop function if exists SYN_FUN_004;
create or replace function SYN_FUN_004(c bigint)return int
as
b int := c;
begin
    for i in 1..c loop
        b:= b / 1;
    end loop;
    return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_004;
create or replace synonym SYN_FUN_SYN_004 for SYN_FUN_004;
--建表
drop table if exists SYN_TAB_020 cascade;
create table SYN_TAB_020
(
    id int,
    name varchar2(10),
    sal number
);
--插入数据
insert into SYN_TAB_020 values(1,'aaa',2600);
insert into SYN_TAB_020 values(1,'bbb',2600);
insert into SYN_TAB_020 values(2,'ccc',2800);
insert into SYN_TAB_020 values(3,'ddd',3000);
insert into SYN_TAB_020 values(3,'fff',3000);
insert into SYN_TAB_020 values(4,'eee',3200);
--查询
select name,sal,max(SYN_FUN_SYN_001(SYN_FUN_SYN_002(SYN_FUN_SYN_003(SYN_FUN_SYN_004(-1))))) over (partition by id order by id) from SYN_TAB_020;
select name,sal,min(SYN_FUN_SYN_001(SYN_FUN_SYN_002(SYN_FUN_SYN_003(SYN_FUN_SYN_004(-1))))) over (partition by id order by id) from SYN_TAB_020;
--清理环境
drop function if exists SYN_FUN_001(c bigint) cascade;
drop function if exists SYN_FUN_002(c bigint) cascade;
drop function if exists SYN_FUN_003(c bigint) cascade;
drop function if exists SYN_FUN_004(c bigint) cascade;
drop synonym if exists SYN_FUN_SYN_001;
drop synonym if exists SYN_FUN_SYN_002;
drop synonym if exists SYN_FUN_SYN_003;
drop synonym if exists SYN_FUN_SYN_004;
DROP TABLE if EXISTS SYN_TAB_020 CASCADE;
