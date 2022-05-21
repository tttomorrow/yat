-- @testpoint: opengauss关键字nvarchar(非保留)，作为函数名 部分测试点合理报错
--step1:关键字不带引号;expect:合理报错
create or replace function nvarchar(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

--step2:关键字带双引号;expect:成功
create or replace function "nvarchar"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function if exists "nvarchar"(i integer);

--step3:关键字带单引号;expect:合理报错
drop function if exists 'nvarchar'(i integer);
create function 'nvarchar'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

--step4:关键字带反引号;expect:合理报错
drop function if exists `nvarchar`(i integer);
create function `nvarchar`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
