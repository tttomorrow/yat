-- @testpoint: opengauss关键字do(保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists do_test cascade;
create table do_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor do for select * from do_test order by 1;
close do;
end;

--关键字带双引号-成功
start transaction;
cursor "do" for select * from do_test order by 1;
close "do";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'do' for select * from do_test order by 1;
close 'do';
end;

--关键字带反引号-合理报错
start transaction;
cursor `do` for select * from do_test order by 1;
close `do`;
end;
drop table if exists do_test cascade;
