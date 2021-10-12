-- @testpoint: 相对时间间隔类型reltime,插入有效值

drop table if exists reltime01;
create table reltime01 (name reltime);
insert into reltime01 values ('9999 23:59:59');
insert into reltime01 values ('0000 00:00:00');
insert into reltime01 values ('123');
insert into reltime01 values ('23:45:56');
insert into reltime01 values ('-123');
select * from reltime01;
drop table reltime01;
