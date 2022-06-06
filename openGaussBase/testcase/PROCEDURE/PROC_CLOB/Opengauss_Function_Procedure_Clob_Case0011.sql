-- @testpoint: 存储过程clob数据类型的测试，clob和char/varchar类型的转换

drop table if exists proc_clob_table_011;
create table proc_clob_table_011(t1 int,t2 clob,t3 clob);
insert into proc_clob_table_011 values(1,'01010101111100000100000010000000100111111111字符串字符串字符串#￥%……&*（——）（*&……gv个国家级科技控股及港口价格可加工客','ukagcccccccfttttayyygdbbbbuyu7885445112');

--创建存储过程
create or replace procedure proc_clob_011() is
v1 char(8000);
v2 varchar(8000);
begin
    select t2 into v1 from proc_clob_table_011 where t1=1;
    select t3 into v2 from proc_clob_table_011 where t1=1;
    raise info 'result:%',rtrim(v1);
    raise info'result:%',v2;
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/
--调用存储过程
call proc_clob_011();

--恢复环境
drop procedure if exists proc_clob_011;
drop table if exists proc_clob_table_011;