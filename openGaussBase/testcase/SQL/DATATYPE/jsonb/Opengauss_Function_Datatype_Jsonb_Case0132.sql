-- @testpoint: 序列与包含jsonb类型的表

drop table if exists tab1321;
drop sequence if exists seq1 cascade;
drop table if exists tab1322;
create table tab1321(id serial,name jsonb);
create sequence seq1 cache 100;
create table tab1322(id int not null default nextval('seq1'),name jsonb);
insert into tab1322 values(0,'"json"');
insert into tab1322 (name) values('"jay"');
insert into tab1322 (name) values('"jack"');
select * from tab1322;
drop table if exists tab1322;
drop table if exists tab1321;
drop sequence if exists seq1 cascade;