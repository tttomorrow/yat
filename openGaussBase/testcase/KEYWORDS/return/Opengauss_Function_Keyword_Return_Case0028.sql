-- @testpoint: opengauss关键字return(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists return_test;
create table return_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists return;
create synonym return for return_test;
insert into return values (1,'ada'),(2, 'bob');
update return set return.name='cici' where return.id=2;
select * from return;
drop synonym if exists return;

--关键字带双引号-成功
drop synonym if exists "return";
create synonym "return" for return_test;
insert into "return" values (1,'ada'),(2, 'bob');
update "return" set "return".name='cici' where "return".id=2;
select * from "return";
drop synonym if exists "return";

--关键字带单引号-合理报错
drop synonym if exists 'return';

--关键字带反引号-合理报错
drop synonym if exists `return`;
drop table if exists return_test;