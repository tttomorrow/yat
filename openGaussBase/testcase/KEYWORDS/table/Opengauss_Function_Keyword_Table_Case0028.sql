-- @testpoint: opengauss关键字table(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists table_test;
create table table_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists table;
create synonym table for table_test;


--关键字带双引号-成功
drop synonym if exists "table";
create synonym "table" for table_test;
insert into "table" values (1,'ada'),(2, 'bob');
update "table" set "table".name='cici' where "table".id=2;
select * from "table";
drop synonym "table";
--关键字带单引号-合理报错
drop synonym if exists 'table';
create synonym 'table' for table_test;
insert into 'table' values (1,'ada'),(2, 'bob');
update 'table' set 'table'.name='cici' where 'table'.id=2;
select * from 'table';

--关键字带反引号-合理报错
drop synonym if exists `table`;
create synonym `table` for table_test;
insert into `table` values (1,'ada'),(2, 'bob');
update `table` set `table`.name='cici' where `table`.id=2;
select * from `table`;

--清理环境
drop table if exists table_test;
