--  @testpoint:指定列按降序排序,name列按字母排序降序排列

drop table if exists test_1;
create table test_1 (id int ,name char(20));
insert into test_1  values(1,'lily'),(2,'wilian'),(3,'karia');
select * from test_1 order by name desc;
drop table test_1;