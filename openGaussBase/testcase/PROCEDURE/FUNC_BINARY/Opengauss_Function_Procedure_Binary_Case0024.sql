-- @testpoint: BINARY类型的测试———测试RAW类型

drop table if exists FVT_PROC_BINARY_TABLE_006;
create table FVT_PROC_BINARY_TABLE_006(T1 INT,T2 RAW(100));
INSERT INTO FVT_PROC_BINARY_TABLE_006 VALUES(1,'FF098');

--创建自定义函数
create or replace function FVT_PROC_BINARY_006() return RAW
is
V1 RAW(100);
begin
    select T2 into V1 from FVT_PROC_BINARY_TABLE_006 where T1=1;
    return V1;
    EXCEPTION
    WHEN NO_DATA_FOUND THEN  raise info 'NO_DATA_FOUND';
end;
/

--调用自定义函数
select FVT_PROC_BINARY_006();

update FVT_PROC_BINARY_TABLE_006 set T2='FFFFDDD' where T1=1;
--调用自定义函数
select FVT_PROC_BINARY_006();

--恢复环境
drop table if exists FVT_PROC_BINARY_TABLE_006;
drop function if exists FVT_PROC_BINARY_006;

