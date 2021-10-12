-- @testpoint: interval时间间隔类型，天数和秒数精度不在范围内，合理报错

--创建表
drop table if exists interval02;
create table interval02 (name interval day(3) to second(2));

--插入数据
insert into interval02 values ('12356 2:25:4567');
insert into interval02 values ('123 24:25:456');

--清理环境
drop table interval02;
