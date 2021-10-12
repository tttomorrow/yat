-- @testpoint: 删除数组array中所有的anyelement元素，element用select查询结果代替，部分合理报错

--创建数据
drop table if exists re06;
create table re06(id int,name varchar);
insert into re06 values(1,'Joe');
insert into re06 values(2,'Jim');
insert into re06 values(3,'Jay');
insert into re06 values(4,'Janne');
insert into re06 values(5,'Bob');
insert into re06 values(6,'Cherrs');
insert into re06 values(7,'Alexs');
insert into re06 values(8,'Lily');

--查询结果类型和数组中元素数据类型一致：删除成功
select array_remove(array[1,2,2,3],(select id from re06 where name = 'Jim'));
select array_remove(array[4,5,6,7,8,9],(select id from re06 where name = 'Jay'));
select array_remove(array[1,2,2,3],(select id from re06 where name = 'bob'));
select array_remove(array['Joe','Jim','Cherrs','Lily'],((select name from re06 where id = 2)::text));
select array_remove(array['Joe','Jim','Cherrs','Lily'],((select name from re06 where id = 4)::text));

--查询结果类型和数组中元素数据类型不一致：合理报错
select array_remove(array[1,2,2,3],(select name from re06 where id = 6));
select array_remove(array[1,2,3,4,5,6,7,8,9],(select id from re06));
select array_remove(array['Joe','Jim','Cherrs','Lily'],(select name from re06 where id = 7));

--清理环境
drop table if exists re06 cascade;