-- @testpoint: sign函数与常用关键字结合使用
drop table if exists tb1;
create table tb1(a int,b int);
insert into tb1 values(1,234),(2,0),(3,-123),(4,-0),(4,-0);
select count(*) from tb1 where sign(b) = 1;
select distinct b from tb1 where sign(b) =1 order by b;
select a,b from tb1 union all select sign(a),sign(b) from tb1 order by a;
drop table tb1;
