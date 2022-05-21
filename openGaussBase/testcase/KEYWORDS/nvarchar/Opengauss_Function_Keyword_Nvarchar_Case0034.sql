-- @testpoint: opengauss关键字nvarchar(非保留)，作为游标名,部分测试点合理报错

--step1:建表;expect:成功
drop table if exists t_nvarchar_0034 cascade;
create table t_nvarchar_0034(cid int,fid int);

--step2:关键字不带引号;expect:成功
start transaction;
cursor nvarchar for select * from t_nvarchar_0034 order by 1;
close nvarchar;
end;

--step3:关键字带双引号;expect:成功
start transaction;
cursor "nvarchar" for select * from t_nvarchar_0034 order by 1;
close "nvarchar";
end;

--step4:关键字带单引号;expect:合理报错
start transaction;
cursor 'nvarchar' for select * from t_nvarchar_0034 order by 1;
close 'nvarchar';
end;

--step5:关键字带反引号;expect:合理报错
start transaction;
cursor `nvarchar` for select * from t_nvarchar_0034 order by 1;
close `nvarchar`;
end;

--step6:清理环境;expect:成功
drop table if exists t_nvarchar_0034 cascade;
