-- @testpoint: opengauss关键字transactions_rolled_back(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists transactions_rolled_back;
create synonym transactions_rolled_back for explain_test;
insert into transactions_rolled_back values (1,'ada'),(2, 'bob');
update transactions_rolled_back set transactions_rolled_back.name='cici' where transactions_rolled_back.id=2;
select * from transactions_rolled_back;
drop synonym if exists transactions_rolled_back;

--关键字带双引号-成功
drop synonym if exists "transactions_rolled_back";
create synonym "transactions_rolled_back" for explain_test;
drop synonym if exists "transactions_rolled_back";

--关键字带单引号-合理报错
drop synonym if exists 'transactions_rolled_back';
create synonym 'transactions_rolled_back' for explain_test;
insert into 'transactions_rolled_back' values (1,'ada'),(2, 'bob');
update 'transactions_rolled_back' set 'transactions_rolled_back'.name='cici' where 'transactions_rolled_back'.id=2;
select * from 'transactions_rolled_back';

--关键字带反引号-合理报错
drop synonym if exists `transactions_rolled_back`;
create synonym `transactions_rolled_back` for explain_test;
insert into `transactions_rolled_back` values (1,'ada'),(2, 'bob');
update `transactions_rolled_back` set `transactions_rolled_back`.name='cici' where `transactions_rolled_back`.id=2;
select * from `transactions_rolled_back`;

--清理环境
drop table if exists explain_test;