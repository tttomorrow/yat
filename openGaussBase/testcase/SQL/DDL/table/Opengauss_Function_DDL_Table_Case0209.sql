-- @testpoint: alter table对多个列设置联合主键，合理报错
drop table if exists hsf;
create table hsf(col1 int, col2 int,col3 int,col4 int);
create unique index test_hsf on hsf(col1,col2);
ALTER TABLE hsf ADD PRIMARY KEY(col1,col2);

ALTER TABLE hsf ADD PRIMARY KEY(col1,col3,col2);   --error

drop table if exists hsf;