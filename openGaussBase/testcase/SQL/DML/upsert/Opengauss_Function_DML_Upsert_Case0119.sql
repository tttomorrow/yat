--  @testpoint:使用upsert语句，对视图进行update，合理报错
drop table if exists test_5;
--建表指定id列为唯一约束且name列为数组类型
create table test_5
(
   name char[]  ,
   id int unique ,
   address nvarchar2(50)
) ;

--常规insert插入一条数据
insert into test_5 values(array['c','d','a'],3,'tianjin1');
select * from test_5;
--创建视图
drop view if exists myView;
CREATE VIEW myView AS SELECT * FROM test_5 WHERE address = 'tianjin1';
--视图使用upsert语句，合理报错
 insert into myView values(array['c','d','e'],3,'yunnan1'),(array['c','d','g'],4,'daqing1') ON duplicate key update name=EXCLUDED.name;
 --删除表
 drop table test_5 cascade;
 --删除视图
drop view if exists myView cascade;

