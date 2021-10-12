--  @testpoint:建表，使用insert...update..EXCLUDED语句和insert..nothing，更新数组列
 drop table if exists test_3;
--建表指定id列为主键约束且name列为数组类型
create table test_3
(
   name char[]  ,
   id int primary key ,
   address nvarchar2(50)
) ;

--常规insert插入一条数据
insert into test_3 values (array['a','b','c'],1,'xian');
select * from test_3;
--主键冲突，upadte name列，原数据(array['a','b','c'],1,'xian')更改为(array['c','d','e'],1,'xian')
insert into test_3 values(array['c','d','e'],1,'dalian') ON duplicate key update  name=EXCLUDED.name;
select * from test_3;
--主键不冲突，插入两条数据(array['c','d'],2,'dalian'),(array['c','d'],3,'dalian')
insert into test_3 values(array['c','d'],2,'dalian'),(array['c','d'],3,'dalian')ON duplicate key update name=EXCLUDED.name;
select * from test_3;
--插入两条数据，第一条主键冲突，第二条主键不冲突,更新已有数据(array['c','d'],2,'dalian')为(array['c','d'],2,'dali')且插入一条数据(array['c','d'],4,'dalian')
insert into test_3 values(array['c','d'],2,'dali'),(array['c','d'],4,'dalian')ON duplicate key update address=EXCLUDED.address;
select * from test_3;
--插入两条数据，主键均冲突，更改后的数据是(array['c','d','e'],2,'tianjin')和(array['c','d'],4,'dalian1')
insert into test_3 values(array['c','d','e'],2,'tianjin'),(array['c','d'],4,'dalian1') ON duplicate key update name=EXCLUDED.name, address=EXCLUDED.address;
select * from test_3;
 truncate test_3;
 --使用insert..nothing语句，插入两条数据，主键重复，插入一条数据(array['c','d','e'],2,'tianjin')
 insert into test_3 values(array['c','d','e'],2,'tianjin'),(array['c','d'],2,'dalian1') ON duplicate key update nothing;
 select * from test_3;
 --使用insert..nothing语句，插入两条数据，主键不重复，插入两条数据
 insert into test_3 values(array['c','d','e'],3,'tianjin'),(array['c','d'],4,'dalian1') ON duplicate key update nothing;
 select * from test_3;
 --使用insert..nothing语句，插入两条数据，第一条主键冲突，第二条主键不冲突，插入第二条数据(array['c','d'],5,'dalian1')
 insert into test_3  values(array['c','d','a'],3,'tianjin1'),(array['c','d'],5,'dalian1') ON duplicate key update nothing;
 select * from test_3;
 drop table test_3;