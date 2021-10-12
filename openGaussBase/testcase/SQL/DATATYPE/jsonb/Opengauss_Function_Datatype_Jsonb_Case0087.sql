-- @testpoint: json额外支持操作函数：json_object_agg（将名字/值对聚集成一个 JSON 对象，当入参不合理时，合理报错）

--合理入参
drop table if exists classes;
create table classes(class int,name varchar,score float);
insert into classes values(1,'xiaoming',87.5),(3,'xiaowang',66),(3,'xiaozhang',90);
select json_object_agg(name,score) from classes group by name order by name;
select json_object_agg(class,score) from classes;
select json_object_agg(class,name) from (values(2,'xiaolong'),(3,'xiaolan'),(2,'fuqiang')) as xx (class,name);
select json_object_agg(k,v) from (values(1,1),(1,2),(2,2)) as xx(k, v) group by k;
select json_object_agg(k, v) from (values('a','m'),('w','s'),('q','a')) as xx(k, v) ;

--不合理入参：报错
select json_object_agg(score),name  from classes;
select json_object_agg(score) from classes;
select json_object_agg(name,scores) from class;
select json_object_agg(y,x) from (values(1,1),(1,2),(2,2)) as xx(k, v) group by k;

--清理数据
drop table classes;