-- @testpoint: opengauss关键字min(非保留)，作为函数名,部分测试点合理报错

--关键字不带引号-成功

create function min(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function  min(i integer);
--关键字带双引号-成功

create function "min"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function  "min"(i integer);
--关键字带单引号-合理报错

create function 'min'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function 'min'(i integer);
--关键字带反引号-合理报错

create function `min`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function  `min`(i integer);
