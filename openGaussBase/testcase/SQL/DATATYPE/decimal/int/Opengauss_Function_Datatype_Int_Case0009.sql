-- @testpoint: 插入0值

drop table if exists int09;
create table int09 (name int);
insert into int09 values (0);
insert into int09 values (0);
insert into int09 values (0);
select * from int09;
drop table int09;