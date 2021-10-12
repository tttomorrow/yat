-- @testpoint: opengauss关键字select(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists select_test;
create table select_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists select;
create synonym select for select_test;


--关键字带双引号-成功
drop synonym if exists "select";
create synonym "select" for select_test;
insert into "select" values (1,'ada'),(2, 'bob');
update "select" set "select".name='cici' where "select".id=2;
select * from "select";

--清理环境
drop synonym "select";

--关键字带单引号-合理报错
drop synonym if exists 'select';
create synonym 'select' for select_test;
insert into 'select' values (1,'ada'),(2, 'bob');
update 'select' set 'select'.name='cici' where 'select'.id=2;
select * from 'select';

--关键字带反引号-合理报错
drop synonym if exists `select`;
create synonym `select` for select_test;
insert into `select` values (1,'ada'),(2, 'bob');
update `select` set `select`.name='cici' where `select`.id=2;
select * from `select`;
drop table if exists select_test;