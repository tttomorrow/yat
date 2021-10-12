-- @testpoint: opengauss关键字procedure(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists procedure_test;
create table procedure_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists procedure;
create synonym procedure for procedure_test;


--关键字带双引号-成功
drop synonym if exists "procedure";
create synonym "procedure" for procedure_test;
insert into "procedure" values (1,'ada'),(2, 'bob');
update "procedure" set "procedure".name='cici' where "procedure".id=2;
select * from "procedure";

--清理环境
drop synonym "procedure";

--关键字带单引号-合理报错
drop synonym if exists 'procedure';
create synonym 'procedure' for procedure_test;
insert into 'procedure' values (1,'ada'),(2, 'bob');
update 'procedure' set 'procedure'.name='cici' where 'procedure'.id=2;
select * from 'procedure';

--关键字带反引号-合理报错
drop synonym if exists `procedure`;
create synonym `procedure` for procedure_test;
insert into `procedure` values (1,'ada'),(2, 'bob');
update `procedure` set `procedure`.name='cici' where `procedure`.id=2;
select * from `procedure`;
--清理环境
drop table if exists procedure_test;