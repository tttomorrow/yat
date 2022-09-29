-- @testpoint: list分区个数测试，使用values in
--step1:分区个数等于64;expect:成功
drop table if exists tb_plugin0011;
create table tb_plugin0011(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p0 values in(0));

--step2:创建存储过程;expect:成功
create or replace procedure pro_plugin0011()
as
alter_str varchar;
begin
    for i in 1..63 loop
        alter_str = 'alter table tb_plugin0011 add partition p'||i|| ' values ('||i||');';
		execute immediate alter_str;
    end loop;
end;
/
call pro_plugin0011();

--step3:查看分区个数,等于64;expect:成功
select  count(boundaries) from pg_partition where parentid = (select parentid from pg_partition where relname = 'tb_plugin0011');

--step4:清理环境;expect:成功
drop table if exists tb_plugin0011;