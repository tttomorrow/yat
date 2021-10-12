-- @testpoint: opengauss关键字cobol(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists cobol_test;
create table cobol_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists cobol;
create synonym cobol for cobol_test;
insert into cobol values (1,'ada'),(2, 'bob');
update cobol set cobol.name='cici' where cobol.id=2;
select * from cobol;

--清理环境
drop synonym if exists cobol;

--关键字带双引号-成功
drop synonym if exists "cobol";
create synonym "cobol" for cobol_test;
insert into "cobol" values (1,'ada'),(2, 'bob');
update "cobol" set "cobol".name='cici' where "cobol".id=2;
select * from "cobol";

--清理环境
drop synonym if exists "cobol";

--关键字带单引号-合理报错
drop synonym if exists 'cobol';

--关键字带反引号-合理报错
drop synonym if exists `cobol`;
drop table if exists cobol_test;