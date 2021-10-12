-- @testpoint: pg_get_triggerdef(oid, boolean) 描述：获取触发器的定义信息

--创建源表和触发表
drop table if exists test_tb_trigger_001;
drop table if exists test_tb_trigger_002;
create table test_tb_trigger_001(id1 int, id2 int, id3 int);
create table test_tb_trigger_002(id1 int, id2 int, id3 int);

--创建触发器函数
create or replace function tri_truncate_func() returns trigger as
$$
declare
begin
	truncate test_tb_trigger_002;
	return old;
end
$$ language plpgsql;
/

--创建触发器
create trigger truncate_trigger before truncate on test_tb_trigger_001 execute procedure tri_truncate_func();
/
--获取触发器的定义信息
select pg_get_triggerdef(oid,true) from pg_trigger;

--清理环境
drop table test_tb_trigger_001;
drop table test_tb_trigger_002;
drop function tri_truncate_func();
