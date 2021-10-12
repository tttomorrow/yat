-- @testpoint: opengauss关键字dec(非保留)，作为函数名，部分测试点合理报错

--关键字不带引号-合理报错
drop function if exists dec;
create function dec(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带双引号-成功(开发者指南备注不能是函数或类型，目前加引号作为函数名是成功的，需要与开发确认)
drop function if exists "dec";
create function "dec"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
select  "dec"(3);
drop function if exists "dec";
--关键字带单引号-合理报错
drop function if exists 'dec';
create function 'dec'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带反引号-合理报错
drop function if exists `dec`;
create function `dec`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/