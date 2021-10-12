-- @testpoint: 与max函数结合使用
drop table if exists test;
create table test(id int,name text);
insert into test values(1,'A'),(1,'c'),(1,'hodheuh;ifhkhoi'),(1,'一条大河波浪宽，风吹稻花香两岸'),(1,'OPENGAUSS');
select max(bit_length(name)) from test;
drop table if exists test;