-- @testpoint: 输入参数类型完全匹配

-- @testpoint：输入参数类型完全匹配：success
-- @lengthb(string)
explain performance SELECT lengthb('hello'::text);
explain performance SELECT lengthb('hello'::bpchar);

--清理环境
--no need to clean