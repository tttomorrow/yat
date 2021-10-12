-- @testpoint: rpad函数与order by联用
drop table if exists tb;
create table tb(id text,name char(30));
insert into tb values('00001123','Curry'),('00001125','Selenia'),('00001128','hebe');
select id from tb order by rpad(name,15,'3');
drop table tb;