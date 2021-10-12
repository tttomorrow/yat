-- @testpoint: opengauss关键字bitvar(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists bitvar_test;
create table bitvar_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists bitvar;
create synonym bitvar for bitvar_test;
insert into bitvar values (1,'ada'),(2, 'bob');
update bitvar set bitvar.name='cici' where bitvar.id=2;
select * from bitvar;

--清理环境
drop synonym if exists bitvar;

--关键字带双引号-成功
drop synonym if exists "bitvar";
create synonym "bitvar" for bitvar_test;
insert into "bitvar" values (1,'ada'),(2, 'bob');
update "bitvar" set "bitvar".name='cici' where "bitvar".id=2;
select * from "bitvar";

--清理环境
drop synonym if exists "bitvar";

--关键字带单引号-合理报错
drop synonym if exists 'bitvar';

--关键字带反引号-合理报错
drop synonym if exists `bitvar`;
drop table if exists bitvar_test;