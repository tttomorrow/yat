-- @testpoint: 表与聚合函数,入参类型不符合，合理报错

drop table if exists tab136;
create table tab136 (id int,name char(20),class char(10),course char(20),score jsonb);
insert into tab136 values(4,'小明',1,'数学','[87.5]');
insert into tab136 values(2,'小红',2,'数学','[62]');
insert into tab136 values(1,'小蓝',1,'数学','[77.5]');
insert into tab136 values(2,'小黑',1,'数学','[97.5]');
insert into tab136 values(3,'小黄',2,'数学','[88]');
insert into tab136 values(5,'小紫',1,'数学','[57]');
insert into tab136 values(7,'小白',1,'数学','[100]');

--sum(expression)
select sum(score)fromtab136whereclass=2andcourse='数学';
--max(expression)
select max(score)fromtab136whereclass=2andcourse='数学';
--min(expression)
select min(score)fromtab136whereclass=2andcourse='数学';
--avg(expression)
select avg(score)fromtab136whereclass=1andcourse='数学';
--string_agg(expression, delimiter)
select string_agg(score,';') from tab136;
--count（）
select count(*) from tab136;
--array_agg(expression)
select array_agg(score) from tab136 ;
--bit_length(string)
select char_length(score) from tab136 ;
drop table if exists tab136;