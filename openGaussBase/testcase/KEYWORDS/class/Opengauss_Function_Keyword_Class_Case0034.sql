--  @testpoint:opengauss关键字class(非保留)，作为游标名
--前置条件
drop table if exists class_test cascade;
create table class_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor class for select * from class_test order by 1;
close class;
end;

--关键字带双引号-成功
start transaction;
cursor "class" for select * from class_test order by 1;
close "class";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'class' for select * from class_test order by 1;
close 'class';
end;

--关键字带反引号-合理报错
start transaction;
cursor `class` for select * from class_test order by 1;
close `class`;
end;

--清理环境
drop table class_test;