--  @testpoint:查询表的数据且去重

drop table if exists test_1;
create table test_1 (id int ,name char(20));
insert into test_1  values(1,'lily'),(2,'wilian'),(3,'lily');
select distinct on(name)id,name from test_1 order by name ;
drop table test_1;