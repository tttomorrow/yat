-- @testpoint: opengauss关键字within(非保留)，作为触发器名，部分测试点合理报错


--前置条件
--创建源表
drop table if exists test_trigger_src_tbl;
create table test_trigger_src_tbl(id1 int, id2 int, id3 int);
--创建触发表
drop table if exists test_trigger_des_tbl;
create table test_trigger_des_tbl(id1 int, id2 int, id3 int);

--创建触发器函数
create or replace function tri_insert_func() returns trigger as
$$
declare
begin
   insert into test_trigger_des_tbl values(new.id1, new.id2, new.id3);
   return new;
end
$$ language plpgsql;
/

--关键字explain作为作为触发器名，不带引号，创建成功
--创建insert触发器不带引号，创建成功
create trigger within before insert on test_trigger_src_tbl for each row execute procedure tri_insert_func();
/
drop trigger within on test_trigger_src_tbl cascade;

--关键字explain作为触发器名，加双引号，创建成功
--创建insert触发器带双引号，创建成功
create trigger "within" before insert on test_trigger_src_tbl for each row execute procedure tri_insert_func();
/
drop trigger "within" on test_trigger_src_tbl cascade;

--关键字explain作为触发器名，加单引号，合理报错
--创建insert触发器带单引号，合理报错
create trigger 'within' before insert on test_trigger_src_tbl for each row execute procedure tri_insert_func();
/

--关键字explain作为触发器名，带反引号，合理报错
--创建insert触发器带反单引号，合理报错
create trigger `within` before insert on test_trigger_src_tbl for each row execute procedure tri_insert_func();
/
drop table if exists test_trigger_src_tbl;
drop table if exists test_trigger_des_tbl;
drop function tri_insert_func;