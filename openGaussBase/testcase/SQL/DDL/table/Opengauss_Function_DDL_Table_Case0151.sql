-- @testpoint: 创建列类型是文本搜索类型的表
drop table if exists table_2;
create table table_2(a tsvector,b tsquery);
insert into table_2 values('qwerrttyyutuyi','23redrvxcvvfhtyuhn6ty');
select * from table_2;
drop table if exists table_2;