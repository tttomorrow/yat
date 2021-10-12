-- @testpoint: opengauss关键字Lc_Ctype(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Lc_Ctype;
create synonym Lc_Ctype for explain_test;
insert into Lc_Ctype values (1,'ada'),(2, 'bob');
update Lc_Ctype set Lc_Ctype.name='cici' where Lc_Ctype.id=2;
select * from Lc_Ctype;

--关键字带双引号-成功
drop synonym if exists "Lc_Ctype";
create synonym "Lc_Ctype" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Lc_Ctype';
create synonym 'Lc_Ctype' for explain_test;
insert into 'Lc_Ctype' values (1,'ada'),(2, 'bob');
update 'Lc_Ctype' set 'Lc_Ctype'.name='cici' where 'Lc_Ctype'.id=2;
select * from 'Lc_Ctype';

--关键字带反引号-合理报错
drop synonym if exists `Lc_Ctype`;
create synonym `Lc_Ctype` for explain_test;
insert into `Lc_Ctype` values (1,'ada'),(2, 'bob');
update `Lc_Ctype` set `Lc_Ctype`.name='cici' where `Lc_Ctype`.id=2;
select * from `Lc_Ctype`;
--清理环境
drop synonym if exists lc_Ctype;
drop synonym if exists "Lc_Ctype";
drop table if exists explain_test;