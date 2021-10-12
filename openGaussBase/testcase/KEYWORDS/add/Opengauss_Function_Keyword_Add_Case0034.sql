--  @testpoint:opengauss关键字add(非保留)，作为游标名
--前置条件
drop table if exists add_test cascade;
create table add_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor add for select * from add_test order by 1;
close add;
end;

--关键字带双引号-成功
start transaction;
cursor "add" for select * from add_test order by 1;
close "add";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'add' for select * from add_test order by 1;
close 'add';
end;

--关键字带反引号-合理报错
start transaction;
cursor `add` for select * from add_test order by 1;
close `add`;
end;

--清理环境
drop table add_test;