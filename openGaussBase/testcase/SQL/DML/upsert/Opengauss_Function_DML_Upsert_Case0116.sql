--  @testpoint:建表，指定主键约束列的数据类型是数组,使用insert...update语句
 drop table if exists test_1;
--建表指定id列为主键约束且数据类型是数组
create table test_1
(
   name nvarchar2(20)  ,
   id int[] primary key ,
   address nvarchar2(50)
) ;

--常规insert插入一条数据
insert into test_1 values('a',array[1,2,3,4,5,6],'xian');
select * from test_1;
--使用insert...update语句,主键冲突，update主键，合理报错
insert into test_1 values('b',array[1,2,3,4,5,6],'dalian') ON duplicate key update  id=array[1,2,3,4,5,6];
----使用insert...update语句,主键冲突，update name列，原数据('a',array[1,2,3,4,5,6],'xian')更改为('b',array[1,2,3,4,5,6],'xian')
insert into test_1 values('b',array[1,2,3,4,5,6],'dalian') ON duplicate key update name='b';
select * from test_1;
--使用insert...update语句,主键不冲突，update name列，新增一条数据
insert into test_1 values('b',array[1,2,3,4,5],'dalian') ON duplicate key update name='b';
select * from test_1;
--使用insert...update语句,主键冲突，update name和address列，原数据('b',array[1,2,3,4,5],'dalian')更改为('c',array[1,2,3,4,5],'dalian1')
insert into test_1 values('c',array[1,2,3,4,5],'dalian1') ON duplicate key update name='c',address='dalian1';
select * from test_1;
drop table test_1;