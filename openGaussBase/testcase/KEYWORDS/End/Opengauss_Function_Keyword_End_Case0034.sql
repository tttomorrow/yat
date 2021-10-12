-- @testpoint: opengauss关键字end(保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists end_test cascade;
create table end_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor end for select * from end_test order by 1;
close end;
end;

--关键字带双引号-成功
start transaction;
cursor "end" for select * from end_test order by 1;
close "end";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'end' for select * from end_test order by 1;
close 'end';
end;

--关键字带反引号-合理报错
start transaction;
cursor `end` for select * from end_test order by 1;
close `end`;
end;
drop table if exists end_test cascade;
