-- @testpoint: round函数入参为空或者负数
drop table if exists tb;
create table tb (nem numeric);
insert into tb values ('');
insert into tb values (null);
insert into tb values (-9.56);
select round(nem) from tb;
drop table tb;