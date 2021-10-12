-- @testpoint: 表与聚合函数
drop table if exists temp_table_003;
create TEMPORARY table temp_table_003 (id int,name char(20),class char(10),course char(20),score float(1));

insert into temp_table_003 values(4,'小明',1,'数学',87.5);
insert into temp_table_003 values(2,'小红',2,'数学',62);
insert into temp_table_003 values(1,'小蓝',1,'数学',77.5);
insert into temp_table_003 values(2,'小黑',1,'数学',97.5);
insert into temp_table_003 values(3,'小黄',2,'数学',88);
insert into temp_table_003 values(5,'小紫',1,'数学',57);
insert into temp_table_003 values(7,'小白',1,'数学',100);
-- count（）
select count(*) from temp_table_003;
--sum(expression)
SELECT SUM(score) FROM temp_table_003 where class = 2 and course = '数学';
-- •max(expression)
SELECT max(score) FROM temp_table_003 where class = 2 and course = '数学';
-- •min(expression)
SELECT min(score) FROM temp_table_003 where class = 2 and course = '数学';
--•avg(expression)
SELECT avg(score) FROM temp_table_003 where class = 1 and course = '数学';
-- •array_agg(expression)
SELECT array_agg(name) FROM temp_table_003 ;
drop table if exists temp_table_003;