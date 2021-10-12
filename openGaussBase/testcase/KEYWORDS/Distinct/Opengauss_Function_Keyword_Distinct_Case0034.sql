-- @testpoint: opengauss关键字distinct(保留)，作为游标名，部分测试点合理报错

--前置条件
drop table if exists distinct_test cascade;
create table distinct_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor distinct for select * from distinct_test order by 1;
close distinct;
end;

--关键字带双引号-成功
start transaction;
cursor "distinct" for select * from distinct_test order by 1;
close "distinct";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'distinct' for select * from distinct_test order by 1;
close 'distinct';
end;

--关键字带反引号-合理报错
start transaction;
cursor `distinct` for select * from distinct_test order by 1;
close `distinct`;
end;
drop table if exists distinct_test cascade;