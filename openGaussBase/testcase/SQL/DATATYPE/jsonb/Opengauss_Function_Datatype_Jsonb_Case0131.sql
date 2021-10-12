-- @testpoint: 结合触发器使用jsonb数据类型

drop table if exists tab1311;
drop table if exists tab1312;
create  table tab1311(id int,name jsonb,sal number);
create  table tab1312(id int,name jsonb,sal number);
--创建触发器函数
create or replace function tri_insert_func() returns trigger as
           $$
           declare
           begin
               insert into tab1311 values(new.id, new.name, new.sal);
               return new;
           end
           $$ language plpgsql;
/
--创建触发器
create trigger table_trigger
           before insert on tab1312
           for each row
           execute procedure tri_insert_func();
/
--插入数据，调用触发器
insert into tab1312 values(1,'"aaa"',2600);
insert into tab1312 values(2,'null',2600);
insert into tab1312 values(3,'852',2800);
select * from tab1312;
select * from tab1311;
drop trigger table_trigger on tab1312;
drop function tri_insert_func()cascade;
drop table if exists tab1311;
drop table if exists tab1312;