-- @testpoint: 替换数组array中所有的指定元素，element用select查询结果代替，部分合理报错

--创建数据
drop table if exists rep08;
create table rep08(id int,name varchar);
insert into rep08 values(1,'Joe');
insert into rep08 values(2,'Jim');
insert into rep08 values(3,'Jay');
insert into rep08 values(4,'Janne');
insert into rep08 values(5,'Bob');
insert into rep08 values(6,'Cherrs');
insert into rep08 values(7,'Alexs');
insert into rep08 values(8,'Lily');

--查询结果类型和数组中元素数据类型一致
select array_replace(array[1,2,2,3],(select id from rep08 where name = 'Jim'),(select id from rep08 where name = 'Cherrs'));
select array_replace(array[4,5,6,7,8,9],(select id from rep08 where name = 'Jay'),(select id from rep08 where name = 'Cherrs'));
select array_replace(array['Joe','Jim','Cherrs','Lily'],((select name from rep08 where id = 2)::text),((select name from rep08 where id = 5)::text));
select array_replace(array['Joe','Jim','Cherrs','Lily'],((select name from rep08 where id = 4)::text),((select name from rep08 where id = 5)::text));

--查询结果类型和数组中元素数据类型不一致：合理报错
select array_replace(array[1,2,2,3],(select name from rep08 where id = 6),6);
select array_replace(array[1,2,3,4,5,6,7,8,9],(select id from rep08),((select name from rep08 where id = 4)::text));
select array_replace(array['Joe','Jim','Cherrs','Lily'],(select name from rep08 where id = 7),10);

--清理环境
drop table if exists rep08 cascade;