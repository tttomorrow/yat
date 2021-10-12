-- @testpoint: opengauss关键字decimal(非保留)，作为函数名，部分测试点合理报错

--关键字不带引号-失败(不可以是函数名)
drop function if exists decimal;
create function decimal(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带双引号-成功（强制使用关键字）
drop function if exists "decimal";
create function "decimal"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
select "decimal"(3);
drop function if exists "decimal";
--关键字带单引号-合理报错
drop function if exists 'decimal';
create function 'decimal'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带反引号-合理报错
drop function if exists `decimal`;
create function `decimal`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/