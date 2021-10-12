-- @testpoint: 函数regr_r2(Y, X),相关系数的平方,入参为非int类型时，合理报错

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);

--当入参中有非int类型参数时，合理报错
select regr_r2(id, name)from  table_test where age <20;
select regr_r2(id, hobbies)from  table_test where age <20;
select regr_r2(name, hobbies)from  table_test where age <20;

--当有三个入参时合理报错
select regr_r2(id, tel, height)from  table_test where age <20;
drop table table_test;