-- @testpoint: 输入类型不匹配但是可以隐式转换为匹配

-- @repeat(string text, number int )
-- @testpoint：输入类型不匹配但是可以隐式转换为匹配：success
explain performance select repeat(123, 2);
explain performance select repeat(0.01, 4);
explain performance select repeat(HEXTORAW('DEADBEEF'), 3);
explain performance select repeat(date '2020-12-3', 2);
explain performance select repeat(timestamp without time zone '2020-12-3', 2);

--清理环境
--no need to clean