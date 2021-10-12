-- @testpoint: openGauss保留关键字end作为触发器名，不带引号，部分测试点合理报错
--前提条件
--创建源表
drop table if exists test_trigger_src_tbl;
create table test_trigger_src_tbl(id1 int, id2 int, id3 int);

--创建触发表
drop table if exists test_trigger_des_tbl;
create table test_trigger_des_tbl(id1 int, id2 int, id3 int);

 -----创建触发器函数
 create or replace function tri_insert_func() returns trigger as
           $$
           declare
           begin
                   insert into test_trigger_des_tbl values(new.id1, new.id2, new.id3);
                   return new;
           end
           $$ language plpgsql;
 /


 --创建insert触发器，end作为作为触发器名，不带引号，合理报错

create trigger end
           before insert on test_trigger_src_tbl
           for each row
           execute procedure tri_insert_func();
/

--openGauss保留关键字end作为触发器名，加双引号，创建成功

create trigger "end"
           before insert on test_trigger_src_tbl
           for each row
           execute procedure tri_insert_func();
/
drop trigger "end" on test_trigger_src_tbl cascade;

--openGauss保留关键字end作为触发器名，加单引号，合理报错

create trigger 'end'
           before insert on test_trigger_src_tbl
           for each row
           execute procedure tri_insert_func();
/

 --openGauss保留关键字end作为触发器名，带反引号，合理报错

create trigger `end`
           before insert on test_trigger_src_tbl
           for each row
           execute procedure tri_insert_func();
/
drop table if exists test_trigger_src_tbl;
drop table if exists test_trigger_des_tbl;
drop function if exists tri_insert_func;


