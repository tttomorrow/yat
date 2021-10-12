--  @testpoint:delete语法，alias选项测试，不符合标识符命名规范，合理报错
--建表
drop table if exists t_delete01;
create table t_delete01(id int,name varchar(10));
--插入数据
insert into t_delete01 (id) values(generate_series(1,100));
--删除表数据，指定alias参数，别名由数字开头,合理报错
delete from t_delete01 as 1_delete01$;
--删除表数据，指定alias参数，别名以()开头，省略as选项，合理报错
delete from t_delete01 ()_delete01$;
--删除表数据，指定alias参数，别名以汉字开头，未报错，删除成功(和pg一致)
delete from t_delete01 as 删除_delete01$;
--删除表
drop table t_delete01;