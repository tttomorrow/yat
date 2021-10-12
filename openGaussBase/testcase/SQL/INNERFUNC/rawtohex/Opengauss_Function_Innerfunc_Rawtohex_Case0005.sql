-- @testpoint: rawtohex函数与order by联合使用
drop table if exists tb;
create table tb(id int,hex int);
insert into tb values(1,3),(4,5),(8,9);
select rawtohex(concat(id,hex)) from tb order by 1;
select rawtohex(concat_ws('',id,hex)) from tb order by 1;
drop table if exists tb;