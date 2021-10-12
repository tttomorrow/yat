-- @testpoint: 创建表与序列

drop table if exists T1;
CREATE TABLE T1(id serial,name text);

DROP SEQUENCE if exists seq1 cascade;
drop table if exists T2;
CREATE SEQUENCE seq1 cache 100;
CREATE TEMPORARY TABLE T2
(id   int not null default nextval('seq1'),name text);
insert into T2 values(1,'2');
insert into T2 (name) values('3');
insert into T2 (name) values('6');
select * from T2;
drop table if exists T2;
DROP SEQUENCE if exists seq1 cascade;