-- @testpoint: 创建jsonb类型字段的表，并设置缺省值为"null"

drop table if exists tab134;
create table tab134
(
    sk         integer          not null,
    id         char(16)         not null,
    name       varchar(20),
    state                jsonb          default '"null"'
);
insert into  tab134 values(1,'a','xiaoming','"job"');
insert into  tab134(sk,id,name) values(2,'b','xiaohong');
insert into  tab134 values(3,'c','lihua','"job"');
insert into  tab134(sk,id,name) values(4,'d','zhangsan');
select * from tab134;
drop table if exists tab134;
