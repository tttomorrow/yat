-- @testpoint: sign函数与update结合使用
drop table if exists tb;
create table tb(a int,b int);
insert into tb values(1,1),(2,-1),(3,-6),(4,0);
update tb set b=888 where sign(b)<=-1;
select a,b from tb order by a;
drop table tb;