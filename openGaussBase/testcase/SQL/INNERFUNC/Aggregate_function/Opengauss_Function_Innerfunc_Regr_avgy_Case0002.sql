-- @testpoint: 函数regr_avgy(Y, X)，因变量的平均值 (sum(Y)/N)，当入参中有无效参数时，合理报错

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
insert into table_test values(1, '张三', 12, 156.23, 'sings', 12355551895),
(7, '李四', 15, 146.45, 'read books', 12866661265),
(3, '李华', 18, 160.55, 'Dancing', 11822220366),
(5, '赵六', 18, 170.55, 'Playing games', 13344443322);

--当入参中有非int类型参数时，合理报错
select regr_avgy(id, name)from  table_test where age <20;
select regr_avgy(id, hobbies)from  table_test where age <20;
select regr_avgy(name, hobbies)from  table_test where age <20;

--当有三个入参时合理报错
select regr_avgy(id, tel, height)from  table_test where age <20;
drop table table_test;
