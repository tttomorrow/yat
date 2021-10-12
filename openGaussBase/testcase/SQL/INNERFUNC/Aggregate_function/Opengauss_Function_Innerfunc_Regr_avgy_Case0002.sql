-- @testpoint: 函数regr_avgy(Y, X)，因变量的平均值 (sum(Y)/N)，当入参中有无效参数时，合理报错

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);

--当入参中有非int类型参数时，合理报错
select regr_avgy(id, name)from  table_test where age <20;
select regr_avgy(id, hobbies)from  table_test where age <20;
select regr_avgy(name, hobbies)from  table_test where age <20;

--当有三个入参时合理报错
select regr_avgy(id, tel, height)from  table_test where age <20;
drop table table_test;
