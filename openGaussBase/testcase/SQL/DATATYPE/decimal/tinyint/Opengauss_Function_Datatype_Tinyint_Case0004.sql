-- @testpoint: 插入字符串类型整数

drop table if exists tinyint04;
create table tinyint04 (name tinyint);
insert into tinyint04 values ('12');
insert into tinyint04 values ('123');
insert into tinyint04 values ('1');
insert into tinyint04 values ('2');
insert into tinyint04 values ('3');
select * from tinyint04;
drop table tinyint04;
