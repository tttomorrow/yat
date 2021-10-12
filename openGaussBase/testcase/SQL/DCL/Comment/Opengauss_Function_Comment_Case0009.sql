--- Case Type： Comment
--- Case Name： 在触发器上添加注释

--创建源表和触发表
drop table if exists trigger_comment1;
drop table if exists trigger_comment2;
create table trigger_comment1(id int,name varchar(10));
create table trigger_comment2(id int,name varchar(10));

--创建触发器函数
create or replace function tri_insert_func() returns trigger as
         $$
           declare
           begin
                   insert into trigger_comment1 values(NEW.id, NEW.name);
                   return new;
           end
           $$ language plpgsql;
/
--创建insert触发器
create trigger insert_trigger before insert on trigger_comment2 for each row execute procedure tri_insert_func();
/
--给触发器添加注释信息
comment on trigger insert_trigger on trigger_comment2 is '测试触发器注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_description where objoid=(select oid from pg_trigger where tgname='insert_trigger');

--清理环境
drop table trigger_comment1 cascade;
drop table trigger_comment2 cascade;


