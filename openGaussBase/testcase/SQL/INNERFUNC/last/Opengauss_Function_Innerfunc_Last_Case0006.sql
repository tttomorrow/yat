-- @testpoint: last函数在视图中的使用，部分合理报错

--建表
drop table if exists last06;
create table last06(
s_id integer(20),
s_name varchar(20) ,
s_birth date,
s_sex varchar(10));

--建视图1
drop view if exists fview1;
create view fview1 as select * from last06;
select * from fview1;

--表中未插入数据，使用last函数，返回一个空行
select last(s_id) from fview1;
select last(s_name) as name, last(s_id order by s_id nulls last ) as id
from fview1;
select last(s_birth) from fview1;
select last(s_sex), last(s_name) from fview1;

--nulls last 必须用在order by 后，否则合理报错
select last(s_name) as name, last(s_id nulls last ) from last06;

--表中插入数据
insert into last06 values (1,'zhaolei',null,'男');
insert into last06 values (2,'zhoumei','1991-12-01','女');
insert into last06 values (3,'zhuzhu','1991-06-01',null);
insert into last06 values (4,'lilei','1992-05-01','男');
insert into last06 values (null,'lihua','1991-03-01','男');
insert into last06 values (1,'zhangsan','1992-08-01','男');
insert into last06 values (2,'sunjin','1991-09-01','女');
insert into last06 values (3,'wangwu','1992-10-01','女');
insert into last06 values (4,null,'1990-11-01','女');
insert into last06 values (5,'ninghao','1993-12-01','女');

--建视图2
drop view if exists fview2;
create view fview2 as select * from last06;
select * from fview2;

--与group by，order by，having  结合使用
select  last(s_name order by s_id) from fview2;
select s_name, last(s_id) as id from fview2 group by s_name order by s_name;
select s_birth, last(s_id ) from fview2 group by s_birth order by s_birth;
select s_id, last(s_name) as name from fview2 group by s_id having s_id > 5 order by s_id;
select last(s_name order by s_id) from fview2 group by s_name;
select s_sex,last(s_birth) from fview2 group by s_sex order by s_sex;

--输入包含null，并排序(nulls last)
select last(s_name order by s_id nulls last) from fview2;
select s_id, last(s_birth order by s_birth  nulls last) from fview2 group by s_id order by s_id;

--与函数嵌套使用
select char_length(last(s_name order by s_name)) from fview2;
select isfinite(last(s_birth order by s_birth)) from fview2;
select last(s_id order by s_id nulls first)as id,first(s_name) as name  from last06;

--和聚合函数结合使用，合理报错
select count(last(s_id order by s_id)) from fview2;

--last函数入参不合理，合理报错
select last(s_id,s_name) from fview2;
select last(s_id,s_name) from last06;

--清理环境
drop view if exists fview1;
drop view if exists fview2;
drop table if exists last06 cascade;