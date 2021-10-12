-- @testpoint: rawtohex函数与group by联合使用
drop table if exists tb;
create table tb(hex2 int,b varchar2(20));
insert into tb values(2,'ab'),(4,'ef'),(8,'AB'),(2,'ab');
select rawtohex(to_char(hex2)),count(rawtohex(to_char(hex2))) from tb
group by rawtohex(to_char(hex2));
drop table if exists tb;